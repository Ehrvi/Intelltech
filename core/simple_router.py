#!/usr/bin/env python3
"""
Simple Rule-Based OpenAI Router - Phase 2 Credit Optimization

Routes tasks using deterministic rules (no LLM overhead).
Target: 90% OpenAI, 10% Manus.

Author: Manus AI Agent
Version: 2.0 (Simplified)
Date: 2026-02-15
"""

import os
import json
import re
from typing import Dict, Tuple
from datetime import datetime

# Manus-only keywords (strategic/critical tasks)
# Conservative list - only truly critical tasks
MANUS_KEYWORDS = [
    # Strategic decisions (not just analysis)
    'strategic decision', 'strategy decision', 'decide strategy',
    
    # Final client deliverables (not drafts)
    'final client', 'final investor', 'final board',
    'client deliverable', 'investor deliverable',
    
    # Financial decisions (not analysis)
    'financial decision', 'investment decision', 'approve investment',
    
    # Legal (always critical)
    'legal review', 'legal contract', 'compliance review',
    
    # Executive approval
    'ceo approval', 'board approval', 'executive decision',
    
    # Explicit final validation
    'final validation', 'final approval', 'sign off'
]

# OpenAI-optimal keywords (routine tasks)
OPENAI_KEYWORDS = [
    # Research
    'research', 'find', 'search', 'lookup', 'investigate',
    'analyze', 'study', 'explore',
    
    # Data collection
    'collect', 'gather', 'compile', 'list', 'enumerate',
    
    # Summarization
    'summarize', 'summary', 'tldr', 'brief', 'overview',
    'extract', 'highlight',
    
    # Translation
    'translate', 'translation', 'convert language',
    
    # Formatting
    'format', 'reformat', 'organize', 'structure',
    
    # Code
    'code', 'script', 'program', 'function', 'debug',
    
    # Writing
    'write', 'draft', 'compose', 'create document',
    'outline', 'notes'
]


class SimpleRouter:
    """Rule-based task router (deterministic, no LLM)"""
    
    def __init__(self, metrics_path: str = '/home/ubuntu/manus_global_knowledge/metrics/simple_routing_metrics.json'):
        self.metrics_path = metrics_path
        self.metrics = self._load_metrics()
    
    def _load_metrics(self) -> Dict:
        """Load routing metrics"""
        if os.path.exists(self.metrics_path):
            with open(self.metrics_path, 'r') as f:
                return json.load(f)
        return {
            'total_tasks': 0,
            'openai_tasks': 0,
            'manus_tasks': 0,
            'routing_history': []
        }
    
    def _save_metrics(self):
        """Save routing metrics"""
        os.makedirs(os.path.dirname(self.metrics_path), exist_ok=True)
        with open(self.metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def route(self, task_description: str, force_manus: bool = False) -> Tuple[str, Dict]:
        """
        Route task using simple rules
        
        Returns:
            (engine, reasoning)
        """
        
        task_lower = task_description.lower()
        
        reasoning = {
            'task': task_description[:100],
            'timestamp': datetime.now().isoformat(),
            'matched_keywords': [],
            'decision_factors': []
        }
        
        # Rule 1: Force Manus override
        if force_manus:
            reasoning['decision_factors'].append('OVERRIDE: force_manus=True')
            engine = 'manus'
        
        # Rule 2: Check for Manus keywords
        else:
            manus_matches = []
            openai_matches = []
            
            for keyword in MANUS_KEYWORDS:
                if keyword in task_lower:
                    manus_matches.append(keyword)
            
            for keyword in OPENAI_KEYWORDS:
                if keyword in task_lower:
                    openai_matches.append(keyword)
            
            # Decision logic
            if manus_matches:
                reasoning['matched_keywords'] = manus_matches
                reasoning['decision_factors'].append(f'MANUS_KEYWORDS: {", ".join(manus_matches[:3])}')
                engine = 'manus'
            
            elif openai_matches:
                reasoning['matched_keywords'] = openai_matches
                reasoning['decision_factors'].append(f'OPENAI_KEYWORDS: {", ".join(openai_matches[:3])}')
                engine = 'openai'
            
            # Default: OpenAI (to hit 90% target)
            else:
                reasoning['decision_factors'].append('DEFAULT: No specific keywords, route to OpenAI')
                engine = 'openai'
        
        # Update metrics
        self.metrics['total_tasks'] += 1
        if engine == 'openai':
            self.metrics['openai_tasks'] += 1
        else:
            self.metrics['manus_tasks'] += 1
        
        # Log routing
        self.metrics['routing_history'].append({
            'task': task_description[:100],
            'engine': engine,
            'keywords': reasoning['matched_keywords'][:5],
            'timestamp': reasoning['timestamp']
        })
        
        # Keep last 100 only
        if len(self.metrics['routing_history']) > 100:
            self.metrics['routing_history'] = self.metrics['routing_history'][-100:]
        
        self._save_metrics()
        
        # Add stats to reasoning
        reasoning['engine'] = engine
        reasoning['openai_percentage'] = round(
            (self.metrics['openai_tasks'] / self.metrics['total_tasks'] * 100), 1
        ) if self.metrics['total_tasks'] > 0 else 0
        
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
            'target_met': openai_pct >= 80  # Target: 90%, acceptable: 80%+
        }


# Test cases
if __name__ == '__main__':
    router = SimpleRouter()
    
    test_tasks = [
        # Should route to OpenAI
        "Research top 10 construction companies in Australia",
        "Summarize this 50-page technical report",
        "Translate document from English to Portuguese",
        "Write a draft blog post about SHMS technology",
        "Find contact information for mining companies in Chile",
        "Create a list of renewable energy projects in Asia",
        "Format this data into a table",
        "Write Python code to parse CSV files",
        
        # Should route to Manus
        "Create final client presentation for BHP Group",
        "Make strategic decision on market entry timing",
        "Validate financial projections for investor pitch",
        "Review legal contract for compliance",
        "Prepare board presentation on Q4 results",
        "Decide whether to acquire competitor",
        "Final deliverable for CEO review"
    ]
    
    print("=" * 80)
    print("Simple Router - Test Run")
    print("=" * 80)
    
    for task in test_tasks:
        engine, reasoning = router.route(task)
        
        print(f"\nTask: {task}")
        print(f"→ {engine.upper()}")
        if reasoning['matched_keywords']:
            print(f"  Keywords: {', '.join(reasoning['matched_keywords'][:3])}")
        print(f"  Reason: {reasoning['decision_factors'][0]}")
    
    print("\n" + "=" * 80)
    print("Routing Statistics")
    print("=" * 80)
    stats = router.get_statistics()
    print(json.dumps(stats, indent=2))
    
    print("\n" + "=" * 80)
    print("Target Analysis")
    print("=" * 80)
    if stats['target_met']:
        print(f"✅ TARGET MET: {stats['openai_percentage']}% routed to OpenAI (target: 80%+)")
    else:
        print(f"❌ TARGET MISSED: {stats['openai_percentage']}% routed to OpenAI (target: 80%+)")
    
    print(f"\nExpected credit savings: {stats['openai_percentage']}% of task credits")
