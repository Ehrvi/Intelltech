#!/usr/bin/env python3
"""
OpenAI Routing Decision Engine - Phase 2 Credit Optimization

Routes tasks to OpenAI (90%) or Manus (10%) based on complexity, criticality, and task type.
Implements "First Rule Over All" with scientific decision-making framework.

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


class TaskRouter:
    """Routes tasks to optimal execution engine (OpenAI or Manus)"""
    
    # Decision thresholds (scientifically calibrated)
    MANUS_COMPLEXITY_THRESHOLD = 8  # 1-10 scale
    MANUS_CRITICALITY_THRESHOLD = 8  # 1-10 scale
    
    # Task categories that MUST use Manus
    MANUS_ONLY_CATEGORIES = [
        'strategic_decision',
        'client_deliverable',
        'financial_analysis',
        'legal_review',
        'final_validation'
    ]
    
    # Task categories optimal for OpenAI
    OPENAI_OPTIMAL_CATEGORIES = [
        'research',
        'data_collection',
        'summarization',
        'classification',
        'translation',
        'formatting',
        'code_generation',
        'writing_draft'
    ]
    
    def __init__(self, metrics_path: str = '/home/ubuntu/manus_global_knowledge/metrics/routing_metrics.json'):
        self.metrics_path = metrics_path
        self.metrics = self._load_metrics()
    
    def _load_metrics(self) -> Dict:
        """Load routing metrics from disk"""
        if os.path.exists(self.metrics_path):
            with open(self.metrics_path, 'r') as f:
                return json.load(f)
        return {
            'total_tasks': 0,
            'openai_tasks': 0,
            'manus_tasks': 0,
            'escalations': 0,
            'quality_failures': 0,
            'routing_history': []
        }
    
    def _save_metrics(self):
        """Save routing metrics to disk"""
        os.makedirs(os.path.dirname(self.metrics_path), exist_ok=True)
        with open(self.metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def analyze_task(self, task_description: str) -> Dict:
        """
        Analyze task characteristics using OpenAI
        
        Returns:
            {
                'complexity': 1-10,
                'criticality': 1-10,
                'category': str,
                'volume': int,
                'homogeneity': 1-10,
                'client_facing': bool,
                'strategic': bool
            }
        """
        
        prompt = f"""Analyze this task and provide structured assessment:

Task: {task_description}

Guidelines:
- Research/data collection/summarization are typically complexity 3-5, criticality 3-5
- Translation/formatting/code generation are complexity 2-4, criticality 2-4
- Strategic decisions/client deliverables are complexity 8-10, criticality 8-10
- Most routine tasks are NOT client-facing and NOT strategic

Provide JSON response with:
- complexity: 1-10 (1=trivial like formatting, 5=moderate research, 10=strategic decision)
- criticality: 1-10 (1=low impact internal task, 5=important but not critical, 10=mission critical client deliverable)
- category: one of [research, data_collection, summarization, classification, translation, formatting, code_generation, writing_draft, strategic_decision, client_deliverable, financial_analysis, legal_review, final_validation, other]
- volume: number of items to process (1 if single task)
- homogeneity: 1-10 (1=unique, 10=identical subtasks)
- client_facing: true/false (only true if directly delivered to external client)
- strategic: true/false (only true if affects company strategy/direction)

