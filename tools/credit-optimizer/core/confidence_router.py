#!/usr/bin/env python3
"""
Confidence-Based API Routing
Routes requests to cheaper APIs when confidence is sufficient

Strategy:
1. Estimate task complexity/confidence
2. Try cheaper API first
3. Fall back to expensive API if needed
4. Learn from outcomes

Based on Chen et al. (2020) "FrugalML"

Author: Manus AI
Date: 2026-02-16
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any


class ConfidenceRouter:
    """
    Routes API calls based on confidence and cost
    """
    
    def __init__(self, base_path: str = "/home/ubuntu/manus_global_knowledge"):
        """
        Initialize confidence router
        
        Args:
            base_path: Base path for logs and data
        """
        self.base_path = Path(base_path)
        self.logs_dir = self.base_path / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        self.routing_log = self.logs_dir / "routing_decisions.jsonl"
        
        # API tiers (from cheap to expensive)
        self.api_tiers = {
            'apollo': [
                {'name': 'apollo_search', 'cost_per_call': 0.002, 'confidence_threshold': 0.3},
                {'name': 'apollo_enrich', 'cost_per_call': 0.003, 'confidence_threshold': 0.5},
            ],
            'openai': [
                {'name': 'gpt-3.5-turbo', 'cost_per_1k_tokens': 0.002, 'confidence_threshold': 0.6},
                {'name': 'gpt-4', 'cost_per_1k_tokens': 0.030, 'confidence_threshold': 0.0},  # Always available
            ]
        }
        
        # Routing statistics
        self.stats = {
            'total_routes': 0,
            'successful_cheap_routes': 0,
            'fallback_routes': 0,
            'cost_saved': 0.0,
            'by_operation': {}
        }
    
    def estimate_confidence(self, operation: str, payload: Dict[str, Any]) -> float:
        """
        Estimate confidence for a task
        
        Args:
            operation: Operation name
            payload: Request payload
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        confidence = 0.5  # Default medium confidence
        
        # Heuristics for confidence estimation
        
        # 1. Simple operations have higher confidence for cheap APIs
        simple_operations = ['search', 'lookup', 'find', 'get', 'list']
        if any(op in operation.lower() for op in simple_operations):
            confidence += 0.2
        
        # 2. Complex operations need expensive APIs
        complex_operations = ['analyze', 'generate', 'create', 'write', 'design']
        if any(op in operation.lower() for op in complex_operations):
            confidence -= 0.2
        
        # 3. Small payloads can use cheap APIs
        payload_size = len(json.dumps(payload))
        if payload_size < 500:
            confidence += 0.1
        elif payload_size > 2000:
            confidence -= 0.1
        
        # 4. Check for specific fields that indicate complexity
        if isinstance(payload, dict):
            # If asking for detailed analysis
            if any(keyword in str(payload).lower() for keyword in ['detailed', 'comprehensive', 'analysis']):
                confidence -= 0.15
            
            # If simple query
            if any(keyword in str(payload).lower() for keyword in ['simple', 'quick', 'basic']):
                confidence += 0.15
        
        # Clamp to [0, 1]
        confidence = max(0.0, min(1.0, confidence))
        
        return confidence
    
    def select_api(self, api_type: str, operation: str, payload: Dict[str, Any]) -> Tuple[str, float]:
        """
        Select the best API for a task
        
        Args:
            api_type: Type of API ('apollo' or 'openai')
            operation: Operation name
            payload: Request payload
            
        Returns:
            Tuple of (selected_api_name, confidence)
        """
        if api_type not in self.api_tiers:
            return (None, 0.0)
        
        # Estimate confidence
        confidence = self.estimate_confidence(operation, payload)
        
        # Select API tier based on confidence
        tiers = self.api_tiers[api_type]
        
        for tier in tiers:
            if confidence >= tier['confidence_threshold']:
                return (tier['name'], confidence)
        
        # Default to last (most expensive) tier
        return (tiers[-1]['name'], confidence)
    
    def route_request(self, api_type: str, operation: str, payload: Dict[str, Any], 
                     execute_fn: callable) -> Tuple[Any, Dict]:
        """
        Route request with fallback strategy
        
        Args:
            api_type: Type of API ('apollo' or 'openai')
            operation: Operation name
            payload: Request payload
            execute_fn: Function to execute the API call (api_name, payload) -> response
            
        Returns:
            Tuple of (response, routing_info)
        """
        self.stats['total_routes'] += 1
        
        # Track by operation
        if operation not in self.stats['by_operation']:
            self.stats['by_operation'][operation] = {
                'total': 0,
                'cheap_success': 0,
                'fallback': 0,
                'cost_saved': 0.0
            }
        
        self.stats['by_operation'][operation]['total'] += 1
        
        # Select initial API
        selected_api, confidence = self.select_api(api_type, operation, payload)
        
        routing_info = {
            'operation': operation,
            'confidence': confidence,
            'selected_api': selected_api,
            'fallback_used': False,
            'cost_saved': 0.0
        }
        
        # Try selected API
        try:
            response = execute_fn(selected_api, payload)
            
            # Check if response is good enough
            is_good = self._validate_response(response, confidence)
            
            if is_good:
                # Success with selected API
                self.stats['successful_cheap_routes'] += 1
                self.stats['by_operation'][operation]['cheap_success'] += 1
                
                # Calculate cost saved (if not using most expensive)
                if api_type in self.api_tiers:
                    tiers = self.api_tiers[api_type]
                    if selected_api != tiers[-1]['name']:
                        # Estimate cost saved
                        cost_saved = self._estimate_cost_saved(api_type, selected_api, tiers[-1]['name'])
                        routing_info['cost_saved'] = cost_saved
                        self.stats['cost_saved'] += cost_saved
                        self.stats['by_operation'][operation]['cost_saved'] += cost_saved
                
                self._log_routing(routing_info)
                return (response, routing_info)
            else:
                # Response not good enough, fallback
                raise Exception("Response quality insufficient")
        
        except Exception as e:
            # Fallback to most expensive API
            if api_type in self.api_tiers:
                tiers = self.api_tiers[api_type]
                fallback_api = tiers[-1]['name']
                
                if fallback_api != selected_api:
                    routing_info['fallback_used'] = True
                    routing_info['fallback_api'] = fallback_api
                    routing_info['fallback_reason'] = str(e)
                    
                    self.stats['fallback_routes'] += 1
                    self.stats['by_operation'][operation]['fallback'] += 1
                    
                    # Execute fallback
                    response = execute_fn(fallback_api, payload)
                    
                    self._log_routing(routing_info)
                    return (response, routing_info)
            
            # If no fallback available, raise error
            raise
    
    def _validate_response(self, response: Any, confidence: float) -> bool:
        """
        Validate if response is good enough
        
        Args:
            response: API response
            confidence: Confidence score
            
        Returns:
            True if response is acceptable
        """
        # Simple validation heuristics
        
        # If high confidence, accept response
        if confidence > 0.7:
            return True
        
        # Check if response is not empty
        if response is None:
            return False
        
        # Check response size (too small might be incomplete)
        if isinstance(response, str) and len(response) < 10:
            return False
        
        if isinstance(response, dict):
            # Check for error indicators
            if 'error' in response or 'Error' in response:
                return False
            
            # Check if response has content
            if not response:
                return False
        
        # Default: accept
        return True
    
    def _estimate_cost_saved(self, api_type: str, used_api: str, expensive_api: str) -> float:
        """
        Estimate cost saved by using cheaper API
        
        Args:
            api_type: Type of API
            used_api: API that was used
            expensive_api: Most expensive API
            
        Returns:
            Estimated cost saved in USD
        """
        tiers = self.api_tiers[api_type]
        
        used_cost = 0.0
        expensive_cost = 0.0
        
        for tier in tiers:
            if tier['name'] == used_api:
                used_cost = tier.get('cost_per_call', tier.get('cost_per_1k_tokens', 0.0))
            if tier['name'] == expensive_api:
                expensive_cost = tier.get('cost_per_call', tier.get('cost_per_1k_tokens', 0.0))
        
        return max(0.0, expensive_cost - used_cost)
    
    def _log_routing(self, routing_info: Dict):
        """
        Log routing decision
        
        Args:
            routing_info: Routing information
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            **routing_info
        }
        
        try:
            with open(self.routing_log, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            print(f"⚠️ Warning: Failed to log routing: {e}")
    
    def get_stats(self) -> Dict:
        """
        Get routing statistics
        
        Returns:
            Dict with statistics
        """
        stats = self.stats.copy()
        
        if stats['total_routes'] > 0:
            stats['cheap_success_rate'] = (stats['successful_cheap_routes'] / stats['total_routes'] * 100)
            stats['fallback_rate'] = (stats['fallback_routes'] / stats['total_routes'] * 100)
        else:
            stats['cheap_success_rate'] = 0
            stats['fallback_rate'] = 0
        
        return stats
    
    def generate_report(self) -> str:
        """
        Generate routing report
        
        Returns:
            Report string
        """
        stats = self.get_stats()
        
        report = "="*70 + "\n"
        report += "CONFIDENCE-BASED ROUTING REPORT\n"
        report += "="*70 + "\n\n"
        
        report += f"Total Routes:         {stats['total_routes']}\n"
        report += f"Cheap API Success:    {stats['successful_cheap_routes']} ({stats['cheap_success_rate']:.1f}%)\n"
        report += f"Fallback Routes:      {stats['fallback_routes']} ({stats['fallback_rate']:.1f}%)\n"
        report += f"Total Cost Saved:     ${stats['cost_saved']:.4f}\n"
        report += "\n"
        
        if stats['by_operation']:
            report += "By Operation:\n"
            report += "-"*70 + "\n"
            for operation, op_stats in stats['by_operation'].items():
                cheap_rate = (op_stats['cheap_success'] / op_stats['total'] * 100) if op_stats['total'] > 0 else 0
                report += f"  {operation:30s} {op_stats['total']:4d} routes  "
                report += f"({cheap_rate:.0f}% cheap, ${op_stats['cost_saved']:.4f} saved)\n"
        
        report += "="*70 + "\n"
        
        return report


def main():
    """Test the confidence router"""
    router = ConfidenceRouter()
    
    print("Testing Confidence Router...")
    print()
    
    # Test 1: Estimate confidence
    print("Test 1: Confidence estimation")
    
    simple_payload = {'query': 'find companies'}
    confidence = router.estimate_confidence("search_companies", simple_payload)
    print(f"  Simple search confidence: {confidence:.2f}")
    
    complex_payload = {'query': 'generate comprehensive analysis of market trends'}
    confidence = router.estimate_confidence("analyze_market", complex_payload)
    print(f"  Complex analysis confidence: {confidence:.2f}")
    print()
    
    # Test 2: API selection
    print("Test 2: API selection")
    
    api, confidence = router.select_api("openai", "search_companies", simple_payload)
    print(f"  Selected API: {api}, Confidence: {confidence:.2f}")
    
    api, confidence = router.select_api("openai", "analyze_market", complex_payload)
    print(f"  Selected API: {api}, Confidence: {confidence:.2f}")
    print()
    
    # Test 3: Mock routing
    print("Test 3: Mock routing")
    
    def mock_execute(api_name, payload):
        return {"result": f"Response from {api_name}"}
    
    response, info = router.route_request("openai", "search_companies", simple_payload, mock_execute)
    print(f"  Response: {response}")
    print(f"  Routing info: {info}")
    print()
    
    # Generate report
    print(router.generate_report())


if __name__ == "__main__":
    main()
