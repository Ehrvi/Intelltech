#!/usr/bin/env python3
"""
Continuous Learning Pipeline
Automatically learns and improves optimization strategies over time

Features:
- Collects optimization outcomes
- Trains models on historical data
- Updates thresholds automatically
- A/B testing for new strategies
- Performance tracking

Author: Manus AI
Date: 2026-02-16
"""

import json
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class ContinuousLearner:
    """
    Continuous learning system for cost optimization
    """
    
    def __init__(self, base_path: str = "/home/ubuntu/manus_global_knowledge"):
        """
        Initialize continuous learner
        
        Args:
            base_path: Base path for data storage
        """
        self.base_path = Path(base_path)
        self.data_dir = self.base_path / "learning_data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.outcomes_file = self.data_dir / "optimization_outcomes.jsonl"
        self.models_file = self.data_dir / "learned_models.json"
        
        # Configuration
        self.config = {
            'min_samples_for_learning': 100,  # Minimum samples before learning
            'retraining_interval_hours': 24,  # Retrain every 24 hours
            'learning_rate': 0.1,  # Learning rate for updates
            'exploration_rate': 0.1,  # 10% exploration (A/B testing)
        }
        
        # Load learned models
        self.models = self._load_models()
        
        # Statistics
        self.stats = {
            'total_outcomes': 0,
            'successful_optimizations': 0,
            'failed_optimizations': 0,
            'retrainings': 0,
            'last_retrain': None
        }
    
    def _load_models(self) -> Dict:
        """Load learned models from file"""
        if self.models_file.exists():
            try:
                with open(self.models_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                return self._initialize_models()
        return self._initialize_models()
    
    def _initialize_models(self) -> Dict:
        """Initialize default models"""
        return {
            'cache_thresholds': {
                # Operation -> (min_cost, max_cost) for caching
                'default': (0.0001, 1.0)
            },
            'compression_thresholds': {
                # Operation -> (min_tokens, max_tokens) for compression
                'default': (100, 10000)
            },
            'routing_confidence': {
                # Operation -> confidence threshold for routing
                'default': 0.7
            },
            'response_limits': {
                # Operation -> max_tokens for response
                'default': 500
            },
            'metadata': {
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'version': '1.0'
            }
        }
    
    def _save_models(self):
        """Save learned models to file"""
        self.models['metadata']['last_updated'] = datetime.now().isoformat()
        
        try:
            with open(self.models_file, 'w') as f:
                json.dump(self.models, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning: Failed to save models: {e}")
    
    def record_outcome(self, operation: str, optimization_type: str, 
                      success: bool, metrics: Dict):
        """
        Record an optimization outcome for learning
        
        Args:
            operation: Operation name
            optimization_type: Type of optimization (cache, compression, routing, etc.)
            success: Whether optimization was successful
            metrics: Metrics dict (cost, tokens, time, etc.)
        """
        outcome = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'type': optimization_type,
            'success': success,
            'metrics': metrics
        }
        
        # Append to outcomes file
        try:
            with open(self.outcomes_file, 'a') as f:
                f.write(json.dumps(outcome) + '\n')
        except Exception as e:
            print(f"⚠️ Warning: Failed to record outcome: {e}")
        
        # Update stats
        self.stats['total_outcomes'] += 1
        if success:
            self.stats['successful_optimizations'] += 1
        else:
            self.stats['failed_optimizations'] += 1
    
    def _load_recent_outcomes(self, hours: int = 24) -> List[Dict]:
        """
        Load recent optimization outcomes
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            List of outcomes
        """
        if not self.outcomes_file.exists():
            return []
        
        cutoff = datetime.now() - timedelta(hours=hours)
        outcomes = []
        
        try:
            with open(self.outcomes_file, 'r') as f:
                for line in f:
                    outcome = json.loads(line)
                    outcome_time = datetime.fromisoformat(outcome['timestamp'])
                    
                    if outcome_time > cutoff:
                        outcomes.append(outcome)
        except Exception as e:
            print(f"⚠️ Warning: Failed to load outcomes: {e}")
        
        return outcomes
    
    def should_retrain(self) -> bool:
        """
        Check if models should be retrained
        
        Returns:
            True if retraining is needed
        """
        # Check if enough samples
        outcomes = self._load_recent_outcomes(hours=self.config['retraining_interval_hours'])
        
        if len(outcomes) < self.config['min_samples_for_learning']:
            return False
        
        # Check if enough time has passed
        if self.stats['last_retrain']:
            last_retrain = datetime.fromisoformat(self.stats['last_retrain'])
            hours_since = (datetime.now() - last_retrain).total_seconds() / 3600
            
            if hours_since < self.config['retraining_interval_hours']:
                return False
        
        return True
    
    def retrain(self):
        """Retrain models based on recent outcomes"""
        print("Retraining models...")
        
        # Load recent outcomes
        outcomes = self._load_recent_outcomes(hours=self.config['retraining_interval_hours'] * 7)  # Use 1 week of data
        
        if len(outcomes) < self.config['min_samples_for_learning']:
            print(f"  ⚠️ Not enough samples ({len(outcomes)} < {self.config['min_samples_for_learning']})")
            return
        
        # Group by operation and type
        by_operation = defaultdict(lambda: defaultdict(list))
        
        for outcome in outcomes:
            op = outcome['operation']
            opt_type = outcome['type']
            by_operation[op][opt_type].append(outcome)
        
        # Learn cache thresholds
        self._learn_cache_thresholds(by_operation)
        
        # Learn compression thresholds
        self._learn_compression_thresholds(by_operation)
        
        # Learn routing confidence
        self._learn_routing_confidence(by_operation)
        
        # Learn response limits
        self._learn_response_limits(by_operation)
        
        # Save models
        self._save_models()
        
        # Update stats
        self.stats['retrainings'] += 1
        self.stats['last_retrain'] = datetime.now().isoformat()
        
        print(f"  ✅ Retrained with {len(outcomes)} samples")
    
    def _learn_cache_thresholds(self, by_operation: Dict):
        """Learn optimal cache thresholds"""
        for operation, by_type in by_operation.items():
            if 'cache' not in by_type:
                continue
            
            cache_outcomes = by_type['cache']
            
            # Calculate success rate by cost range
            costs = [o['metrics'].get('cost', 0) for o in cache_outcomes]
            successes = [o['success'] for o in cache_outcomes]
            
            if len(costs) < 10:
                continue
            
            # Find cost range where caching is most successful
            sorted_indices = np.argsort(costs)
            sorted_costs = [costs[i] for i in sorted_indices]
            sorted_successes = [successes[i] for i in sorted_indices]
            
            # Calculate moving average of success rate
            window = 10
            success_rates = []
            for i in range(len(sorted_costs) - window):
                rate = sum(sorted_successes[i:i+window]) / window
                success_rates.append(rate)
            
            if success_rates:
                # Find range where success rate > 0.8
                good_indices = [i for i, rate in enumerate(success_rates) if rate > 0.8]
                
                if good_indices:
                    min_cost = sorted_costs[good_indices[0]]
                    max_cost = sorted_costs[min(good_indices[-1] + window, len(sorted_costs) - 1)]
                    
                    # Update model
                    self.models['cache_thresholds'][operation] = (min_cost, max_cost)
    
    def _learn_compression_thresholds(self, by_operation: Dict):
        """Learn optimal compression thresholds"""
        for operation, by_type in by_operation.items():
            if 'compression' not in by_type:
                continue
            
            compression_outcomes = by_type['compression']
            
            # Calculate success rate by token count
            tokens = [o['metrics'].get('tokens', 0) for o in compression_outcomes]
            successes = [o['success'] for o in compression_outcomes]
            
            if len(tokens) < 10:
                continue
            
            # Find token range where compression is most successful
            sorted_indices = np.argsort(tokens)
            sorted_tokens = [tokens[i] for i in sorted_indices]
            sorted_successes = [successes[i] for i in sorted_indices]
            
            # Calculate moving average of success rate
            window = 10
            success_rates = []
            for i in range(len(sorted_tokens) - window):
                rate = sum(sorted_successes[i:i+window]) / window
                success_rates.append(rate)
            
            if success_rates:
                # Find range where success rate > 0.8
                good_indices = [i for i, rate in enumerate(success_rates) if rate > 0.8]
                
                if good_indices:
                    min_tokens = sorted_tokens[good_indices[0]]
                    max_tokens = sorted_tokens[min(good_indices[-1] + window, len(sorted_tokens) - 1)]
                    
                    # Update model
                    self.models['compression_thresholds'][operation] = (int(min_tokens), int(max_tokens))
    
    def _learn_routing_confidence(self, by_operation: Dict):
        """Learn optimal routing confidence thresholds"""
        for operation, by_type in by_operation.items():
            if 'routing' not in by_type:
                continue
            
            routing_outcomes = by_type['routing']
            
            # Calculate success rate
            total = len(routing_outcomes)
            successes = sum(1 for o in routing_outcomes if o['success'])
            success_rate = successes / total if total > 0 else 0
            
            if total < 10:
                continue
            
            # Adjust confidence threshold based on success rate
            current_threshold = self.models['routing_confidence'].get(operation, 0.7)
            
            if success_rate > 0.9:
                # High success rate - can lower threshold (route more)
                new_threshold = max(0.5, current_threshold - 0.05)
            elif success_rate < 0.7:
                # Low success rate - raise threshold (route less)
                new_threshold = min(0.9, current_threshold + 0.05)
            else:
                new_threshold = current_threshold
            
            self.models['routing_confidence'][operation] = new_threshold
    
    def _learn_response_limits(self, by_operation: Dict):
        """Learn optimal response token limits"""
        for operation, by_type in by_operation.items():
            if 'response_control' not in by_type:
                continue
            
            response_outcomes = by_type['response_control']
            
            # Calculate average tokens for successful responses
            successful = [o for o in response_outcomes if o['success']]
            
            if len(successful) < 10:
                continue
            
            tokens = [o['metrics'].get('tokens', 0) for o in successful]
            avg_tokens = int(np.mean(tokens))
            std_tokens = int(np.std(tokens))
            
            # Set limit to mean + 1 std dev
            limit = avg_tokens + std_tokens
            
            self.models['response_limits'][operation] = limit
    
    def get_cache_threshold(self, operation: str) -> Tuple[float, float]:
        """Get learned cache threshold for operation"""
        return self.models['cache_thresholds'].get(
            operation, 
            self.models['cache_thresholds']['default']
        )
    
    def get_compression_threshold(self, operation: str) -> Tuple[int, int]:
        """Get learned compression threshold for operation"""
        return self.models['compression_thresholds'].get(
            operation,
            self.models['compression_thresholds']['default']
        )
    
    def get_routing_confidence(self, operation: str) -> float:
        """Get learned routing confidence for operation"""
        return self.models['routing_confidence'].get(
            operation,
            self.models['routing_confidence']['default']
        )
    
    def get_response_limit(self, operation: str) -> int:
        """Get learned response limit for operation"""
        return self.models['response_limits'].get(
            operation,
            self.models['response_limits']['default']
        )
    
    def should_explore(self) -> bool:
        """
        Decide if should explore (A/B testing)
        
        Returns:
            True if should explore new strategies
        """
        return np.random.random() < self.config['exploration_rate']
    
    def get_stats(self) -> Dict:
        """Get learning statistics"""
        stats = self.stats.copy()
        
        if stats['total_outcomes'] > 0:
            stats['success_rate'] = (stats['successful_optimizations'] / 
                                    stats['total_outcomes'] * 100)
        else:
            stats['success_rate'] = 0
        
        stats['learned_operations'] = {
            'cache': len(self.models['cache_thresholds']) - 1,  # -1 for default
            'compression': len(self.models['compression_thresholds']) - 1,
            'routing': len(self.models['routing_confidence']) - 1,
            'response': len(self.models['response_limits']) - 1
        }
        
        return stats
    
    def print_stats(self):
        """Print learning statistics"""
        stats = self.get_stats()
        
        print("="*70)
        print("CONTINUOUS LEARNING STATISTICS")
        print("="*70)
        print(f"Total Outcomes:       {stats['total_outcomes']}")
        print(f"Successful:           {stats['successful_optimizations']}")
        print(f"Failed:               {stats['failed_optimizations']}")
        print(f"Success Rate:         {stats['success_rate']:.1f}%")
        print(f"Retrainings:          {stats['retrainings']}")
        print(f"Last Retrain:         {stats['last_retrain'] or 'Never'}")
        print()
        print("Learned Operations:")
        for opt_type, count in stats['learned_operations'].items():
            print(f"  {opt_type:15s} {count:3d} operations")
        print("="*70)


def main():
    """Test continuous learner"""
    learner = ContinuousLearner()
    
    print("Testing Continuous Learner...")
    print()
    
    # Simulate some outcomes
    print("Simulating outcomes...")
    for i in range(150):
        learner.record_outcome(
            operation='apollo_search',
            optimization_type='cache',
            success=np.random.random() > 0.2,  # 80% success rate
            metrics={'cost': np.random.uniform(0.001, 0.01), 'tokens': 100}
        )
    
    print(f"  Recorded {learner.stats['total_outcomes']} outcomes")
    print()
    
    # Check if should retrain
    print("Checking if should retrain...")
    if learner.should_retrain():
        print("  ✅ Retraining...")
        learner.retrain()
    else:
        print("  ⏭️  Not enough data yet")
    print()
    
    # Print stats
    learner.print_stats()


if __name__ == "__main__":
    main()
