#!/usr/bin/env python3
"""
Unified Cost Optimizer
Consolidates optimized_api_wrapper.py and aggressive_cost_optimizer.py into a single, comprehensive system

Features:
- Caching (MD5-based with TTL)
- Template engine
- Prompt optimization
- Response control
- Statistics tracking
- Cost logging
- Drop-in replacement for requests.post()

Author: Manus AI
Date: 2026-02-16
"""

import os
import sys
import json
import hashlib
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple

# Add core directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from prompt_optimizer import PromptOptimizer
    from response_controller import ResponseController
    OPTIMIZATION_MODULES_AVAILABLE = True
except ImportError:
    OPTIMIZATION_MODULES_AVAILABLE = False
    print("⚠️ Warning: Optimization modules not found. Running with basic optimization.")


class UnifiedCostOptimizer:
    """
    Unified cost optimizer that combines caching, templates, prompt optimization,
    and response control into a single, easy-to-use system.
    """
    
    def __init__(self, enable_optimization: bool = None):
        """
        Initialize the unified optimizer
        
        Args:
            enable_optimization: Whether to enable optimization (defaults to env var)
        """
        if enable_optimization is None:
            enable_optimization = os.environ.get('ENABLE_COST_OPTIMIZATION', 'true').lower() == 'true'
        
        self.enable_optimization = enable_optimization
        
        # Setup paths
        self.base_path = Path("/home/ubuntu/manus_global_knowledge")
        self.cache_dir = self.base_path / ".cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        self.templates_dir = self.base_path / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        self.cost_log = self.base_path / "logs" / "cost_tracking.jsonl"
        self.cost_log.parent.mkdir(exist_ok=True)
        
        # Initialize optimization modules
        if self.enable_optimization and OPTIMIZATION_MODULES_AVAILABLE:
            self.prompt_optimizer = PromptOptimizer()
            self.response_controller = ResponseController()
        else:
            self.prompt_optimizer = None
            self.response_controller = None
        
        # Configuration
        self.config = {
            'cache_ttl_days': 30,
            'max_prompt_tokens': 500,
            'template_first': True,
            'enable_caching': True,
            'enable_templates': True,
            'enable_prompt_optimization': True,
            'enable_response_control': True
        }
        
        # Statistics tracking
        self.stats = {
            'total_calls': 0,
            'optimized_calls': 0,
            'cache_hits': 0,
            'template_uses': 0,
            'total_tokens_saved': 0,
            'total_cost_saved': 0.0,
            'by_endpoint': {}
        }
    
    # ==================== CACHING ====================
    
    def _generate_cache_key(self, data: str) -> str:
        """Generate MD5 hash for cache key"""
        return hashlib.md5(data.encode()).hexdigest()
    
    def check_cache(self, key: str, ttl_days: int = None) -> Tuple[bool, Any, str]:
        """
        Check if cached response exists and is valid
        
        Args:
            key: Cache key (will be hashed)
            ttl_days: Time to live in days (defaults to config)
            
        Returns:
            Tuple of (hit, data, message)
        """
        if not self.config['enable_caching']:
            return (False, None, "Caching disabled")
        
        if ttl_days is None:
            ttl_days = self.config['cache_ttl_days']
        
        cache_key = self._generate_cache_key(key)
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
            
            self.stats['cache_hits'] += 1
            return (True, cached['data'], f"Cache hit ({age_days} days old)")
        
        except Exception as e:
            return (False, None, f"Cache error: {e}")
    
    def save_cache(self, key: str, data: Any):
        """
        Save response to cache
        
        Args:
            key: Cache key (will be hashed)
            data: Data to cache
        """
        if not self.config['enable_caching']:
            return
        
        cache_key = self._generate_cache_key(key)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        cached = {
            'key': key,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(cached, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning: Failed to save cache: {e}")
    
    # ==================== TEMPLATES ====================
    
    def get_template(self, template_name: str) -> Optional[str]:
        """
        Get template if exists
        
        Args:
            template_name: Name of the template
            
        Returns:
            Template content or None
        """
        if not self.config['enable_templates']:
            return None
        
        template_file = self.templates_dir / f"{template_name}.md"
        
        if template_file.exists():
            self.stats['template_uses'] += 1
            return template_file.read_text()
        
        return None
    
    def save_template(self, template_name: str, content: str):
        """
        Save template for reuse
        
        Args:
            template_name: Name of the template
            content: Template content
        """
        if not self.config['enable_templates']:
            return
        
        template_file = self.templates_dir / f"{template_name}.md"
        
        try:
            template_file.write_text(content)
        except Exception as e:
            print(f"⚠️ Warning: Failed to save template: {e}")
    
    # ==================== OPTIMIZATION ====================
    
    def optimize_prompt(self, prompt: str) -> Tuple[str, int]:
        """
        Optimize prompt to reduce tokens
        
        Args:
            prompt: Original prompt
            
        Returns:
            Tuple of (optimized_prompt, tokens_saved)
        """
        if not self.config['enable_prompt_optimization']:
            return (prompt, 0)
        
        original_length = len(prompt)
        
        # Use PromptOptimizer if available
        if self.prompt_optimizer:
            optimized = prompt  # PromptOptimizer works on dict payloads
        else:
            # Basic optimization
            optimized = prompt.strip()
            optimized = ' '.join(optimized.split())
            
            # Remove redundant phrases
            redundant = ["please ", "could you ", "I would like you to ", "can you "]
            for phrase in redundant:
                optimized = optimized.replace(phrase, "")
        
        # Calculate tokens saved (rough estimate: 4 chars = 1 token)
        tokens_saved = (original_length - len(optimized)) // 4
        
        if tokens_saved > 0:
            self.stats['total_tokens_saved'] += tokens_saved
        
        return (optimized, tokens_saved)
    
    def optimize_payload(self, payload: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
        """
        Optimize API payload
        
        Args:
            payload: Original payload
            endpoint: API endpoint name
            
        Returns:
            Optimized payload
        """
        if not self.enable_optimization:
            return payload
        
        # Create a copy
        optimized = payload.copy()
        
        # Optimize text fields using PromptOptimizer
        if self.prompt_optimizer and self.config['enable_prompt_optimization']:
            optimized = self.prompt_optimizer.optimize_prompt_data(optimized)
        
        # Add response size limits if applicable
        if self.config['enable_response_control']:
            if 'max_tokens' not in optimized and endpoint in ['chat', 'completions', 'generate']:
                optimized['max_tokens'] = 500  # Conservative default
        
        return optimized
    
    # ==================== API WRAPPER ====================
    
    def post(self, url: str, operation: str = None, **kwargs) -> requests.Response:
        """
        Optimized POST request with caching, templates, and optimization
        
        Args:
            url: API endpoint URL
            operation: Operation name for templates and logging
            **kwargs: Same as requests.post()
            
        Returns:
            requests.Response object
        """
        self.stats['total_calls'] += 1
        
        # Extract endpoint name
        endpoint = self._extract_endpoint(url)
        if operation is None:
            operation = endpoint
        
        # Track by endpoint
        if endpoint not in self.stats['by_endpoint']:
            self.stats['by_endpoint'][endpoint] = {
                'calls': 0,
                'optimized': 0,
                'cache_hits': 0,
                'template_uses': 0
            }
        self.stats['by_endpoint'][endpoint]['calls'] += 1
        
        # Generate cache key from payload
        if 'json' in kwargs:
            cache_key = f"{url}:{json.dumps(kwargs['json'], sort_keys=True)}"
        else:
            cache_key = url
        
        # 1. Check cache first
        cache_hit, cached_data, cache_msg = self.check_cache(cache_key)
        if cache_hit:
            print(f"✅ {cache_msg}")
            self.stats['by_endpoint'][endpoint]['cache_hits'] += 1
            
            # Return a mock response with cached data
            response = requests.Response()
            response.status_code = 200
            response._content = json.dumps(cached_data).encode()
            
            # Log cost savings
            self.log_cost(operation, 0, 0, saved=0.05)
            
            return response
        
        # 2. Check template
        if self.config['template_first']:
            template = self.get_template(operation)
            if template:
                print(f"✅ Template exists for '{operation}' - Using template")
                self.stats['by_endpoint'][endpoint]['template_uses'] += 1
                
                # Return a mock response with template
                response = requests.Response()
                response.status_code = 200
                response._content = template.encode()
                
                # Log cost savings
                self.log_cost(operation, 0, 0, saved=0.10)
                
                return response
        
        # 3. Apply optimizations
        if self.enable_optimization and 'json' in kwargs:
            original_payload = kwargs['json']
            optimized_payload = self.optimize_payload(original_payload, endpoint)
            
            if optimized_payload != original_payload:
                kwargs['json'] = optimized_payload
                self.stats['optimized_calls'] += 1
                self.stats['by_endpoint'][endpoint]['optimized'] += 1
                
                # Estimate tokens saved
                original_size = len(json.dumps(original_payload))
                optimized_size = len(json.dumps(optimized_payload))
                tokens_saved = (original_size - optimized_size) // 4
                self.stats['total_tokens_saved'] += max(0, tokens_saved)
        
        # 4. Make the actual API call
        response = requests.post(url, **kwargs)
        
        # 5. Cache the response
        if response.status_code == 200:
            try:
                response_data = response.json()
                self.save_cache(cache_key, response_data)
            except Exception as e:
                pass  # Not JSON or error
        
        # 6. Log cost (estimate)
        estimated_tokens = len(response.text) // 4
        estimated_cost = estimated_tokens * 0.000003
        self.log_cost(operation, estimated_cost, estimated_tokens)
        
        return response
    
    def _extract_endpoint(self, url: str) -> str:
        """Extract endpoint name from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            path = parsed.path
            parts = [p for p in path.split('/') if p]
            if parts:
                return parts[-1]
            return 'unknown'
        except Exception as e:
            return 'unknown'
    
    # ==================== LOGGING ====================
    
    def log_cost(self, operation: str, cost: float, tokens: int, saved: float = 0):
        """
        Log cost for tracking
        
        Args:
            operation: Operation name
            cost: Cost in USD
            tokens: Number of tokens
            saved: Cost saved in USD
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'cost': cost,
            'tokens': tokens,
            'saved': saved
        }
        
        try:
            with open(self.cost_log, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"⚠️ Warning: Failed to log cost: {e}")
        
        if saved > 0:
            self.stats['total_cost_saved'] += saved
    
    def get_cost_stats(self, days: int = 7) -> Dict[str, Any]:
        """
        Get cost statistics from log
        
        Args:
            days: Number of days to look back
            
        Returns:
            Dict with cost statistics
        """
        if not self.cost_log.exists():
            return {'total_cost': 0, 'total_saved': 0, 'operations': 0, 'savings_rate': 0}
        
        cutoff = datetime.now() - timedelta(days=days)
        
        total_cost = 0
        total_saved = 0
        operations = 0
        
        try:
            with open(self.cost_log, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['timestamp'])
                    
                    if entry_time > cutoff:
                        total_cost += entry['cost']
                        total_saved += entry['saved']
                        operations += 1
        except Exception as e:
            print(f"⚠️ Warning: Failed to read cost log: {e}")
        
        return {
            'total_cost': total_cost,
            'total_saved': total_saved,
            'operations': operations,
            'savings_rate': (total_saved / (total_cost + total_saved) * 100) if (total_cost + total_saved) > 0 else 0
        }
    
    # ==================== STATISTICS ====================
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get optimization statistics
        
        Returns:
            Dict with statistics
        """
        stats = self.stats.copy()
        
        # Calculate rates
        if stats['total_calls'] > 0:
            stats['optimization_rate'] = stats['optimized_calls'] / stats['total_calls'] * 100
            stats['cache_hit_rate'] = stats['cache_hits'] / stats['total_calls'] * 100
        else:
            stats['optimization_rate'] = 0
            stats['cache_hit_rate'] = 0
        
        # Estimate cost savings (assuming $0.002 per 1K tokens)
        tokens_saved = stats['total_tokens_saved']
        stats['estimated_cost_savings_usd'] = (tokens_saved / 1000) * 0.002 + stats['total_cost_saved']
        
        # Add cost stats from log
        cost_stats = self.get_cost_stats(days=7)
        stats['cost_stats_7days'] = cost_stats
        
        return stats
    
    def print_stats(self):
        """Print optimization statistics"""
        stats = self.get_stats()
        
        print("="*70)
        print("UNIFIED COST OPTIMIZATION STATISTICS")
        print("="*70)
        print(f"Total API Calls:        {stats['total_calls']}")
        print(f"Optimized Calls:        {stats['optimized_calls']} ({stats['optimization_rate']:.1f}%)")
        print(f"Cache Hits:             {stats['cache_hits']} ({stats['cache_hit_rate']:.1f}%)")
        print(f"Template Uses:          {stats['template_uses']}")
        print(f"Tokens Saved (est):     {stats['total_tokens_saved']}")
        print(f"Cost Savings (est):     ${stats['estimated_cost_savings_usd']:.4f}")
        print()
        print("Cost Stats (Last 7 Days):")
        print("-"*70)
        cost_stats = stats['cost_stats_7days']
        print(f"  Total Cost:           ${cost_stats['total_cost']:.4f}")
        print(f"  Total Saved:          ${cost_stats['total_saved']:.4f}")
        print(f"  Operations:           {cost_stats['operations']}")
        print(f"  Savings Rate:         {cost_stats['savings_rate']:.1f}%")
        print()
        print("By Endpoint:")
        print("-"*70)
        for endpoint, data in stats['by_endpoint'].items():
            opt_rate = (data['optimized'] / data['calls'] * 100) if data['calls'] > 0 else 0
            cache_rate = (data['cache_hits'] / data['calls'] * 100) if data['calls'] > 0 else 0
            print(f"  {endpoint:20s} {data['calls']:4d} calls  "
                  f"({opt_rate:.0f}% opt, {cache_rate:.0f}% cached)")
        print("="*70)


# ==================== GLOBAL INSTANCE ====================

_global_optimizer = None


def get_optimizer() -> UnifiedCostOptimizer:
    """Get global optimizer instance (singleton)"""
    global _global_optimizer
    
    if _global_optimizer is None:
        _global_optimizer = UnifiedCostOptimizer()
    
    return _global_optimizer


def optimized_post(url: str, operation: str = None, **kwargs) -> requests.Response:
    """
    Optimized POST request (convenience function)
    
    Drop-in replacement for requests.post() with automatic optimizations
    
    Args:
        url: API endpoint URL
        operation: Operation name for templates and logging
        **kwargs: Same as requests.post()
        
    Returns:
        requests.Response object
        
    Example:
        # Before:
        response = requests.post(url, headers=headers, json=payload)
        
        # After:
        response = optimized_post(url, operation="search", headers=headers, json=payload)
    """
    optimizer = get_optimizer()
    return optimizer.post(url, operation=operation, **kwargs)


def print_optimization_stats():
    """Print optimization statistics (convenience function)"""
    optimizer = get_optimizer()
    optimizer.print_stats()


def get_optimization_stats() -> Dict[str, Any]:
    """Get optimization statistics (convenience function)"""
    optimizer = get_optimizer()
    return optimizer.get_stats()


# ==================== MAIN ====================

if __name__ == "__main__":
    print("="*70)
    print("UNIFIED COST OPTIMIZER - TEST")
    print("="*70)
    print()
    
    # Create optimizer
    optimizer = UnifiedCostOptimizer()
    
    # Test 1: Cache
    print("TEST 1: Caching")
    print("-"*70)
    
    test_key = "test_prompt_123"
    test_data = {"result": "This is a test response"}
    
    # Save to cache
    optimizer.save_cache(test_key, test_data)
    print("✓ Saved to cache")
    
    # Retrieve from cache
    hit, data, msg = optimizer.check_cache(test_key)
    print(f"✓ Cache check: {msg}")
    print(f"  Hit: {hit}, Data: {data}")
    print()
    
    # Test 2: Templates
    print("TEST 2: Templates")
    print("-"*70)
    
    template_name = "test_template"
    template_content = "# Test Template\n\nThis is a test template."
    
    # Save template
    optimizer.save_template(template_name, template_content)
    print("✓ Saved template")
    
    # Retrieve template
    retrieved = optimizer.get_template(template_name)
    print(f"✓ Retrieved template: {retrieved[:50]}...")
    print()
    
    # Test 3: Prompt Optimization
    print("TEST 3: Prompt Optimization")
    print("-"*70)
    
    test_prompt = "Please could you kindly provide a very detailed analysis"
    optimized, saved = optimizer.optimize_prompt(test_prompt)
    print(f"Original:  '{test_prompt}'")
    print(f"Optimized: '{optimized}'")
    print(f"Tokens saved: {saved}")
    print()
    
    # Test 4: Statistics
    print("TEST 4: Statistics")
    print("-"*70)
    
    # Simulate some calls
    optimizer.stats['total_calls'] = 100
    optimizer.stats['optimized_calls'] = 75
    optimizer.stats['cache_hits'] = 30
    optimizer.stats['template_uses'] = 10
    optimizer.stats['total_tokens_saved'] = 500
    optimizer.stats['by_endpoint'] = {
        'search': {'calls': 50, 'optimized': 40, 'cache_hits': 15, 'template_uses': 5},
        'enrich': {'calls': 30, 'optimized': 25, 'cache_hits': 10, 'template_uses': 3},
        'create': {'calls': 20, 'optimized': 10, 'cache_hits': 5, 'template_uses': 2}
    }
    
    optimizer.print_stats()
    
    print()
    print("="*70)
    print("✅ UNIFIED OPTIMIZER TEST COMPLETE")
    print("="*70)
