#!/usr/bin/env python3
"""
Guardian Validation Middleware - Phase 2 Credit Optimization

Validates OpenAI outputs for quality before delivery.
Escalates to Manus if quality < 80%.

Author: Manus AI Agent
Version: 1.0
Date: 2026-02-15
"""

import os
import json
from typing import Dict, Tuple, List
from datetime import datetime
from openai import OpenAI

# Initialize OpenAI client
api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
if not api_base.startswith('http'):
    api_base = f'https://{api_base}'

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=api_base
)


class GuardianValidator:
    """Quality assurance middleware for OpenAI outputs"""
    
    QUALITY_THRESHOLD = 80  # Minimum acceptable quality (0-100)
    
    def __init__(self, metrics_path: str = '/home/ubuntu/manus_global_knowledge/metrics/validation_metrics.json'):
        self.metrics_path = metrics_path
        self.metrics = self._load_metrics()
    
    def _load_metrics(self) -> Dict:
        """Load validation metrics"""
        if os.path.exists(self.metrics_path):
            with open(self.metrics_path, 'r') as f:
                return json.load(f)
        return {
            'total_validations': 0,
            'passed': 0,
            'failed': 0,
            'escalated': 0,
            'average_quality': 0,
            'validation_history': []
        }
    
    def _save_metrics(self):
        """Save validation metrics"""
        os.makedirs(os.path.dirname(self.metrics_path), exist_ok=True)
        with open(self.metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def validate_simple(self, task: str, output: str) -> Tuple[bool, Dict]:
        """
        Simple rule-based validation (no LLM overhead)
        
        Checks:
        - Output is not empty
        - Output length is reasonable
        - No obvious errors
        
        Returns:
            (passes, validation_report)
        """
        
        issues = []
        quality_score = 100
        
        # Check 1: Not empty
        if not output or len(output.strip()) < 10:
            issues.append("Output is empty or too short")
            quality_score -= 50
        
        # Check 2: Not just error message
        error_indicators = ['error:', 'exception:', 'failed:', 'could not', 'unable to']
        if any(indicator in output.lower() for indicator in error_indicators):
            issues.append("Output contains error indicators")
            quality_score -= 30
        
        # Check 3: Reasonable length (not truncated)
        if len(output) < 50 and 'research' in task.lower():
            issues.append("Output seems too short for research task")
            quality_score -= 20
        
        # Check 4: Contains relevant keywords from task
        task_words = set(task.lower().split())
        output_words = set(output.lower().split())
        overlap = len(task_words & output_words)
        
        if overlap < 2:
            issues.append("Output doesn't seem related to task")
            quality_score -= 20
        
        passes = quality_score >= self.QUALITY_THRESHOLD
        
        validation = {
            'method': 'simple_rules',
            'quality_score': max(0, quality_score),
            'passes': passes,
            'issues': issues,
            'recommendation': 'approve' if passes else 'escalate',
            'timestamp': datetime.now().isoformat()
        }
        
        # Update metrics
        self.metrics['total_validations'] += 1
        if passes:
            self.metrics['passed'] += 1
        else:
            self.metrics['failed'] += 1
            self.metrics['escalated'] += 1
        
        # Update average quality
        total = self.metrics['total_validations']
        prev_avg = self.metrics['average_quality']
        self.metrics['average_quality'] = round(
            (prev_avg * (total - 1) + quality_score) / total, 1
        )
        
        # Log validation
        self.metrics['validation_history'].append({
            'task': task[:100],
            'quality_score': quality_score,
            'passes': passes,
            'timestamp': validation['timestamp']
        })
        
        # Keep last 100 only
        if len(self.metrics['validation_history']) > 100:
            self.metrics['validation_history'] = self.metrics['validation_history'][-100:]
        
        self._save_metrics()
        
        return passes, validation
    
    def validate_with_llm(self, task: str, output: str, criteria: List[str] = None) -> Tuple[bool, Dict]:
        """
        LLM-based validation (higher quality, higher cost)
        
        Use this for critical tasks only.
        
        Returns:
            (passes, validation_report)
        """
        
        if criteria is None:
            criteria = ['completeness', 'accuracy', 'relevance', 'clarity']
        
        prompt = f"""Validate this AI-generated output:

TASK: {task}

OUTPUT:
{output[:2000]}

CRITERIA: {', '.join(criteria)}

Provide JSON response with:
- quality_score: 0-100
- criteria_scores: {{criterion: 0-100, ...}}
- issues: [list of issues found]
- recommendation: 'approve' or 'escalate'

Respond ONLY with valid JSON."""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a quality assurance expert. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            validation = json.loads(response.choices[0].message.content)
            validation['method'] = 'llm_validation'
            validation['timestamp'] = datetime.now().isoformat()
            
            passes = validation['quality_score'] >= self.QUALITY_THRESHOLD
            validation['passes'] = passes
            
            # Update metrics
            self.metrics['total_validations'] += 1
            if passes:
                self.metrics['passed'] += 1
            else:
                self.metrics['failed'] += 1
                self.metrics['escalated'] += 1
            
            # Update average
            total = self.metrics['total_validations']
            prev_avg = self.metrics['average_quality']
            self.metrics['average_quality'] = round(
                (prev_avg * (total - 1) + validation['quality_score']) / total, 1
            )
            
            # Log
            self.metrics['validation_history'].append({
                'task': task[:100],
                'quality_score': validation['quality_score'],
                'passes': passes,
                'timestamp': validation['timestamp']
            })
            
            if len(self.metrics['validation_history']) > 100:
                self.metrics['validation_history'] = self.metrics['validation_history'][-100:]
            
            self._save_metrics()
            
            return passes, validation
            
        except Exception as e:
            # Fallback to simple validation
            return self.validate_simple(task, output)
    
    def get_statistics(self) -> Dict:
        """Get validation statistics"""
        total = self.metrics['total_validations']
        if total == 0:
            return {
                'total_validations': 0,
                'pass_rate': 0,
                'escalation_rate': 0,
                'average_quality': 0
            }
        
        return {
            'total_validations': total,
            'passed': self.metrics['passed'],
            'failed': self.metrics['failed'],
            'escalated': self.metrics['escalated'],
            'pass_rate': round((self.metrics['passed'] / total) * 100, 1),
            'escalation_rate': round((self.metrics['escalated'] / total) * 100, 1),
            'average_quality': self.metrics['average_quality']
        }


# Test cases
if __name__ == '__main__':
    validator = GuardianValidator()
    
    test_cases = [
        # Good outputs
        {
            'task': 'Research top 5 construction companies in Australia',
            'output': '''Here are the top 5 construction companies in Australia:

1. Lendlease - Major infrastructure and construction company
2. CIMIC Group - Engineering and construction services
3. John Holland - Infrastructure construction
4. CPB Contractors - Civil engineering and construction
5. Multiplex - Building and construction

These companies are leaders in the Australian construction market.'''
        },
        
        # Bad output (too short)
        {
            'task': 'Summarize the 50-page technical report on SHMS',
            'output': 'The report discusses SHMS technology.'
        },
        
        # Bad output (error)
        {
            'task': 'Translate document to Portuguese',
            'output': 'Error: Could not complete translation. File format not supported.'
        },
        
        # Good output (code)
        {
            'task': 'Write Python code to parse CSV files',
            'output': '''import csv

def parse_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    return data

# Usage
data = parse_csv('data.csv')
print(f"Loaded {len(data)} rows")'''
        }
    ]
    
    print("=" * 80)
    print("Guardian Validator - Test Run")
    print("=" * 80)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n[Test {i}]")
        print(f"Task: {test['task']}")
        print(f"Output length: {len(test['output'])} chars")
        
        passes, validation = validator.validate_simple(test['task'], test['output'])
        
        print(f"→ {'✅ PASS' if passes else '❌ FAIL'} (Quality: {validation['quality_score']}/100)")
        if validation['issues']:
            print(f"  Issues: {', '.join(validation['issues'])}")
        print(f"  Recommendation: {validation['recommendation'].upper()}")
    
    print("\n" + "=" * 80)
    print("Validation Statistics")
    print("=" * 80)
    stats = validator.get_statistics()
    print(json.dumps(stats, indent=2))
    
    print("\n" + "=" * 80)
    print("Quality Analysis")
    print("=" * 80)
    if stats['pass_rate'] >= 80:
        print(f"✅ QUALITY TARGET MET: {stats['pass_rate']}% pass rate (target: 80%+)")
    else:
        print(f"❌ QUALITY TARGET MISSED: {stats['pass_rate']}% pass rate (target: 80%+)")
    
    print(f"Average quality score: {stats['average_quality']}/100")
    print(f"Escalation rate: {stats['escalation_rate']}%")
