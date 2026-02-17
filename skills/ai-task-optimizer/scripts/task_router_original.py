#!/usr/bin/env python3
"""
AI Task Router
Intelligent routing of tasks to optimal AI provider (OpenAI vs Manus)
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class TaskProfile:
    """Task characteristics for routing decision"""
    complexity: int  # 1=simple, 2=moderate, 3=complex
    volume: int  # 1=low (1-10), 2=medium (11-100), 3=high (100+)
    quality_sensitivity: int  # 1=low, 2=medium, 3=high
    time_sensitivity: int  # 1=low, 2=medium, 3=high
    
    def score(self) -> int:
        return self.complexity + self.volume + self.quality_sensitivity + self.time_sensitivity


class TaskRouter:
    """Routes tasks to optimal provider based on characteristics"""
    
    # Cost per 1000 tokens/operations (AUD)
    COSTS = {
        'openai': 0.0002,  # ~$0.15 per 1M tokens
        'manus': 0.50      # Manus credits
    }
    
    def __init__(self):
        self.stats = {
            'openai': {'count': 0, 'tokens': 0},
            'manus': {'count': 0, 'tokens': 0}
        }
    
    def route(
        self,
        task_description: str,
        complexity: int = 2,
        volume: int = 1,
        quality_sensitivity: int = 2,
        time_sensitivity: int = 2
    ) -> Dict[str, Any]:
        """
        Route task to optimal provider
        
        Returns routing decision with provider and rationale
        """
        profile = TaskProfile(complexity, volume, quality_sensitivity, time_sensitivity)
        score = profile.score()
        
        provider, rationale = self._decide(score, profile, task_description)
        
        return {
            'provider': provider,
            'score': score,
            'rationale': rationale,
            'profile': {
                'complexity': complexity,
                'volume': volume,
                'quality_sensitivity': quality_sensitivity,
                'time_sensitivity': time_sensitivity
            }
        }
    
    def _decide(self, score: int, profile: TaskProfile, task: str) -> tuple[str, str]:
        """Internal routing logic"""
        
        # High quality sensitivity always uses Manus
        if profile.quality_sensitivity == 3:
            return 'manus', 'High quality sensitivity requires Manus'
        
        # High complexity always uses Manus
        if profile.complexity == 3:
            return 'manus', 'High complexity requires strategic thinking'
        
        # Score-based routing
        if score <= 6:
            return 'openai', f'Score {score}: Bulk processing suitable for OpenAI'
        elif score == 7:
            if profile.volume == 3:
                return 'openai', f'Score {score}: High volume, use OpenAI for efficiency'
            else:
                return 'manus', f'Score {score}: Use Manus for quality'
        elif score == 8:
            if profile.volume >= 2:
                return 'openai', f'Score {score}: Medium-high volume, OpenAI acceptable'
            else:
                return 'manus', f'Score {score}: Low volume, use Manus'
        else:  # score >= 9
            return 'manus', f'Score {score}: Strategic/high-value work requires Manus'
    
    def analyze_task(self, task_description: str) -> Dict[str, int]:
        """
        Analyze task description to estimate profile
        Returns suggested complexity, volume, quality_sensitivity, time_sensitivity
        """
        task_lower = task_description.lower()
        
        profile = {
            'complexity': 2,
            'volume': 1,
            'quality_sensitivity': 2,
            'time_sensitivity': 2
        }
        
        # Complexity
        if any(kw in task_lower for kw in ['strategy', 'design', 'create', 'develop', 'proposal']):
            profile['complexity'] = 3
        elif any(kw in task_lower for kw in ['find', 'search', 'list', 'extract', 'classify']):
            profile['complexity'] = 1
        
        # Volume
        if any(kw in task_lower for kw in ['all', 'every', 'batch', 'bulk', 'hundred', 'many']):
            profile['volume'] = 3
        elif any(kw in task_lower for kw in ['several', 'some']):
            profile['volume'] = 2
        
        # Quality sensitivity
        if any(kw in task_lower for kw in ['client', 'proposal', 'presentation', 'executive']):
            profile['quality_sensitivity'] = 3
        elif any(kw in task_lower for kw in ['draft', 'quick', 'rough', 'internal']):
            profile['quality_sensitivity'] = 1
        
        # Time sensitivity
        if any(kw in task_lower for kw in ['urgent', 'asap', 'now', 'immediately']):
            profile['time_sensitivity'] = 3
        elif any(kw in task_lower for kw in ['when you can', 'no rush']):
            profile['time_sensitivity'] = 1
        
        return profile
    
    def calculate_savings(self, provider: str, tokens: int = 200) -> Dict[str, float]:
        """Calculate cost savings vs all-Manus approach"""
        manus_cost = (tokens / 1000) * self.COSTS['manus']
        
        if provider == 'openai':
            actual_cost = (tokens / 1000) * self.COSTS['openai']
        else:
            actual_cost = manus_cost
        
        savings = manus_cost - actual_cost
        savings_pct = (savings / manus_cost * 100) if manus_cost > 0 else 0
        
        return {
            'manus_cost_aud': round(manus_cost, 4),
            'actual_cost_aud': round(actual_cost, 4),
            'saved_aud': round(savings, 4),
            'saved_percentage': round(savings_pct, 1)
        }
    
    def update_stats(self, provider: str, tokens: int):
        """Update routing statistics"""
        self.stats[provider]['count'] += 1
        self.stats[provider]['tokens'] += tokens
    
    def get_stats(self) -> Dict[str, Any]:
        """Get routing statistics"""
        total_tasks = sum(s['count'] for s in self.stats.values())
        total_tokens = sum(s['tokens'] for s in self.stats.values())
        
        if total_tasks == 0:
            return {'message': 'No tasks routed yet'}
        
        # Calculate total savings
        all_manus_cost = (total_tokens / 1000) * self.COSTS['manus']
        actual_cost = (
            (self.stats['openai']['tokens'] / 1000) * self.COSTS['openai'] +
            (self.stats['manus']['tokens'] / 1000) * self.COSTS['manus']
        )
        
        return {
            'total_tasks': total_tasks,
            'openai_tasks': self.stats['openai']['count'],
            'manus_tasks': self.stats['manus']['count'],
            'total_savings_aud': round(all_manus_cost - actual_cost, 2),
            'savings_percentage': round((all_manus_cost - actual_cost) / all_manus_cost * 100, 1)
        }


# Global instance
router = TaskRouter()


# Simple interface
def route_task(task: str, **kwargs) -> Dict[str, Any]:
    """Route a task with automatic or manual profile"""
    if not any(k in kwargs for k in ['complexity', 'volume', 'quality_sensitivity', 'time_sensitivity']):
        # Auto-analyze
        profile = router.analyze_task(task)
        kwargs.update(profile)
    
    return router.route(task, **kwargs)


def get_stats() -> Dict[str, Any]:
    """Get routing statistics"""
    return router.get_stats()


if __name__ == "__main__":
    # Test examples
    print("AI Task Router - Examples\n")
    
    examples = [
        "Qualify 100 leads as HOT/WARM/COLD",
        "Create strategic proposal for BHP Mining",
        "Extract emails from these 50 profiles",
        "Develop go-to-market strategy for Australia"
    ]
    
    for task in examples:
        decision = route_task(task)
        print(f"Task: {task}")
        print(f"  → {decision['provider'].upper()} (score: {decision['score']})")
        print(f"  Rationale: {decision['rationale']}\n")
