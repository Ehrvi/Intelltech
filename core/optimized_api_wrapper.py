#!/usr/bin/env python3
"""
Optimized API Wrapper
Drop-in replacement for requests.post() that applies cost optimizations automatically

Usage:
    # Instead of:
    # response = requests.post(url, headers=headers, json=payload)
    
    # Use:
    from optimized_api_wrapper import optimized_post
    response = optimized_post(url, headers=headers, json=payload)
    
Author: Manus AI + MOTHER V5
Date: 2026-02-16
"""

import os
import sys
import json
import requests
from typing import Dict, Any, Optional
from pathlib import Path

# Add core directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from prompt_optimizer import PromptOptimizer
    from response_controller import ResponseController
    OPTIMIZATION_AVAILABLE = True
except ImportError:
    OPTIMIZATION_AVAILABLE = False
    print("⚠️ Warning: Optimization modules not found. Running without optimization.")


class OptimizedAPIWrapper:
    """Wrapper that applies cost optimizations to API calls"""
    
    def __init__(self, enable_optimization: bool = None):
        """
        Initialize wrapper
        
        Args:
            enable_optimization: Whether to enable optimization (defaults to env var)
        """
        if enable_optimization is None:
            enable_optimization = os.environ.get('ENABLE_COST_OPTIMIZATION', 'true').lower() == 'true'
        
        self.enable_optimization = enable_optimization and OPTIMIZATION_AVAILABLE
        
        if self.enable_optimization:
            self.prompt_optimizer = PromptOptimizer()
            self.response_controller = ResponseController()
        
        # Stats tracking
        self.stats = {
            'total_calls': 0,
            'optimized_calls': 0,
            'total_tokens_saved_estimated': 0,
            'by_endpoint': {}
        }
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """
        Optimized POST request
        
        Args:
            url: API endpoint URL
            **kwargs: Same as requests.post()
            
        Returns:
            requests.Response object
        """
        self.stats['total_calls'] += 1
        
        # Track by endpoint
        endpoint = self._extract_endpoint(url)
        if endpoint not in self.stats['by_endpoint']:
            self.stats['by_endpoint'][endpoint] = {'calls': 0, 'optimized': 0}
        self.stats['by_endpoint'][endpoint]['calls'] += 1
        
        # Apply optimizations if enabled
        if self.enable_optimization and 'json' in kwargs:
            original_payload = kwargs['json']
            optimized_payload = self._optimize_payload(original_payload, endpoint)
            
            if optimized_payload != original_payload:
                kwargs['json'] = optimized_payload
                self.stats['optimized_calls'] += 1
                self.stats['by_endpoint'][endpoint]['optimized'] += 1
                
                # Estimate tokens saved (rough estimate)
                original_size = len(json.dumps(original_payload))
                optimized_size = len(json.dumps(optimized_payload))
                tokens_saved = (original_size - optimized_size) // 4  # Rough estimate: 4 chars = 1 token
                self.stats['total_tokens_saved_estimated'] += max(0, tokens_saved)
        
        # Make the actual API call
        response = requests.post(url, **kwargs)
        
        # Optionally process response (for future enhancement)
        # response = self._process_response(response, endpoint)
        
        return response
    
    def _extract_endpoint(self, url: str) -> str:
        """Extract endpoint name from URL for tracking"""
        try:
            # Extract path from URL
            from urllib.parse import urlparse
            parsed = urlparse(url)
            path = parsed.path
            
            # Get last meaningful part
            parts = [p for p in path.split('/') if p]
            if parts:
                return parts[-1]
            return 'unknown'
        except:
            return 'unknown'
    
    def _optimize_payload(self, payload: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
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
        
        # Create a copy to avoid modifying original
        optimized = payload.copy()
        
        # Optimize text fields (prompts, queries, etc)
        optimized = self.prompt_optimizer.optimize_prompt_data(optimized)
        
        # Add response size limits if applicable
        # (This is more relevant for LLM APIs, less for Apollo)
        if 'max_tokens' not in optimized and endpoint in ['chat', 'completions', 'generate']:
            optimized['max_tokens'] = 500  # Conservative default
        
        return optimized
    
    def _process_response(self, response: requests.Response, endpoint: str) -> requests.Response:
        """
        Process API response (for future enhancement)
        
        Args:
            response: Original response
            endpoint: API endpoint name
            
        Returns:
            Processed response
        """
        # For now, just return as-is
        # Future: Could truncate large responses, cache, etc
        return response
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get optimization statistics
        
        Returns:
            Dict with stats
        """
        stats = self.stats.copy()
        
        # Calculate percentages
        if stats['total_calls'] > 0:
            stats['optimization_rate'] = stats['optimized_calls'] / stats['total_calls'] * 100
        else:
            stats['optimization_rate'] = 0
        
        # Estimate cost savings (assuming $0.002 per 1K tokens for GPT-3.5)
        tokens_saved = stats['total_tokens_saved_estimated']
        stats['estimated_cost_savings_usd'] = (tokens_saved / 1000) * 0.002
        
        return stats
    
    def print_stats(self):
        """Print optimization statistics"""
        stats = self.get_stats()
        
        print("="*70)
        print("COST OPTIMIZATION STATISTICS")
        print("="*70)
        print(f"Total API Calls:        {stats['total_calls']}")
        print(f"Optimized Calls:        {stats['optimized_calls']}")
        print(f"Optimization Rate:      {stats['optimization_rate']:.1f}%")
        print(f"Tokens Saved (est):     {stats['total_tokens_saved_estimated']}")
        print(f"Cost Savings (est):     ${stats['estimated_cost_savings_usd']:.4f}")
        print()
        print("By Endpoint:")
        print("-"*70)
        for endpoint, data in stats['by_endpoint'].items():
            opt_rate = (data['optimized'] / data['calls'] * 100) if data['calls'] > 0 else 0
            print(f"  {endpoint:20s} {data['calls']:4d} calls  ({opt_rate:.0f}% optimized)")
        print("="*70)


# Global instance (singleton)
_global_wrapper = None


def get_wrapper() -> OptimizedAPIWrapper:
    """Get global wrapper instance"""
    global _global_wrapper
    
    if _global_wrapper is None:
        _global_wrapper = OptimizedAPIWrapper()
    
    return _global_wrapper


def optimized_post(url: str, **kwargs) -> requests.Response:
    """
    Optimized POST request (convenience function)
    
    Drop-in replacement for requests.post() with automatic optimizations
    
    Args:
        url: API endpoint URL
        **kwargs: Same as requests.post()
        
    Returns:
        requests.Response object
        
    Example:
        # Before:
        response = requests.post(url, headers=headers, json=payload)
        
        # After:
        response = optimized_post(url, headers=headers, json=payload)
    """
    wrapper = get_wrapper()
    return wrapper.post(url, **kwargs)


def print_optimization_stats():
    """Print optimization statistics (convenience function)"""
    wrapper = get_wrapper()
    wrapper.print_stats()


def get_optimization_stats() -> Dict[str, Any]:
    """Get optimization statistics (convenience function)"""
    wrapper = get_wrapper()
    return wrapper.get_stats()


if __name__ == "__main__":
    # Test the wrapper
    print("="*70)
    print("OPTIMIZED API WRAPPER - TEST")
    print("="*70)
    print()
    
    # Test 1: Simple POST with optimization
    print("TEST 1: Optimized POST")
    print("-"*70)
    
    test_payload = {
        'query': 'Please kindly provide a very detailed analysis of this data.',
        'max_results': 10,
        'filters': {
            'country': 'Australia',
            'industry': 'mining'
        }
    }
    
    print(f"Original payload size: {len(json.dumps(test_payload))} chars")
    
    # Simulate optimization (without actual API call)
    wrapper = get_wrapper()
    if wrapper.enable_optimization:
        optimized = wrapper._optimize_payload(test_payload, 'search')
        print(f"Optimized payload size: {len(json.dumps(optimized))} chars")
        print(f"Reduction: {len(json.dumps(test_payload)) - len(json.dumps(optimized))} chars")
    else:
        print("⚠️ Optimization disabled or unavailable")
    
    print()
    
    # Test 2: Stats tracking
    print("TEST 2: Stats Tracking")
    print("-"*70)
    
    # Simulate some calls
    wrapper.stats['total_calls'] = 10
    wrapper.stats['optimized_calls'] = 7
    wrapper.stats['total_tokens_saved_estimated'] = 150
    wrapper.stats['by_endpoint'] = {
        'search': {'calls': 5, 'optimized': 4},
        'enrich': {'calls': 3, 'optimized': 2},
        'create': {'calls': 2, 'optimized': 1}
    }
    
    wrapper.print_stats()
    
    print()
    print("="*70)
    print("✅ WRAPPER TEST COMPLETE")
    print("="*70)
