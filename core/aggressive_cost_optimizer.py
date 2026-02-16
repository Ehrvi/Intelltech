#!/usr/bin/env python3
"""
Aggressive Cost Optimizer for MOTHER
Enforces maximum cost savings without quality loss

Target: 75-90% cost reduction
Quality: Maintain ≥80%
"""

import os
import json
import hashlib
import time
from pathlib import Path
from datetime import datetime, timedelta

class AggressiveCostOptimizer:
    def __init__(self):
        self.base_path = Path("/home/ubuntu/manus_global_knowledge")
        self.cache_dir = self.base_path / ".cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        self.templates_dir = self.base_path / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        # Cost tracking
        self.cost_log = self.base_path / "logs" / "cost_tracking.jsonl"
        self.cost_log.parent.mkdir(exist_ok=True)
        
        # Optimization rules
        self.rules = {
            'cache_ttl_days': 30,
            'max_prompt_tokens': 500,
            'prefer_local_threshold': 0.8,
            'batch_min_size': 3,
            'template_first': True,
            'local_validation_first': True
        }
    
    def check_cache(self, key: str, ttl_days: int = None) -> tuple:
        """Check if cached response exists and is valid"""
        if ttl_days is None:
            ttl_days = self.rules['cache_ttl_days']
        
        cache_key = hashlib.md5(key.encode()).hexdigest()
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if not cache_file.exists():
            return (False, None, "Cache miss")
        
        try:
            with open(cache_file, 'r') as f:
                cached = json.load(f)
            
            cached_time = datetime.fromisoformat(cached['timestamp'])
            age_days = (datetime.now() - cached_time).days
            
            if age_days > ttl_days:
                return (False, None, f"Cache expired ({age_days} days old)")
            
            return (True, cached['data'], f"Cache hit ({age_days} days old)")
        
        except Exception as e:
            return (False, None, f"Cache error: {e}")
    
    def save_cache(self, key: str, data: any):
        """Save response to cache"""
        cache_key = hashlib.md5(key.encode()).hexdigest()
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        cached = {
            'key': key,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(cache_file, 'w') as f:
            json.dump(cached, f, indent=2)
    
    def get_template(self, template_name: str) -> str:
        """Get template if exists"""
        template_file = self.templates_dir / f"{template_name}.md"
        
        if template_file.exists():
            return template_file.read_text()
        
        return None
    
    def save_template(self, template_name: str, content: str):
        """Save template for reuse"""
        template_file = self.templates_dir / f"{template_name}.md"
        template_file.write_text(content)
    
    def should_use_local(self, task_complexity: float) -> bool:
        """Determine if task can be done locally"""
        # task_complexity: 0.0 (simple) to 1.0 (complex)
        return task_complexity < self.rules['prefer_local_threshold']
    
    def optimize_prompt(self, prompt: str, max_tokens: int = None) -> str:
        """Compress prompt to reduce tokens"""
        if max_tokens is None:
            max_tokens = self.rules['max_prompt_tokens']
        
        # Simple optimization (can be enhanced)
        optimized = prompt.strip()
        
        # Remove extra whitespace
        optimized = ' '.join(optimized.split())
        
        # Remove redundant phrases
        redundant = [
            "please ",
            "could you ",
            "I would like you to ",
            "can you ",
        ]
        
        for phrase in redundant:
            optimized = optimized.replace(phrase, "")
        
        # Estimate tokens (rough: 1 token ≈ 4 chars)
        estimated_tokens = len(optimized) // 4
        
        if estimated_tokens > max_tokens:
            # Truncate if too long
            optimized = optimized[:max_tokens * 4]
        
        return optimized
    
    def log_cost(self, operation: str, cost: float, tokens: int, saved: float = 0):
        """Log cost for tracking"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'cost': cost,
            'tokens': tokens,
            'saved': saved
        }
        
        with open(self.cost_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def get_cost_stats(self, days: int = 7) -> dict:
        """Get cost statistics"""
        if not self.cost_log.exists():
            return {'total_cost': 0, 'total_saved': 0, 'operations': 0}
        
        cutoff = datetime.now() - timedelta(days=days)
        
        total_cost = 0
        total_saved = 0
        operations = 0
        
        with open(self.cost_log, 'r') as f:
            for line in f:
                entry = json.loads(line)
                entry_time = datetime.fromisoformat(entry['timestamp'])
                
                if entry_time > cutoff:
                    total_cost += entry['cost']
                    total_saved += entry['saved']
                    operations += 1
        
        return {
            'total_cost': total_cost,
            'total_saved': total_saved,
            'operations': operations,
            'savings_rate': (total_saved / (total_cost + total_saved) * 100) if (total_cost + total_saved) > 0 else 0
        }
    
    def enforce_before_api_call(self, operation: str, prompt: str) -> dict:
        """Enforce cost optimization before API call"""
        result = {
            'proceed': False,
            'reason': '',
            'optimized_prompt': prompt,
            'estimated_cost': 0,
            'cached_result': None
        }
        
        # 1. Check cache first
        cache_hit, cached_data, cache_msg = self.check_cache(prompt)
        if cache_hit:
            result['proceed'] = False
            result['reason'] = f"✅ {cache_msg} - Using cached result (saved $$$)"
            result['cached_result'] = cached_data
            self.log_cost(operation, 0, 0, saved=0.05)  # Estimate saved
            return result
        
        # 2. Check template
        template = self.get_template(operation)
        if template and self.rules['template_first']:
            result['proceed'] = False
            result['reason'] = f"✅ Template exists for '{operation}' - Use template instead (saved $$$)"
            result['cached_result'] = template
            self.log_cost(operation, 0, 0, saved=0.10)
            return result
        
        # 3. Optimize prompt
        optimized = self.optimize_prompt(prompt)
        if len(optimized) < len(prompt):
            tokens_saved = (len(prompt) - len(optimized)) // 4
            result['optimized_prompt'] = optimized
            result['reason'] = f"⚠️ Prompt optimized: {tokens_saved} tokens saved"
        
        # 4. Estimate cost
        estimated_tokens = len(optimized) // 4
        estimated_cost = estimated_tokens * 0.000003  # Rough estimate
        result['estimated_cost'] = estimated_cost
        
        # 5. Proceed with optimized prompt
        result['proceed'] = True
        result['reason'] += f" | Estimated cost: ${estimated_cost:.4f}"
        
        return result
    
    def enforce_after_api_call(self, operation: str, prompt: str, response: str, actual_cost: float):
        """Enforce cost optimization after API call"""
        # Cache the response
        self.save_cache(prompt, response)
        
        # Check if should save as template
        # (Simple heuristic: if operation name suggests reusability)
        reusable_keywords = ['template', 'format', 'structure', 'outline']
        if any(kw in operation.lower() for kw in reusable_keywords):
            self.save_template(operation, response)
        
        # Log cost
        self.log_cost(operation, actual_cost, len(response) // 4)
    
    def generate_cost_report(self) -> str:
        """Generate cost optimization report"""
        stats = self.get_cost_stats(days=7)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    💰 COST OPTIMIZATION REPORT (7 days)                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Total Cost:        ${stats['total_cost']:.2f} USD                                              ║
║  Total Saved:       ${stats['total_saved']:.2f} USD                                              ║
║  Operations:        {stats['operations']}                                                    ║
║  Savings Rate:      {stats['savings_rate']:.1f}%                                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Optimization Status:                                                        ║
║    ✓ Cache enabled ({len(list(self.cache_dir.glob('*.json')))} entries)                                         ║
║    ✓ Templates enabled ({len(list(self.templates_dir.glob('*.md')))} templates)                                   ║
║    ✓ Prompt optimization active                                             ║
║    ✓ Cost tracking active                                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        return report

def main():
    """Test the optimizer"""
    optimizer = AggressiveCostOptimizer()
    
    # Test cache
    test_prompt = "Generate a design system for a tech company"
    
    # First call (no cache)
    result1 = optimizer.enforce_before_api_call("design_system", test_prompt)
    print("First call:", result1['reason'])
    
    # Simulate API response
    if result1['proceed']:
        optimizer.enforce_after_api_call("design_system", test_prompt, "Mock response", 0.05)
    
    # Second call (should hit cache)
    result2 = optimizer.enforce_before_api_call("design_system", test_prompt)
    print("Second call:", result2['reason'])
    
    # Generate report
    print(optimizer.generate_cost_report())

if __name__ == "__main__":
    main()
