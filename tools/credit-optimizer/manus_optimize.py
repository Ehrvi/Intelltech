#!/usr/bin/env python3
"""
Manus Credit Optimization - Convenience Wrapper
Easy-to-use interface for credit optimization

Usage:
    from manus_optimize import optimize
    
    # Optimize file reading
    content = optimize.read_file("/path/to/file")
    
    # Optimize context
    compressed = optimize.compress_context(messages)
    
    # Optimize tool response
    optimized = optimize.tool_response(data)
    
    # Get stats
    stats = optimize.stats()
"""

import sys
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

from manus_credit_optimizer import get_optimizer


class ManusOptimize:
    """Convenience wrapper for Manus credit optimization"""
    
    def __init__(self):
        self._optimizer = None
    
    @property
    def optimizer(self):
        """Lazy load optimizer"""
        if self._optimizer is None:
            self._optimizer = get_optimizer()
        return self._optimizer
    
    def read_file(self, path: str) -> str:
        """Read file with caching"""
        return self.optimizer.read_file_optimized(path)
    
    def compress_context(self, messages: list) -> list:
        """Compress context for long conversations"""
        return self.optimizer.compress_context_optimized(messages)
    
    def tool_response(self, data, response_type: str = 'auto') -> str:
        """Optimize tool response"""
        return self.optimizer.optimize_tool_response(data, response_type)
    
    def stats(self) -> dict:
        """Get optimization statistics"""
        return self.optimizer.get_optimization_stats()
    
    def report(self, mode: str = 'summary'):
        """Print optimization report"""
        if mode == 'summary':
            stats = self.stats()
            cache = stats['file_cache']
            
            print("="*60)
            print("MANUS CREDIT OPTIMIZATION - SUMMARY")
            print("="*60)
            print(f"Cache Hit Rate: {cache['hit_rate_pct']:.1f}%")
            print(f"Tokens Saved: {cache['tokens_saved']:,}")
            print(f"Cached Files: {cache['cached_files']}")
            print("="*60)
        elif mode == 'detailed':
            stats = self.stats()
            print("="*60)
            print("MANUS CREDIT OPTIMIZATION - DETAILED")
            print("="*60)
            
            # File cache
            print("\n📁 FILE CACHE:")
            cache = stats['file_cache']
            for key, value in cache.items():
                print(f"  {key}: {value}")
            
            # Enabled optimizations
            print("\n⚙️ ENABLED OPTIMIZATIONS:")
            for opt, enabled in stats['enabled_optimizations'].items():
                status = "✅" if enabled else "❌"
                print(f"  {status} {opt}")
            
            # Savings report
            if 'savings_report' in stats and 'error' not in stats['savings_report']:
                print("\n💰 SAVINGS (Last 7 Days):")
                savings = stats['savings_report']
                for key, value in savings.items():
                    if key != 'optimization_stats':
                        print(f"  {key}: {value}")
            
            print("="*60)


# Global instance
optimize = ManusOptimize()


if __name__ == "__main__":
    # Demo
    print("Manus Credit Optimization - Convenience Wrapper")
    print()
    print("Usage:")
    print("  from manus_optimize import optimize")
    print("  content = optimize.read_file('/path/to/file')")
    print("  stats = optimize.stats()")
    print("  optimize.report('summary')")
    print()
    
    # Show current stats
    optimize.report('summary')