Respond ONLY with valid JSON, no explanation."""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a task analysis expert. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            # Fallback: conservative defaults (route to Manus)
            return {
                'complexity': 9,
                'criticality': 9,
                'category': 'other',
                'volume': 1,
                'homogeneity': 1,
                'client_facing': True,
                'strategic': True,
                'error': str(e)
            }
    
    def route(self, task_description: str, force_manus: bool = False) -> Tuple[str, Dict]:
        """
        Route task to OpenAI or Manus
        
        Args:
            task_description: Natural language task description
            force_manus: Override routing logic (for testing)
        
        Returns:
            (engine, reasoning) where engine is 'openai' or 'manus'
        """
        
        # Analyze task
        analysis = self.analyze_task(task_description)
        
        # Decision logic (scientific framework)
        reasoning = {
            'analysis': analysis,
            'decision_factors': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Rule 1: Force Manus override
        if force_manus:
            reasoning['decision_factors'].append('OVERRIDE: force_manus=True')
            engine = 'manus'
        
        # Rule 2: Manus-only categories
        elif analysis['category'] in self.MANUS_ONLY_CATEGORIES:
            reasoning['decision_factors'].append(f"MANUS_ONLY_CATEGORY: {analysis['category']}")
            engine = 'manus'
        
        # Rule 3: High complexity threshold
        elif analysis['complexity'] >= self.MANUS_COMPLEXITY_THRESHOLD:
            reasoning['decision_factors'].append(f"HIGH_COMPLEXITY: {analysis['complexity']}/10")
            engine = 'manus'
        
        # Rule 4: High criticality threshold
        elif analysis['criticality'] >= self.MANUS_CRITICALITY_THRESHOLD:
            reasoning['decision_factors'].append(f"HIGH_CRITICALITY: {analysis['criticality']}/10")
            engine = 'manus'
        
        # Rule 5: Client-facing + strategic
        elif analysis['client_facing'] and analysis['strategic']:
            reasoning['decision_factors'].append('CLIENT_FACING + STRATEGIC')
            engine = 'manus'
        
        # Rule 6: OpenAI optimal categories
        elif analysis['category'] in self.OPENAI_OPTIMAL_CATEGORIES:
            reasoning['decision_factors'].append(f"OPENAI_OPTIMAL: {analysis['category']}")
            engine = 'openai'
        
        # Default: OpenAI (90% target)
        else:
            reasoning['decision_factors'].append('DEFAULT: OpenAI for non-critical tasks')
            engine = 'openai'
        
        # Update metrics
        self.metrics['total_tasks'] += 1
        if engine == 'openai':
            self.metrics['openai_tasks'] += 1
        else:
            self.metrics['manus_tasks'] += 1
        
        # Log routing decision
        self.metrics['routing_history'].append({
            'task': task_description[:100],
            'engine': engine,
            'analysis': analysis,
            'timestamp': reasoning['timestamp']
        })
        
        # Keep only last 100 routing decisions
        if len(self.metrics['routing_history']) > 100:
            self.metrics['routing_history'] = self.metrics['routing_history'][-100:]
        
        self._save_metrics()
        
        reasoning['engine'] = engine
        reasoning['openai_percentage'] = (self.metrics['openai_tasks'] / self.metrics['total_tasks'] * 100) if self.metrics['total_tasks'] > 0 else 0
        
        return engine, reasoning
    
    def get_statistics(self) -> Dict:
        """Get routing statistics"""
        total = self.metrics['total_tasks']
        if total == 0:
            return {
                'total_tasks': 0,
                'openai_percentage': 0,
                'manus_percentage': 0,
                'target_met': False
            }
        
        openai_pct = (self.metrics['openai_tasks'] / total) * 100
        manus_pct = (self.metrics['manus_tasks'] / total) * 100
        
        return {
            'total_tasks': total,
            'openai_tasks': self.metrics['openai_tasks'],
            'manus_tasks': self.metrics['manus_tasks'],
            'openai_percentage': round(openai_pct, 1),
            'manus_percentage': round(manus_pct, 1),
            'target_met': openai_pct >= 80,  # Target: 90%, acceptable: 80%+
            'escalations': self.metrics['escalations'],
            'quality_failures': self.metrics['quality_failures']
        }


class GuardianValidator:
    """Validates OpenAI outputs for quality assurance"""
    
    QUALITY_THRESHOLD = 80  # Minimum quality score (0-100)
    
    def __init__(self, router: TaskRouter):
        self.router = router
    
    def validate(self, task: str, output: str, expected_criteria: List[str] = None) -> Tuple[bool, Dict]:
        """
        Validate OpenAI output quality
        
        Args:
            task: Original task description
            output: OpenAI-generated output
            expected_criteria: List of quality criteria to check
        
        Returns:
            (passes, validation_report)
        """
        
        if expected_criteria is None:
            expected_criteria = [
                'completeness',
                'accuracy',
                'relevance',
                'clarity',
                'format'
            ]
        
        prompt = f"""Validate this AI-generated output:

TASK: {task}

OUTPUT:
{output[:2000]}  # Limit to first 2000 chars for validation

CRITERIA: {', '.join(expected_criteria)}

Provide JSON response with:
- overall_quality: 0-100 score
- criteria_scores: {{criterion: 0-100, ...}}
- issues: [list of quality issues found]
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
            
            passes = validation['overall_quality'] >= self.QUALITY_THRESHOLD
            
            # Update metrics
            if not passes:
                self.router.metrics['escalations'] += 1
                self.router.metrics['quality_failures'] += 1
                self.router._save_metrics()
            
            return passes, validation
            
        except Exception as e:
            # Fallback: escalate on validation error
            return False, {
                'overall_quality': 0,
                'criteria_scores': {},
                'issues': [f'Validation error: {str(e)}'],
                'recommendation': 'escalate',
                'error': str(e)
            }


def execute_with_openai(task: str, model: str = "gpt-4o") -> str:
    """
    Execute task using OpenAI
    
    Args:
        task: Task description
        model: OpenAI model to use (gpt-4o, gpt-4o-mini)
    
    Returns:
        Generated output
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Provide high-quality, accurate responses."},
                {"role": "user", "content": task}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        raise Exception(f"OpenAI execution failed: {str(e)}")


# Example usage
if __name__ == '__main__':
    # Initialize router
    router = TaskRouter()
    validator = GuardianValidator(router)
    
    # Example tasks
    test_tasks = [
        "Research top 10 construction companies in Australia",
        "Create final client presentation for BHP Group",
        "Summarize this 50-page technical report",
        "Make strategic decision on market entry timing",
        "Translate document from English to Portuguese",
        "Validate financial projections for investor pitch"
    ]
    
    print("=" * 80)
    print("OpenAI Router - Test Run")
    print("=" * 80)
    
    for task in test_tasks:
        engine, reasoning = router.route(task)
        
        print(f"\nTask: {task}")
        print(f"Routed to: {engine.upper()}")
        print(f"Complexity: {reasoning['analysis']['complexity']}/10")
        print(f"Criticality: {reasoning['analysis']['criticality']}/10")
        print(f"Category: {reasoning['analysis']['category']}")
        print(f"Reasoning: {', '.join(reasoning['decision_factors'])}")
    
    print("\n" + "=" * 80)
    print("Routing Statistics")
    print("=" * 80)
    stats = router.get_statistics()
    print(json.dumps(stats, indent=2))
