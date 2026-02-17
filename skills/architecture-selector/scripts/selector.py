#!/usr/bin/env python3
"""
Architecture Selector - Automatic architecture selection for optimal task execution
"""

import json
import re
from typing import Dict, Any, Tuple
from datetime import datetime

class ArchitectureSelector:
    """
    Intelligent architecture selection system
    """
    
    def __init__(self):
        self.history_file = "/home/ubuntu/.architecture_selector_history.json"
        self.load_history()
    
    def load_history(self):
        """Load selection history for learning"""
        try:
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        except Exception as e:
            self.history = []
    
    def save_history(self):
        """Save selection history"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """
        Analyze task characteristics
        
        Returns scores for:
        - complexity (1-10)
        - volume (number of items)
        - criticality (1-10)
        - homogeneity (1-10)
        - time_sensitivity (1-10)
        """
        
        task_lower = task_description.lower()
        
        # Complexity analysis
        complexity_keywords = {
            'high': ['strategy', 'strategic', 'plan', 'analysis', 'complex', 'critical'],
            'medium': ['research', 'collect', 'analyze', 'classify', 'process'],
            'low': ['list', 'find', 'search', 'extract', 'simple']
        }
        
        complexity = 5  # default
        if any(kw in task_lower for kw in complexity_keywords['high']):
            complexity = 8
        elif any(kw in task_lower for kw in complexity_keywords['low']):
            complexity = 3
        
        # Volume analysis - check for numbers first
        volume = 1  # default
        
        # Try to extract number + unit (allow words in between)
        number_match = re.search(r'(\d+).*?(?:compan(?:y|ies)|items?|documents?|sources?|countries)', task_lower)
        if number_match:
            volume = int(number_match.group(1))
        elif re.search(r'thousands?', task_lower):
            volume = 1000
        elif re.search(r'hundreds?', task_lower):
            volume = 100

        
        # Criticality analysis
        criticality_keywords = {
            'critical': ['critical', 'important', 'essential', 'strategic', 'executive', 'client'],
            'moderate': ['useful', 'helpful', 'good to have'],
            'low': ['optional', 'nice to have', 'exploratory']
        }
        
        criticality = 6  # default
        if any(kw in task_lower for kw in criticality_keywords['critical']):
            criticality = 9
        elif any(kw in task_lower for kw in criticality_keywords['low']):
            criticality = 3
        
        # Homogeneity analysis
        homogeneity_keywords = ['each', 'every', 'all', 'same', 'similar', 'identical']
        homogeneity = 5  # default
        
        if any(kw in task_lower for kw in homogeneity_keywords):
            homogeneity = 8
        
        if 'different' in task_lower or 'various' in task_lower:
            homogeneity = 3
        
        # Time sensitivity
        time_keywords = {
            'urgent': ['urgent', 'asap', 'immediately', 'now', 'quick'],
            'moderate': ['soon', 'today', 'this week'],
            'low': ['eventually', 'when possible', 'no rush']
        }
        
        time_sensitivity = 5  # default
        if any(kw in task_lower for kw in time_keywords['urgent']):
            time_sensitivity = 9
        elif any(kw in task_lower for kw in time_keywords['low']):
            time_sensitivity = 2
        
        return {
            'complexity': complexity,
            'volume': volume,
            'criticality': criticality,
            'homogeneity': homogeneity,
            'time_sensitivity': time_sensitivity
        }
    
    def select_architecture(self, task_description: str, override: str = None, detailed: bool = False) -> Any:
        """
        Select optimal architecture for task
        
        Args:
            task_description: Natural language task description
            override: Force specific architecture (optional)
            detailed: Return detailed analysis (optional)
        
        Returns:
            Architecture name or detailed analysis dict
        """
        
        if override:
            return override
        
        # Analyze task
        scores = self.analyze_task(task_description)
        
        # Decision logic
        architecture, confidence, reasoning = self._decide_architecture(scores)
        
        if detailed:
            return {
                'recommended': architecture,
                'confidence': confidence,
                'scores': scores,
                'reasoning': reasoning,
                'alternatives': self._get_alternatives(scores, architecture),
                'cost_estimate': self._estimate_cost(architecture, scores['volume'])
            }
        
        return architecture
    
    def _decide_architecture(self, scores: Dict[str, Any]) -> Tuple[str, float, str]:
        """
        Core decision logic
        
        Returns: (architecture, confidence, reasoning)
        """
        
        complexity = scores['complexity']
        volume = scores['volume']
        criticality = scores['criticality']
        homogeneity = scores['homogeneity']
        time_sensitivity = scores['time_sensitivity']
        
        # Rule 1: Strategic/Critical → Direct Manus
        if criticality >= 8 and complexity >= 7:
            return (
                'direct_manus',
                0.95,
                f"High criticality ({criticality}/10) and complexity ({complexity}/10) require highest quality Direct Manus execution"
            )
        
        # Rule 2: High homogeneity + volume → Parallel Map
        if homogeneity >= 8 and volume >= 5:
            return (
                'parallel_map',
                0.90,
                f"Highly homogeneous task ({homogeneity}/10) with {volume} items is perfect for parallel processing"
            )
        
        # Rule 3: High volume + moderate complexity → Guardian
        if volume >= 50 and complexity >= 3 and complexity <= 7:
            return (
                'guardian',
                0.92,
                f"High volume ({volume} items) with moderate complexity ({complexity}/10) suits Guardian GPT workers"
            )
        
        # Rule 4: Multi-stage complexity → Hybrid
        if complexity >= 7 and volume >= 50 and criticality >= 7:
            return (
                'hybrid',
                0.88,
                f"Complex ({complexity}/10), high-volume ({volume}), critical ({criticality}/10) task benefits from hybrid approach"
            )
        
        # Default: Guardian (cost-effective general purpose)
        return (
            'guardian',
            0.75,
            f"General purpose task with moderate characteristics defaults to cost-effective Guardian"
        )
    
    def _get_alternatives(self, scores: Dict[str, Any], selected: str) -> list:
        """Get alternative architectures"""
        
        all_options = ['guardian', 'direct_manus', 'parallel_map', 'hybrid']
        alternatives = [opt for opt in all_options if opt != selected]
        
        return alternatives[:2]  # Top 2 alternatives
    
    def _estimate_cost(self, architecture: str, volume: int) -> str:
        """Estimate cost for architecture"""
        
        costs = {
            'guardian': volume * 0.0001,  # $0.0001 per item
            'direct_manus': volume * 0.01,  # 0.01 credits per item
            'parallel_map': volume * 0.005,  # 0.005 credits per item
            'hybrid': volume * 0.002  # Mixed cost
        }
        
        cost = costs.get(architecture, 0)
        
        if 'manus' in architecture or 'parallel' in architecture or 'hybrid' in architecture:
            return f"{cost:.2f} Manus credits"
        else:
            return f"${cost:.2f} USD"
    
    def record_outcome(self, task_id: str, selected_architecture: str, 
                      actual_cost: str, actual_quality: int, 
                      actual_time: str, user_satisfaction: int):
        """Record task outcome for learning"""
        
        outcome = {
            'task_id': task_id,
            'timestamp': datetime.now().isoformat(),
            'selected_architecture': selected_architecture,
            'actual_cost': actual_cost,
            'actual_quality': actual_quality,
            'actual_time': actual_time,
            'user_satisfaction': user_satisfaction
        }
        
        self.history.append(outcome)
        self.save_history()


def main():
    """CLI interface for architecture selection"""
    
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python selector.py <task_description>")
        print("       python selector.py --test")
        sys.exit(1)
    
    selector = ArchitectureSelector()
    
    if sys.argv[1] == '--test':
        # Run test cases
        test_cases = [
            "Create 5-year expansion strategy for IntellTech",
            "Collect 500 mining companies from Australia",
            "Research top 50 companies in each of 10 countries",
            "Research global mining market and create go-to-market strategy",
            "Expand Apollo database with 3000 mining companies"
        ]
        
        print("=" * 70)
        print("ARCHITECTURE SELECTOR - TEST CASES")
        print("=" * 70)
        
        for task in test_cases:
            print(f"\nTask: {task}")
            print("-" * 70)
            
            analysis = selector.select_architecture(task, detailed=True)
            
            print(f"Recommended: {analysis['recommended']}")
            print(f"Confidence: {analysis['confidence']:.0%}")
            print(f"Reasoning: {analysis['reasoning']}")
            print(f"Cost Estimate: {analysis['cost_estimate']}")
            print(f"Scores: {analysis['scores']}")
    
    else:
        # Analyze single task
        task = ' '.join(sys.argv[1:])
        
        analysis = selector.select_architecture(task, detailed=True)
        
        print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
