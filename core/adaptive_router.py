#!/usr/bin/env python3
"""
Adaptive Self-Learning Router - Phase 2.1

Learns from routing outcomes to improve accuracy over time.
Starts with rule-based routing, evolves to pattern-based ML routing.

Author: Manus AI Agent
Version: 2.1 (Self-Learning)
Date: 2026-02-15
"""

import os
import json
import re
from typing import Dict, Tuple, List
from datetime import datetime
from collections import defaultdict

# Initial routing rules (same as Phase 2.0)
MANUS_KEYWORDS = [
    'strategic decision', 'strategy decision', 'decide strategy',
    'final client', 'final investor', 'final board',
    'client deliverable', 'investor deliverable',
    'financial decision', 'investment decision', 'approve investment',
    'legal review', 'legal contract', 'compliance review',
    'ceo approval', 'board approval', 'executive decision',
    'final validation', 'final approval', 'sign off'
]

OPENAI_KEYWORDS = [
    'research', 'find', 'search', 'lookup', 'investigate', 'analyze', 'study', 'explore',
    'collect', 'gather', 'compile', 'list', 'enumerate',
    'summarize', 'summary', 'tldr', 'brief', 'overview', 'extract', 'highlight',
    'translate', 'translation', 'convert language',
    'format', 'reformat', 'organize', 'structure',
    'code', 'script', 'program', 'function', 'debug',
    'write', 'draft', 'compose', 'create document', 'outline', 'notes'
]


