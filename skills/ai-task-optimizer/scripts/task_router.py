#!/usr/bin/env python3
"""
AI Task Router - OPTIMIZED FOR MAXIMUM SAVINGS
Aggressive cost-saving strategy for intensive daily usage
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
    """Routes tasks to optimal provider - OPTIMIZED FOR SAVINGS"""
    
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
        time_sensitivity: int = 2,
        force_provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Route task to optimal provider
        
        Returns routing decision with provider and rationale
        """
        if force_provider:
            return {
                'provider': force_provider,
                'score': 0,
                'rationale': f'Forced to {force_provider}',
                'profile': {
                    'complexity': complexity,
                    'volume': volume,
                    'quality_sensitivity': quality_sensitivity,
                    'time_sensitivity': time_sensitivity
                }
            }
        
        profile = TaskProfile(complexity, volume, quality_sensitivity, time_sensitivity)
        score = profile.score()
        
        provider, rationale = self._decide_optimized(score, profile, task_description)
        
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
    
    def _decide_optimized(self, score: int, profile: TaskProfile, task: str) -> tuple[str, str]:
        """
        OPTIMIZED routing logic - AGGRESSIVE COST SAVINGS
        
        Philosophy: OpenAI by default, Manus only when absolutely necessary
        """
        
        # ONLY use Manus for truly critical cases
        
        # 1. Client-facing deliverables (proposals, presentations to clients)
        if profile.quality_sensitivity == 3 and profile.complexity >= 2:
            return 'manus', 'Client-facing deliverable requires premium quality'
        
        # 2. Highly complex strategic work (complexity 3 + not simple research)
        if profile.complexity == 3 and 'research' not in task.lower() and 'find' not in task.lower():
            return 'manus', 'Complex strategic work requires deep reasoning'
        
        # 3. Critical business decisions (high stakes)
        critical_keywords = ['strategy', 'roadmap', 'architecture', 'design system', 'business plan']
        if any(kw in task.lower() for kw in critical_keywords) and profile.quality_sensitivity >= 2:
            return 'manus', 'Strategic business decision requires premium analysis'
        
        # EVERYTHING ELSE → OpenAI (95%+ of tasks)
        
        # High volume always OpenAI
        if profile.volume >= 2:
            return 'openai', f'Volume processing (score {score}): OpenAI handles efficiently'
        
        # Simple tasks always OpenAI
        if profile.complexity == 1:
            return 'openai', f'Simple task (score {score}): OpenAI perfect for this'
        
        # Research, search, find → OpenAI
        research_keywords = ['research', 'find', 'search', 'list', 'extract', 'compare', 'review']
        if any(kw in task.lower() for kw in research_keywords):
            return 'openai', f'Research/information task (score {score}): OpenAI excellent quality'
        
        # Product recommendations, shopping → OpenAI
        shopping_keywords = ['buy', 'purchase', 'best', 'recommend', 'product', 'price']
        if any(kw in task.lower() for kw in shopping_keywords):
            return 'openai', f'Product/shopping research (score {score}): OpenAI handles well'
        
        # Content generation (not client-facing) → OpenAI
        if profile.quality_sensitivity <= 2:
            return 'openai', f'Internal content (score {score}): OpenAI quality sufficient'
        
        # Default: OpenAI for cost savings
        # Only go to Manus if score is very high (11-12) and quality critical
        if score >= 11 and profile.quality_sensitivity == 3:
            return 'manus', f'Very high score {score} + critical quality: Use Manus'
        
        return 'openai', f'Default to OpenAI (score {score}): Excellent quality at 99% savings'
    
    def analyze_task(self, task_description: str) -> Dict[str, int]:
        """
        Analyze task description to estimate profile
        OPTIMIZED: More aggressive in marking tasks as simple/low quality sensitivity
        """
        task_lower = task_description.lower()
        
        profile = {
            'complexity': 1,  # Default to simple (changed from 2)
            'volume': 1,
            'quality_sensitivity': 1,  # Default to low (changed from 2)
            'time_sensitivity': 2
        }
        
        # Complexity - be conservative, most tasks are simple or moderate
        if any(kw in task_lower for kw in ['strategy', 'roadmap', 'architecture', 'design system', 'business plan']):
            profile['complexity'] = 3
        elif any(kw in task_lower for kw in ['analyze', 'synthesize', 'compare', 'evaluate']):
            profile['complexity'] = 2
        # Everything else stays 1 (simple)
        
        # Volume
        if any(kw in task_lower for kw in ['all', 'every', 'batch', 'bulk', 'hundred', 'many']):
            profile['volume'] = 3
        elif any(kw in task_lower for kw in ['several', 'some', 'multiple']):
            profile['volume'] = 2
        
        # Quality sensitivity - only mark as high for explicit client-facing work
        if any(kw in task_lower for kw in ['client', 'proposal to', 'presentation to', 'pitch to']):
            profile['quality_sensitivity'] = 3
        elif any(kw in task_lower for kw in ['executive', 'board', 'stakeholder']):
            profile['quality_sensitivity'] = 2
        # Most tasks stay 1 (internal use)
        
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
    print("AI Task Router - OPTIMIZED FOR MAXIMUM SAVINGS\n")
    
    examples = [
        "Qual o melhor mandoline disponível na Austrália",
        "Pesquise 10 empresas de mineração",
        "Escreva proposta técnica para cliente BHP",
        "Encontre emails de 50 leads",
        "Crie estratégia de go-to-market para Austrália",
        "Compare preços de notebooks",
        "Analise dados de vendas do último trimestre",
    ]
    
    for task in examples:
        decision = route_task(task)
        savings = router.calculate_savings(decision['provider'], 200)
        print(f"Task: {task}")
        print(f"  → {decision['provider'].upper()} (score: {decision['score']})")
        print(f"  Rationale: {decision['rationale']}")
        print(f"  Savings: ${savings['saved_aud']:.4f} AUD ({savings['saved_percentage']:.1f}%)\n")
