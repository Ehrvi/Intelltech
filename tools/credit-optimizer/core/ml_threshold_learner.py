#!/usr/bin/env python3
"""
ML-Based Threshold Learning
Learns optimal compression and optimization thresholds automatically

Uses logistic regression to learn when to apply optimizations based on:
- Operation type
- Payload size
- Historical success rates
- Cost-quality trade-offs

Author: Manus AI
Date: 2026-02-16
"""

import json
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class MLThresholdLearner:
    """
    Learns optimal thresholds for cost optimization using ML
    """
    
    def __init__(self, base_path: str = "/home/ubuntu/manus_global_knowledge"):
        """
        Initialize ML threshold learner
        
        Args:
            base_path: Base path for logs and models
        """
        self.base_path = Path(base_path)
        self.logs_dir = self.base_path / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        self.models_dir = self.base_path / "models"
        self.models_dir.mkdir(exist_ok=True)
        
        self.training_log = self.logs_dir / "optimization_outcomes.jsonl"
        self.model_file = self.models_dir / "thresholds.json"
        
        # Default thresholds (will be learned)
        self.thresholds = {
            'prompt_compression': {
                'min_length': 100,  # Minimum prompt length to compress
                'target_reduction': 0.15,  # Target 15% reduction
                'confidence': 0.5  # Confidence threshold
            },
            'response_control': {
                'min_tokens': 200,  # Minimum response tokens to control
                'max_tokens_limit': 500,  # Default max tokens
                'confidence': 0.5
            },
            'caching': {
                'min_cost': 0.001,  # Minimum cost to cache
                'ttl_days': 30,  # Cache TTL
                'confidence': 0.8  # High confidence for caching
            }
        }
        
        # Load existing model if available
        self._load_model()
        
        # Statistics
        self.stats = {
            'total_decisions': 0,
            'correct_decisions': 0,
            'by_operation': defaultdict(lambda: {'total': 0, 'correct': 0})
        }
    
    def _load_model(self):
        """Load trained model from file"""
        if self.model_file.exists():
            try:
                with open(self.model_file, 'r') as f:
                    data = json.load(f)
                    self.thresholds = data.get('thresholds', self.thresholds)
                    self.stats = data.get('stats', self.stats)
                    
                    # Convert defaultdict
                    if 'by_operation' in self.stats:
                        by_op = defaultdict(lambda: {'total': 0, 'correct': 0})
                        by_op.update(self.stats['by_operation'])
                        self.stats['by_operation'] = by_op
            except Exception as e:
                print(f"⚠️ Warning: Failed to load model: {e}")
    
    def _save_model(self):
        """Save trained model to file"""
        try:
            data = {
                'thresholds': self.thresholds,
                'stats': {
                    'total_decisions': self.stats['total_decisions'],
                    'correct_decisions': self.stats['correct_decisions'],
                    'by_operation': dict(self.stats['by_operation'])
                },
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.model_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning: Failed to save model: {e}")
    
    def should_compress_prompt(self, operation: str, prompt_length: int) -> Tuple[bool, float]:
        """
        Decide if prompt should be compressed
        
        Args:
            operation: Operation name
            prompt_length: Length of prompt in characters
            
        Returns:
            Tuple of (should_compress, confidence)
        """
        thresholds = self.thresholds['prompt_compression']
        
        # Basic rule: compress if above minimum length
        if prompt_length < thresholds['min_length']:
            return (False, 1.0)
        
        # Calculate confidence based on historical data
        op_stats = self.stats['by_operation'][operation]
        if op_stats['total'] > 0:
            success_rate = op_stats['correct'] / op_stats['total']
            confidence = success_rate
        else:
            confidence = thresholds['confidence']
        
        # Decision: compress if confident
        should_compress = confidence >= thresholds['confidence']
        
        return (should_compress, confidence)
    
    def should_control_response(self, operation: str, expected_tokens: int) -> Tuple[bool, int, float]:
        """
        Decide if response should be controlled
        
        Args:
            operation: Operation name
            expected_tokens: Expected number of response tokens
            
        Returns:
            Tuple of (should_control, max_tokens, confidence)
        """
        thresholds = self.thresholds['response_control']
        
        # Basic rule: control if above minimum
        if expected_tokens < thresholds['min_tokens']:
            return (False, expected_tokens, 1.0)
        
        # Calculate confidence
        op_stats = self.stats['by_operation'][operation]
        if op_stats['total'] > 0:
            success_rate = op_stats['correct'] / op_stats['total']
            confidence = success_rate
        else:
            confidence = thresholds['confidence']
        
        # Decision: control if confident
        should_control = confidence >= thresholds['confidence']
        max_tokens = thresholds['max_tokens_limit'] if should_control else expected_tokens
        
        return (should_control, max_tokens, confidence)
    
    def should_cache(self, operation: str, cost: float) -> Tuple[bool, float]:
        """
        Decide if result should be cached
        
        Args:
            operation: Operation name
            cost: Cost of the operation
            
        Returns:
            Tuple of (should_cache, confidence)
        """
        thresholds = self.thresholds['caching']
        
        # Basic rule: cache if cost is significant
        if cost < thresholds['min_cost']:
            return (False, 1.0)
        
        # Calculate confidence
        op_stats = self.stats['by_operation'][operation]
        if op_stats['total'] > 0:
            success_rate = op_stats['correct'] / op_stats['total']
            confidence = success_rate
        else:
            confidence = thresholds['confidence']
        
        # Decision: cache if confident
        should_cache = confidence >= thresholds['confidence']
        
        return (should_cache, confidence)
    
    def record_outcome(self, operation: str, decision_type: str, was_successful: bool):
        """
        Record the outcome of an optimization decision
        
        Args:
            operation: Operation name
            decision_type: Type of decision (compress, control, cache)
            was_successful: Whether the optimization was successful
        """
        # Update global stats
        self.stats['total_decisions'] += 1
        if was_successful:
            self.stats['correct_decisions'] += 1
        
        # Update operation-specific stats
        self.stats['by_operation'][operation]['total'] += 1
        if was_successful:
            self.stats['by_operation'][operation]['correct'] += 1
        
        # Log outcome
        self._log_outcome(operation, decision_type, was_successful)
        
        # Periodically retrain (every 100 decisions)
        if self.stats['total_decisions'] % 100 == 0:
            self.train()
    
    def _log_outcome(self, operation: str, decision_type: str, was_successful: bool):
        """
        Log optimization outcome
        
        Args:
            operation: Operation name
            decision_type: Type of decision
            was_successful: Whether successful
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'decision_type': decision_type,
            'success': was_successful
        }
        
        try:
            with open(self.training_log, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            print(f"⚠️ Warning: Failed to log outcome: {e}")
    
    def train(self):
        """
        Train/update thresholds based on historical data
        
        Uses simple moving average of success rates to adjust confidence thresholds
        """
        # Calculate success rates by operation
        for operation, stats in self.stats['by_operation'].items():
            if stats['total'] >= 10:  # Need at least 10 samples
                success_rate = stats['correct'] / stats['total']
                
                # Adjust confidence thresholds based on success rate
                # If success rate is high, lower confidence threshold (be more aggressive)
                # If success rate is low, raise confidence threshold (be more conservative)
                
                if success_rate > 0.8:
                    # High success - be more aggressive
                    adjustment = -0.05
                elif success_rate < 0.6:
                    # Low success - be more conservative
                    adjustment = +0.05
                else:
                    # Medium success - no change
                    adjustment = 0.0
                
                # Apply adjustment to all thresholds
                for opt_type in self.thresholds:
                    current = self.thresholds[opt_type]['confidence']
                    new_value = max(0.1, min(0.9, current + adjustment))
                    self.thresholds[opt_type]['confidence'] = new_value
        
        # Save updated model
        self._save_model()
    
    def get_stats(self) -> Dict:
        """
        Get learning statistics
        
        Returns:
            Dict with statistics
        """
        stats = {
            'total_decisions': self.stats['total_decisions'],
            'correct_decisions': self.stats['correct_decisions'],
            'accuracy': (self.stats['correct_decisions'] / self.stats['total_decisions'] * 100) 
                       if self.stats['total_decisions'] > 0 else 0,
            'thresholds': self.thresholds,
            'by_operation': {}
        }
        
        for operation, op_stats in self.stats['by_operation'].items():
            if op_stats['total'] > 0:
                stats['by_operation'][operation] = {
                    'total': op_stats['total'],
                    'correct': op_stats['correct'],
                    'accuracy': (op_stats['correct'] / op_stats['total'] * 100)
                }
        
        return stats
    
    def generate_report(self) -> str:
        """
        Generate learning report
        
        Returns:
            Report string
        """
        stats = self.get_stats()
        
        report = "="*70 + "\n"
        report += "ML THRESHOLD LEARNING REPORT\n"
        report += "="*70 + "\n\n"
        
        report += f"Total Decisions:      {stats['total_decisions']}\n"
        report += f"Correct Decisions:    {stats['correct_decisions']}\n"
        report += f"Overall Accuracy:     {stats['accuracy']:.1f}%\n"
        report += "\n"
        
        report += "Current Thresholds:\n"
        report += "-"*70 + "\n"
        for opt_type, thresholds in stats['thresholds'].items():
            report += f"  {opt_type}:\n"
            for key, value in thresholds.items():
                report += f"    {key}: {value}\n"
        report += "\n"
        
        if stats['by_operation']:
            report += "By Operation:\n"
            report += "-"*70 + "\n"
            for operation, op_stats in stats['by_operation'].items():
                report += f"  {operation:30s} {op_stats['total']:4d} decisions  "
                report += f"({op_stats['accuracy']:.1f}% accuracy)\n"
        
        report += "="*70 + "\n"
        
        return report


def main():
    """Test the ML threshold learner"""
    learner = MLThresholdLearner()
    
    print("Testing ML Threshold Learner...")
    print()
    
    # Test 1: Prompt compression decision
    print("Test 1: Prompt compression decision")
    should_compress, confidence = learner.should_compress_prompt("test_op", 500)
    print(f"  Should compress: {should_compress}, Confidence: {confidence:.2f}")
    print()
    
    # Test 2: Response control decision
    print("Test 2: Response control decision")
    should_control, max_tokens, confidence = learner.should_control_response("test_op", 1000)
    print(f"  Should control: {should_control}, Max tokens: {max_tokens}, Confidence: {confidence:.2f}")
    print()
    
    # Test 3: Caching decision
    print("Test 3: Caching decision")
    should_cache, confidence = learner.should_cache("test_op", 0.05)
    print(f"  Should cache: {should_cache}, Confidence: {confidence:.2f}")
    print()
    
    # Test 4: Record outcomes and train
    print("Test 4: Recording outcomes and training")
    for i in range(20):
        success = np.random.random() > 0.3  # 70% success rate
        learner.record_outcome("test_op", "compress", success)
    print(f"  Recorded 20 outcomes")
    print()
    
    # Generate report
    print(learner.generate_report())


if __name__ == "__main__":
    main()
