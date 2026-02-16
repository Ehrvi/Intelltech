#!/usr/bin/env python3
"""
Cost Optimization Integration Layer
Integrates PromptOptimizer and ResponseController into the main system

Usage:
    from cost_optimization_integration import optimize_api_call
    
    # Before making API call
    optimized_params = optimize_api_call(original_params, request_type='analysis')
    
    # Make API call
    response = api.call(**optimized_params)
    
    # Process response
    final_response = process_api_response(response, request_type='analysis')
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add core directory to path
sys.path.insert(0, str(Path(__file__).parent))

from prompt_optimizer import PromptOptimizer
from response_controller import ResponseController


class CostOptimizationIntegration:
    """Integration layer for cost optimization modules"""
    
    def __init__(self, enable_optimization: bool = True):
        """
        Initialize integration layer
        
        Args:
            enable_optimization: Whether to enable optimization (can be disabled for testing)
        """
        self.enable_optimization = enable_optimization
        
        # Initialize modules
        self.prompt_optimizer = PromptOptimizer()
        self.response_controller = ResponseController()
        
        # Stats tracking
        self.stats = {
            'total_calls': 0,
            'optimized_calls': 0,
            'total_tokens_saved': 0
        }
    
    def optimize_api_call(self, api_params: Dict[str, Any], request_type: str = 'default') -> Dict[str, Any]:
        """
        Optimize API call parameters before sending
        
        Args:
            api_params: Original API parameters
            request_type: Type of request ('summary', 'analysis', etc.)
            
        Returns:
            Optimized API parameters
        """
        if not self.enable_optimization:
            return api_params
        
        self.stats['total_calls'] += 1
        
        # Step 1: Optimize prompt
        optimized_params = self.prompt_optimizer.optimize_prompt_data(api_params)
        
        # Step 2: Enforce max_tokens
        optimized_params = self.response_controller.enforce_max_tokens(
            optimized_params,
            request_type=request_type
        )
        
        self.stats['optimized_calls'] += 1
        
        return optimized_params
    
    def process_api_response(self, response_data: Any, request_type: str = 'default') -> Any:
        """
        Process API response to control length
        
        Args:
            response_data: API response data
            request_type: Type of request
            
        Returns:
            Processed response
        """
        if not self.enable_optimization:
            return response_data
        
        return self.response_controller.run(response_data, request_type=request_type)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get optimization statistics
        
        Returns:
            Dict with stats
        """
        return self.stats.copy()


# Global instance (singleton pattern)
_global_optimizer = None


def get_optimizer() -> CostOptimizationIntegration:
    """
    Get global optimizer instance
    
    Returns:
        Global CostOptimizationIntegration instance
    """
    global _global_optimizer
    
    if _global_optimizer is None:
        # Check environment variable to enable/disable
        enable = os.environ.get('ENABLE_COST_OPTIMIZATION', 'true').lower() == 'true'
        _global_optimizer = CostOptimizationIntegration(enable_optimization=enable)
    
    return _global_optimizer


# Convenience functions
def optimize_api_call(api_params: Dict[str, Any], request_type: str = 'default') -> Dict[str, Any]:
    """
    Convenience function to optimize API call
    
    Args:
        api_params: Original API parameters
        request_type: Type of request
        
    Returns:
        Optimized API parameters
    """
    optimizer = get_optimizer()
    return optimizer.optimize_api_call(api_params, request_type=request_type)


def process_api_response(response_data: Any, request_type: str = 'default') -> Any:
    """
    Convenience function to process API response
    
    Args:
        response_data: API response data
        request_type: Type of request
        
    Returns:
        Processed response
    """
    optimizer = get_optimizer()
    return optimizer.process_api_response(response_data, request_type=request_type)


def get_optimization_stats() -> Dict[str, Any]:
    """
    Convenience function to get optimization stats
    
    Returns:
        Dict with stats
    """
    optimizer = get_optimizer()
    return optimizer.get_stats()


if __name__ == "__main__":
    # Test the integration
    print("="*70)
    print("COST OPTIMIZATION INTEGRATION - TEST")
    print("="*70)
    print()
    
    # Test 1: Optimize API call
    print("TEST 1: Optimize API Call")
    print("-"*70)
    
    original_params = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'user', 'content': 'Please kindly provide a very detailed analysis.'}
        ]
    }
    
    optimized_params = optimize_api_call(original_params, request_type='analysis')
    
    print(f"Original: {original_params}")
    print(f"Optimized: {optimized_params}")
    print(f"max_tokens added: {optimized_params.get('max_tokens', 'N/A')}")
    print()
    
    # Test 2: Process response
    print("TEST 2: Process API Response")
    print("-"*70)
    
    simulated_response = {
        'choices': [
            {
                'message': {
                    'role': 'assistant',
                    'content': 'Here is a very detailed analysis. ' * 100
                }
            }
        ]
    }
    
    processed_response = process_api_response(simulated_response, request_type='analysis')
    
    original_len = len(simulated_response['choices'][0]['message']['content'])
    processed_len = len(processed_response['choices'][0]['message']['content'])
    
    print(f"Original length: {original_len} chars")
    print(f"Processed length: {processed_len} chars")
    print(f"Savings: {original_len - processed_len} chars ({(original_len - processed_len)/original_len*100:.1f}%)")
    print()
    
    # Test 3: Get stats
    print("TEST 3: Get Optimization Stats")
    print("-"*70)
    
    stats = get_optimization_stats()
    print(f"Stats: {stats}")
    print()
    
    print("="*70)
    print("✅ INTEGRATION TEST COMPLETE")
    print("="*70)
