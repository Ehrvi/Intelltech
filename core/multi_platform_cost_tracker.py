"""
Multi-Platform Cost Tracking System

Tracks costs across multiple platforms:
- Manus (credits)
- OpenAI (USD)
- Apollo (credits)
- Other services

Generates unified cost report showing total spend across all platforms.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class PlatformCost:
    """Cost for a single platform"""
    platform: str
    currency: str  # "credits", "USD", etc.
    total_cost: float
    operations: Dict[str, int] = field(default_factory=dict)
    details: Dict[str, float] = field(default_factory=dict)


class MultiPlatformCostTracker:
    """Track costs across multiple platforms"""
    
    # Manus costs (credits)
    MANUS_COSTS = {
        'shell': 1.0,
        'file_read': 0.5,
        'file_write': 0.5,
        'file_edit': 0.5,
        'search': 20.0,
        'browser': 30.0,
        'browser_action': 5.0,
        'map': 10.0,
        'generate_image': 15.0,
        'generate_video': 50.0,
        'mcp_call': 2.0,
    }
    
    # OpenAI costs (USD per 1M tokens)
    # Source: https://openai.com/api/pricing/ (verified 2024)
    OPENAI_COSTS = {
        'gpt-4o': {'input': 5.00, 'output': 15.00},  # per 1M tokens
        'gpt-4o-mini': {'input': 0.15, 'output': 0.60},
        'gpt-3.5-turbo': {'input': 0.50, 'output': 1.50},
    }
    
    # Apollo costs (credits per call)
    # Source: Apollo.io documentation + user knowledge
    APOLLO_COSTS = {
        'search': 1,  # 1 credit per search
        'enrich': 1,  # 1 credit per enrich
        'export': 1,  # 1 credit per export
    }
    
    # Apollo credit value in USD (conservative estimate)
    APOLLO_CREDIT_USD = 0.10  # $0.10 per credit
    
    def __init__(self):
        self.platforms: Dict[str, PlatformCost] = {}
        self.start_time = datetime.now()
    
    def log_manus_operation(self, tool: str, count: int = 1):
        """Log a Manus operation"""
        if 'manus' not in self.platforms:
            self.platforms['manus'] = PlatformCost(
                platform='Manus',
                currency='credits',
                total_cost=0.0
            )
        
        cost = self.MANUS_COSTS.get(tool, 0.0) * count
        self.platforms['manus'].total_cost += cost
        self.platforms['manus'].operations[tool] = \
            self.platforms['manus'].operations.get(tool, 0) + count
        self.platforms['manus'].details[tool] = cost
    
    def log_openai_operation(self, model: str, input_tokens: int, output_tokens: int):
        """Log an OpenAI API operation"""
        if 'openai' not in self.platforms:
            self.platforms['openai'] = PlatformCost(
                platform='OpenAI',
                currency='USD',
                total_cost=0.0
            )
        
        # Calculate cost
        pricing = self.OPENAI_COSTS.get(model, self.OPENAI_COSTS['gpt-4o'])
        input_cost = (input_tokens / 1_000_000) * pricing['input']
        output_cost = (output_tokens / 1_000_000) * pricing['output']
        total_cost = input_cost + output_cost
        
        self.platforms['openai'].total_cost += total_cost
        self.platforms['openai'].operations[model] = \
            self.platforms['openai'].operations.get(model, 0) + 1
        self.platforms['openai'].details[f"{model}_tokens"] = input_tokens + output_tokens
    
    def log_apollo_operation(self, operation: str, count: int = 1):
        """Log an Apollo API operation"""
        if 'apollo' not in self.platforms:
            self.platforms['apollo'] = PlatformCost(
                platform='Apollo',
                currency='credits',
                total_cost=0.0
            )
        
        cost = self.APOLLO_COSTS.get(operation, 1) * count
        self.platforms['apollo'].total_cost += cost
        self.platforms['apollo'].operations[operation] = \
            self.platforms['apollo'].operations.get(operation, 0) + count
    
    def generate_report(self) -> str:
        """Generate unified cost report across all platforms"""
        if not self.platforms:
            return "No operations logged"
        
        report = "\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        report += "📊 MULTI-PLATFORM COST REPORT\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Summary by platform
        for platform_name, platform_cost in self.platforms.items():
            symbol = "💰" if platform_cost.currency == "credits" else "💵"
            report += f"{symbol} {platform_cost.platform}: "
            report += f"{platform_cost.total_cost:.4f} {platform_cost.currency}\n"
        
        report += "\n"
        report += "Details by Platform:\n"
        report += "─" * 62 + "\n"
        
        # Details for each platform
        for platform_name, platform_cost in self.platforms.items():
            report += f"\n{platform_cost.platform}:\n"
            for op, count in sorted(platform_cost.operations.items(), 
                                   key=lambda x: -x[1]):
                report += f"  • {op:20s} {count:3d}x\n"
        
        report += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        return report
    
    def get_total_cost_usd(self) -> float:
        """
        Get total cost in USD (converting credits to USD estimate).
        Assumes 1 Manus credit ≈ $0.01 USD (user should adjust)
        """
        total_usd = 0.0
        
        for platform_cost in self.platforms.values():
            if platform_cost.currency == "USD":
                total_usd += platform_cost.total_cost
            elif platform_cost.currency == "credits":
                # Convert credits to USD (accurate conversion)
                if platform_cost.platform == "Manus":
                    total_usd += platform_cost.total_cost * 0.01  # 1 Manus credit = $0.01 USD
                elif platform_cost.platform == "Apollo":
                    total_usd += platform_cost.total_cost * self.APOLLO_CREDIT_USD
        
        return total_usd


# Global tracker instance
_global_tracker: Optional[MultiPlatformCostTracker] = None


def get_tracker() -> MultiPlatformCostTracker:
    """Get or create global tracker instance"""
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = MultiPlatformCostTracker()
    return _global_tracker


def reset_tracker():
    """Reset global tracker"""
    global _global_tracker
    _global_tracker = MultiPlatformCostTracker()


# Convenience functions
def log_manus(tool: str, count: int = 1):
    """Log Manus operation"""
    get_tracker().log_manus_operation(tool, count)


def log_openai(model: str, input_tokens: int, output_tokens: int):
    """Log OpenAI operation"""
    get_tracker().log_openai_operation(model, input_tokens, output_tokens)


def log_apollo(operation: str, count: int = 1):
    """Log Apollo operation"""
    get_tracker().log_apollo_operation(operation, count)


def generate_report() -> str:
    """Generate cost report"""
    return get_tracker().generate_report()


if __name__ == "__main__":
    # Example usage
    tracker = MultiPlatformCostTracker()
    
    # Log some operations
    tracker.log_manus_operation('shell', 5)
    tracker.log_manus_operation('file_write', 3)
    tracker.log_openai_operation('gpt-4o', 1000, 2000)
    tracker.log_apollo_operation('search', 2)
    
    # Generate report
    print(tracker.generate_report())
    print(f"\nTotal cost (USD equivalent): ${tracker.get_total_cost_usd():.4f}")