class AdaptiveRouter:
    """Self-learning router that improves over time"""
    
    # Learning parameters
    MIN_SAMPLES_FOR_LEARNING = 20  # Start learning after 20 tasks
    CONFIDENCE_THRESHOLD = 0.85    # High confidence threshold
    RETRAINING_INTERVAL = 50       # Retrain every 50 tasks
    
    def __init__(self, 
                 metrics_path: str = '/home/ubuntu/manus_global_knowledge/metrics/adaptive_routing_metrics.json',
                 learning_data_path: str = '/home/ubuntu/manus_global_knowledge/metrics/learning_data.json'):
        self.metrics_path = metrics_path
        self.learning_data_path = learning_data_path
        self.metrics = self._load_metrics()
        self.learning_data = self._load_learning_data()
        self.keyword_stats = self._compute_keyword_stats()
        self.last_decision = None
    
    def _load_metrics(self) -> Dict:
        """Load routing metrics"""
        if os.path.exists(self.metrics_path):
            with open(self.metrics_path, 'r') as f:
                return json.load(f)
        return {
            'total_tasks': 0,
            'openai_tasks': 0,
            'manus_tasks': 0,
            'rule_based_decisions': 0,
            'learned_decisions': 0,
            'learning_enabled': False,
            'routing_history': []
        }
    
    def _load_learning_data(self) -> List[Dict]:
        """Load historical learning data"""
        if os.path.exists(self.learning_data_path):
            with open(self.learning_data_path, 'r') as f:
                return json.load(f)
        return []
    
    def _save_metrics(self):
        """Save routing metrics"""
        os.makedirs(os.path.dirname(self.metrics_path), exist_ok=True)
        with open(self.metrics_path, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def _save_learning_data(self):
        """Save learning data"""
        os.makedirs(os.path.dirname(self.learning_data_path), exist_ok=True)
        with open(self.learning_data_path, 'w') as f:
            json.dump(self.learning_data, f, indent=2)
    
    def _extract_features(self, task: str) -> Dict:
        """Extract features from task for learning"""
        task_lower = task.lower()
        
        # Extract keywords
        manus_keywords_found = [kw for kw in MANUS_KEYWORDS if kw in task_lower]
        openai_keywords_found = [kw for kw in OPENAI_KEYWORDS if kw in task_lower]
        
        # Extract other features
        features = {
            'length': len(task),
            'word_count': len(task.split()),
            'has_numbers': bool(re.search(r'\d', task)),
            'has_question': '?' in task,
            'manus_keyword_count': len(manus_keywords_found),
            'openai_keyword_count': len(openai_keywords_found),
            'manus_keywords': manus_keywords_found[:3],  # Top 3
            'openai_keywords': openai_keywords_found[:3],  # Top 3
            'starts_with_verb': task.split()[0].lower() in ['research', 'find', 'create', 'make', 'write', 'translate', 'summarize'] if task.split() else False
        }
        
        return features
    
    def _compute_keyword_stats(self) -> Dict:
        """Compute success statistics for each keyword"""
        stats = defaultdict(lambda: {'openai_success': 0, 'openai_total': 0, 'manus_success': 0, 'manus_total': 0})
        
        for entry in self.learning_data:
            if 'outcome' not in entry:
                continue
            
            keywords = entry.get('features', {}).get('manus_keywords', []) + entry.get('features', {}).get('openai_keywords', [])
            routed_to = entry.get('routed_to')
            success = entry.get('outcome', {}).get('success', False)
            
            for keyword in keywords:
                if routed_to == 'openai':
                    stats[keyword]['openai_total'] += 1
                    if success:
                        stats[keyword]['openai_success'] += 1
                elif routed_to == 'manus':
                    stats[keyword]['manus_total'] += 1
                    if success:
                        stats[keyword]['manus_success'] += 1
        
        # Compute success rates
        for keyword, data in stats.items():
            if data['openai_total'] > 0:
                data['openai_success_rate'] = data['openai_success'] / data['openai_total']
            else:
                data['openai_success_rate'] = 0.5  # Unknown, assume 50%
            
            if data['manus_total'] > 0:
                data['manus_success_rate'] = data['manus_success'] / data['manus_total']
            else:
                data['manus_success_rate'] = 0.95  # Assume Manus is high quality
        
        return dict(stats)
    
    def _rule_based_route(self, task: str, features: Dict) -> str:
        """Original rule-based routing (Phase 2.0)"""
        task_lower = task.lower()
        
        # Check for Manus keywords
        if features['manus_keyword_count'] > 0:
            return 'manus'
        
        # Check for OpenAI keywords
        if features['openai_keyword_count'] > 0:
            return 'openai'
        
        # Default: OpenAI
        return 'openai'
    
    def _learned_route(self, task: str, features: Dict) -> Tuple[str, float]:
        """
        Learned routing based on historical patterns
        
        Returns:
            (engine, confidence)
        """
        
        # Extract keywords from task
        all_keywords = features['manus_keywords'] + features['openai_keywords']
        
        if not all_keywords:
            # No keywords, use rule-based default
            return 'openai', 0.5
        
        # Calculate confidence scores for each engine
        openai_confidence = 0
        manus_confidence = 0
        
        for keyword in all_keywords:
            if keyword in self.keyword_stats:
                stats = self.keyword_stats[keyword]
                openai_confidence += stats['openai_success_rate']
                manus_confidence += stats['manus_success_rate']
        
        # Normalize by number of keywords
        openai_confidence /= len(all_keywords)
        manus_confidence /= len(all_keywords)
        
        # Choose engine with higher confidence
        if openai_confidence > manus_confidence:
            return 'openai', openai_confidence
        else:
            return 'manus', manus_confidence
    
    def route(self, task: str, force_manus: bool = False) -> Tuple[str, Dict]:
        """
        Route task using adaptive learning
        
        Returns:
            (engine, reasoning)
        """
        
        # Extract features
        features = self._extract_features(task)
        
        reasoning = {
            'task': task[:100],
            'timestamp': datetime.now().isoformat(),
            'features': features,
            'decision_factors': []
        }
        
        # Rule 1: Force Manus override
        if force_manus:
            reasoning['decision_factors'].append('OVERRIDE: force_manus=True')
            engine = 'manus'
            decision_method = 'override'
            confidence = 1.0
        
        # Rule 2: Check if learning is enabled
        elif len(self.learning_data) >= self.MIN_SAMPLES_FOR_LEARNING:
            # Learning enabled, use learned patterns
            learned_engine, confidence = self._learned_route(task, features)
            rule_based_engine = self._rule_based_route(task, features)
            
            if confidence >= self.CONFIDENCE_THRESHOLD:
                # High confidence in learned decision
                engine = learned_engine
                decision_method = 'learned'
                reasoning['decision_factors'].append(f'LEARNED: {confidence:.2f} confidence → {engine.upper()}')
                self.metrics['learned_decisions'] += 1
            else:
                # Low confidence, fall back to rules
                engine = rule_based_engine
                decision_method = 'rule_based_fallback'
                reasoning['decision_factors'].append(f'RULE_BASED: Low confidence ({confidence:.2f}), using rules → {engine.upper()}')
                self.metrics['rule_based_decisions'] += 1
        
        else:
            # Not enough data, use rule-based
            engine = self._rule_based_route(task, features)
            decision_method = 'rule_based'
            confidence = 0.8 if features['manus_keyword_count'] > 0 or features['openai_keyword_count'] > 0 else 0.5
            reasoning['decision_factors'].append(f'RULE_BASED: {engine.upper()} (learning needs {self.MIN_SAMPLES_FOR_LEARNING - len(self.learning_data)} more samples)')
            self.metrics['rule_based_decisions'] += 1
        
        # Update metrics
        self.metrics['total_tasks'] += 1
        if engine == 'openai':
            self.metrics['openai_tasks'] += 1
        else:
            self.metrics['manus_tasks'] += 1
        
        # Check if learning is enabled
        if len(self.learning_data) >= self.MIN_SAMPLES_FOR_LEARNING:
            self.metrics['learning_enabled'] = True
        
        # Log routing decision
        self.metrics['routing_history'].append({
            'task': task[:100],
            'engine': engine,
            'method': decision_method,
            'confidence': confidence,
            'timestamp': reasoning['timestamp']
        })
        
        # Keep last 100 only
        if len(self.metrics['routing_history']) > 100:
            self.metrics['routing_history'] = self.metrics['routing_history'][-100:]
        
        self._save_metrics()
        
        # Store for outcome tracking
        self.last_decision = {
            'task': task,
            'routed_to': engine,
            'features': features,
            'confidence': confidence,
            'timestamp': reasoning['timestamp']
        }
        
        reasoning['engine'] = engine
        reasoning['confidence'] = confidence
        reasoning['decision_method'] = decision_method
        reasoning['learning_enabled'] = self.metrics['learning_enabled']
        reasoning['openai_percentage'] = round(
            (self.metrics['openai_tasks'] / self.metrics['total_tasks'] * 100), 1
        ) if self.metrics['total_tasks'] > 0 else 0
        
        return engine, reasoning
    
    def record_outcome(self, success: bool, quality_score: int, escalated: bool = False, user_feedback: str = None):
        """
        Record outcome of last routing decision for learning
        
        Args:
            success: Whether task completed successfully
            quality_score: Quality score 0-100
            escalated: Whether task was escalated to Manus
            user_feedback: Optional user feedback
        """
        
        if not self.last_decision:
            return
        
        # Create learning entry
        entry = {
            **self.last_decision,
            'outcome': {
                'success': success,
                'quality_score': quality_score,
                'escalated': escalated,
                'user_feedback': user_feedback,
                'timestamp': datetime.now().isoformat()
            }
        }
        
        self.learning_data.append(entry)
        self._save_learning_data()
        
        # Trigger retraining if needed
        if len(self.learning_data) % self.RETRAINING_INTERVAL == 0:
            self.retrain()
    
    def retrain(self):
        """Retrain routing logic based on accumulated learning data"""
        print(f"🔄 Retraining router with {len(self.learning_data)} samples...")
        
        # Recompute keyword statistics
        self.keyword_stats = self._compute_keyword_stats()
        
        # Analyze overall performance
        total_samples = len(self.learning_data)
        successful_openai = sum(1 for e in self.learning_data 
                               if e.get('routed_to') == 'openai' 
                               and e.get('outcome', {}).get('success', False))
        total_openai = sum(1 for e in self.learning_data if e.get('routed_to') == 'openai')
        
        if total_openai > 0:
            openai_success_rate = successful_openai / total_openai
            print(f"  OpenAI success rate: {openai_success_rate:.1%}")
        
        # Identify top performing keywords
        top_keywords = sorted(
            [(kw, stats['openai_success_rate']) for kw, stats in self.keyword_stats.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        print(f"  Top 10 keywords for OpenAI:")
        for kw, rate in top_keywords:
            print(f"    - {kw}: {rate:.1%} success")
        
        print(f"✅ Retraining complete")
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics including learning metrics"""
        total = self.metrics['total_tasks']
        if total == 0:
            return {
                'total_tasks': 0,
                'openai_percentage': 0,
                'manus_percentage': 0,
                'learning_enabled': False,
                'learning_samples': 0,
                'target_met': False
            }
        
        openai_pct = (self.metrics['openai_tasks'] / total) * 100
        manus_pct = (self.metrics['manus_tasks'] / total) * 100
        
        # Learning statistics
        if self.learning_data:
            recent_data = self.learning_data[-50:]  # Last 50 tasks
            successful = sum(1 for e in recent_data if e.get('outcome', {}).get('success', False))
            accuracy = (successful / len(recent_data) * 100) if recent_data else 0
        else:
            accuracy = 0
        
        return {
            'total_tasks': total,
            'openai_tasks': self.metrics['openai_tasks'],
            'manus_tasks': self.metrics['manus_tasks'],
            'openai_percentage': round(openai_pct, 1),
            'manus_percentage': round(manus_pct, 1),
            'target_met': openai_pct >= 80,
            'learning_enabled': self.metrics['learning_enabled'],
            'learning_samples': len(self.learning_data),
            'rule_based_decisions': self.metrics['rule_based_decisions'],
            'learned_decisions': self.metrics['learned_decisions'],
            'recent_accuracy': round(accuracy, 1),
            'keyword_patterns_learned': len(self.keyword_stats)
        }
    
    def get_learning_progress(self) -> Dict:
        """Get detailed learning progress report"""
        if not self.learning_data:
            return {'status': 'No learning data yet'}
        
        # Analyze learning progression over time
        batches = [self.learning_data[i:i+20] for i in range(0, len(self.learning_data), 20)]
        
        progression = []
        for i, batch in enumerate(batches):
            successful = sum(1 for e in batch if e.get('outcome', {}).get('success', False))
            accuracy = (successful / len(batch) * 100) if batch else 0
            progression.append({
                'batch': i + 1,
                'tasks': len(batch),
                'accuracy': round(accuracy, 1)
            })
        
        return {
            'total_samples': len(self.learning_data),
            'learning_enabled': self.metrics['learning_enabled'],
            'progression': progression,
            'keyword_patterns': len(self.keyword_stats),
            'top_keywords': sorted(
                [(kw, stats['openai_success_rate']) for kw, stats in self.keyword_stats.items()],
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }


# Test adaptive router
if __name__ == '__main__':
    router = AdaptiveRouter()
    
    # Simulate learning progression
    test_tasks = [
        # Batch 1: Initial tasks (rule-based)
        ("Research top 10 mining companies", True, 90),
        ("Translate document to Portuguese", True, 85),
        ("Write Python code", True, 88),
        ("Final client presentation", True, 95),  # Manus
        ("Summarize technical report", True, 92),
        
        # Batch 2: More tasks
        ("Find contact information", True, 87),
        ("Strategic decision on market entry", True, 95),  # Manus
        ("Format data into table", True, 90),
        ("Research renewable energy projects", True, 89),
        ("Legal contract review", True, 95),  # Manus
        
        # Continue for 20+ tasks to enable learning
        ("Analyze market trends", True, 88),
        ("Create draft proposal", True, 86),
        ("Search for industry reports", True, 91),
        ("Compile list of competitors", True, 89),
        ("Write blog post draft", True, 87),
        ("Research construction regulations", True, 90),
        ("Translate user manual", True, 85),
        ("Format spreadsheet data", True, 92),
        ("Find technical specifications", True, 88),
        ("Summarize meeting notes", True, 90),
        ("Research SHMS applications", True, 89),
    ]
    
    print("=" * 80)
    print("Adaptive Router - Learning Simulation")
    print("=" * 80)
    
    for i, (task, success, quality) in enumerate(test_tasks, 1):
        engine, reasoning = router.route(task)
        router.record_outcome(success=success, quality_score=quality, escalated=(quality < 80))
        
        print(f"\n[Task {i}] {task}")
        print(f"→ {engine.upper()} ({reasoning['decision_method']})")
        print(f"  Confidence: {reasoning['confidence']:.2f}")
        if reasoning['learning_enabled']:
            print(f"  🧠 Learning ENABLED")
    
    print("\n" + "=" * 80)
    print("Final Statistics")
    print("=" * 80)
    stats = router.get_statistics()
    print(json.dumps(stats, indent=2))
    
    print("\n" + "=" * 80)
    print("Learning Progress")
    print("=" * 80)
    progress = router.get_learning_progress()
    print(f"Total samples: {progress['total_samples']}")
    print(f"Learning enabled: {progress['learning_enabled']}")
    print(f"\nAccuracy progression:")
    for batch in progress['progression']:
        print(f"  Batch {batch['batch']}: {batch['accuracy']}%")
    
    print(f"\nTop keywords learned:")
    for kw, rate in progress['top_keywords'][:5]:
        print(f"  - {kw}: {rate:.1%} success")
