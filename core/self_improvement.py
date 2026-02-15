#!/usr/bin/env python3
"""
Self-Improvement System for Cost Optimization
Learns from actual cost data and automatically improves decision-making.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class DecisionPattern:
    """Pattern of decision-making"""
    situation: str
    tool_chosen: str
    cost: float
    quality: float
    frequency: int
    last_seen: str


class SelfImprovementEngine:
    """Learns from cost data and improves decision-making"""
    
    def __init__(self, base_path: Path = Path("/home/ubuntu/manus_global_knowledge")):
        self.base_path = base_path
        self.logs_dir = base_path / "logs"
        self.learning_dir = base_path / "learning"
        self.learning_dir.mkdir(exist_ok=True)
        
        self.patterns_file = self.learning_dir / "decision_patterns.json"
        self.improvements_file = self.learning_dir / "improvements.json"
        self.rules_file = self.learning_dir / "learned_rules.json"
        
        self.patterns = self._load_patterns()
        self.rules = self._load_rules()
    
    def _load_patterns(self) -> Dict:
        """Load learned patterns"""
        if self.patterns_file.exists():
            with open(self.patterns_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_patterns(self):
        """Save learned patterns"""
        with open(self.patterns_file, 'w') as f:
            json.dump(self.patterns, f, indent=2)
    
    def _load_rules(self) -> List[Dict]:
        """Load learned rules"""
        if self.rules_file.exists():
            with open(self.rules_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_rules(self):
        """Save learned rules"""
        with open(self.rules_file, 'w') as f:
            json.dump(self.rules, f, indent=2)
    
    def analyze_operations(self, days: int = 7) -> Dict:
        """Analyze operations from last N days"""
        operations_log = self.logs_dir / "operations.jsonl"
        if not operations_log.exists():
            return {'error': 'No operations log found'}
        
        cutoff = datetime.now() - timedelta(days=days)
        operations = []
        
        with open(operations_log, 'r') as f:
            for line in f:
                try:
                    op = json.loads(line)
                    op_time = datetime.fromisoformat(op['timestamp'])
                    if op_time > cutoff:
                        operations.append(op)
                except:
                    continue
        
        return self._analyze_operation_list(operations)
    
    def _analyze_operation_list(self, operations: List[Dict]) -> Dict:
        """Analyze list of operations"""
        analysis = {
            'total_operations': len(operations),
            'total_cost': 0.0,
            'total_savings': 0.0,
            'tool_usage': defaultdict(lambda: {'count': 0, 'cost': 0, 'savings': 0}),
            'wasteful_patterns': [],
            'efficient_patterns': [],
            'improvement_opportunities': []
        }
        
        for op in operations:
            tool = op.get('tool', 'unknown')
            cost = op.get('cost_credits', 0)
            savings = op.get('savings_credits', 0)
            
            analysis['total_cost'] += cost
            analysis['total_savings'] += savings
            analysis['tool_usage'][tool]['count'] += 1
            analysis['tool_usage'][tool]['cost'] += cost
            analysis['tool_usage'][tool]['savings'] += savings
        
        # Identify wasteful patterns
        for tool, data in analysis['tool_usage'].items():
            if tool == 'search' and data['count'] > 0:
                analysis['wasteful_patterns'].append({
                    'pattern': f"Using 'search' {data['count']} times",
                    'cost': data['cost'],
                    'recommendation': "Use OpenAI instead (20,000x cheaper)",
                    'potential_savings': data['cost'] * 0.99995
                })
            
            if tool == 'browser' and data['count'] > 10:
                analysis['wasteful_patterns'].append({
                    'pattern': f"High browser usage ({data['count']} times)",
                    'cost': data['cost'],
                    'recommendation': "Consider if APIs can replace some browser operations",
                    'potential_savings': data['cost'] * 0.5
                })
        
        # Identify efficient patterns
        for tool, data in analysis['tool_usage'].items():
            if tool == 'openai' and data['savings'] > 0:
                analysis['efficient_patterns'].append({
                    'pattern': f"Using OpenAI {data['count']} times",
                    'savings': data['savings'],
                    'recommendation': "Continue this pattern"
                })
        
        return analysis
    
    def learn_from_operations(self) -> Dict:
        """Learn from recent operations and update rules"""
        analysis = self.analyze_operations(days=7)
        
        improvements = {
            'timestamp': datetime.now().isoformat(),
            'new_rules': [],
            'updated_rules': [],
            'insights': []
        }
        
        # Learn from wasteful patterns
        for pattern in analysis.get('wasteful_patterns', []):
            if 'search' in pattern['pattern']:
                rule = {
                    'id': 'avoid_search',
                    'condition': 'task_type == "research"',
                    'action': 'use_openai_instead',
                    'reason': f"Learned: search costs {pattern['cost']:.2f} credits, OpenAI costs 0.001",
                    'confidence': 0.95,
                    'created': datetime.now().isoformat()
                }
                
                if not any(r['id'] == 'avoid_search' for r in self.rules):
                    self.rules.append(rule)
                    improvements['new_rules'].append(rule)
        
        # Learn from efficient patterns
        for pattern in analysis.get('efficient_patterns', []):
            improvements['insights'].append({
                'type': 'efficient_pattern',
                'description': pattern['pattern'],
                'savings': pattern['savings'],
                'action': 'reinforce'
            })
        
        # Calculate savings rate and adjust thresholds
        total_cost = analysis.get('total_cost', 0)
        total_savings = analysis.get('total_savings', 0)
        if total_cost + total_savings > 0:
            savings_rate = (total_savings / (total_cost + total_savings)) * 100
            
            if savings_rate < 50:
                improvements['insights'].append({
                    'type': 'low_savings_rate',
                    'value': savings_rate,
                    'action': 'increase_openai_usage',
                    'recommendation': 'Review all operations and route more to OpenAI'
                })
            elif savings_rate > 80:
                improvements['insights'].append({
                    'type': 'high_savings_rate',
                    'value': savings_rate,
                    'action': 'maintain_current_strategy',
                    'recommendation': 'Current optimization is working well'
                })
        
        # Save improvements
        self._save_rules()
        with open(self.improvements_file, 'a') as f:
            f.write(json.dumps(improvements) + '\n')
        
        return improvements
    
    def get_recommendations(self) -> List[str]:
        """Get actionable recommendations based on learned patterns"""
        recommendations = []
        
        analysis = self.analyze_operations(days=7)
        
        # Check for wasteful patterns
        for pattern in analysis.get('wasteful_patterns', []):
            recommendations.append(
                f"⚠️ {pattern['pattern']}: {pattern['recommendation']} "
                f"(save {pattern['potential_savings']:.2f} credits)"
            )
        
        # Check savings rate
        total_cost = analysis.get('total_cost', 0)
        total_savings = analysis.get('total_savings', 0)
        if total_cost + total_savings > 0:
            savings_rate = (total_savings / (total_cost + total_savings)) * 100
            
            if savings_rate < 50:
                recommendations.append(
                    f"🚨 Savings rate is {savings_rate:.1f}% (target: 75%+). "
                    f"Use OpenAI for more tasks."
                )
            elif savings_rate >= 75:
                recommendations.append(
                    f"✅ Savings rate is {savings_rate:.1f}%. Excellent optimization!"
                )
        
        # Tool-specific recommendations
        tool_usage = analysis.get('tool_usage', {})
        
        if 'search' in tool_usage and tool_usage['search']['count'] > 0:
            recommendations.append(
                "💡 Replace 'search' with OpenAI API for 99.995% cost reduction"
            )
        
        if 'openai' in tool_usage:
            openai_count = tool_usage['openai']['count']
            total_ops = analysis['total_operations']
            openai_rate = (openai_count / total_ops * 100) if total_ops > 0 else 0
            
            if openai_rate < 70:
                recommendations.append(
                    f"📊 OpenAI usage is {openai_rate:.0f}% (target: 90%). "
                    f"Route more tasks to OpenAI."
                )
        
        return recommendations
    
    def generate_learning_report(self) -> str:
        """Generate report on what the system has learned"""
        analysis = self.analyze_operations(days=7)
        improvements = self.learn_from_operations()
        recommendations = self.get_recommendations()
        
        lines = []
        lines.append("=" * 70)
        lines.append("🧠 SELF-IMPROVEMENT REPORT")
        lines.append("=" * 70)
        lines.append("")
        
        # Summary
        lines.append("📊 Analysis (Last 7 Days):")
        lines.append(f"  Total Operations: {analysis['total_operations']}")
        lines.append(f"  Total Cost: {analysis['total_cost']:.2f} credits")
        lines.append(f"  Total Savings: {analysis['total_savings']:.2f} credits")
        
        total = analysis['total_cost'] + analysis['total_savings']
        if total > 0:
            savings_rate = (analysis['total_savings'] / total) * 100
            lines.append(f"  Savings Rate: {savings_rate:.1f}%")
        lines.append("")
        
        # New rules learned
        if improvements['new_rules']:
            lines.append("🆕 New Rules Learned:")
            for rule in improvements['new_rules']:
                lines.append(f"  • {rule['id']}: {rule['reason']}")
            lines.append("")
        
        # Insights
        if improvements['insights']:
            lines.append("💡 Insights:")
            for insight in improvements['insights']:
                lines.append(f"  • {insight['type']}: {insight.get('action', 'N/A')}")
            lines.append("")
        
        # Recommendations
        if recommendations:
            lines.append("🎯 Recommendations:")
            for rec in recommendations:
                lines.append(f"  {rec}")
            lines.append("")
        
        # Learned rules summary
        lines.append(f"📚 Total Rules Learned: {len(self.rules)}")
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)


# Global engine instance
_engine: Optional[SelfImprovementEngine] = None


def get_engine() -> SelfImprovementEngine:
    """Get global self-improvement engine"""
    global _engine
    if _engine is None:
        _engine = SelfImprovementEngine()
    return _engine


def learn_and_improve() -> str:
    """Run learning cycle and return report"""
    engine = get_engine()
    return engine.generate_learning_report()


def get_recommendations() -> List[str]:
    """Get current recommendations"""
    engine = get_engine()
    return engine.get_recommendations()


if __name__ == '__main__':
    # Demo
    engine = SelfImprovementEngine()
    print(engine.generate_learning_report())
