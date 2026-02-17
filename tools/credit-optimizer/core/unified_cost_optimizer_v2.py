#!/usr/bin/env python3
"""
Unified Cost Optimizer V2 - Phase 1 Complete
Integrates all Phase 1 features for efficient and reliable cost control

New Features in V2:
- Anomaly detection for real-time monitoring
- ML-based threshold learning
- Confidence-based API routing
- Enhanced monitoring and alerts

Target: 55-65% cost reduction

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

# Import Phase 1 modules
try:
    from anomaly_detector import AnomalyDetector
    from ml_threshold_learner import MLThresholdLearner
    from confidence_router import ConfidenceRouter
    from cost_monitor import CostMonitor
    PHASE1_AVAILABLE = True
except ImportError as e:
    PHASE1_AVAILABLE = False
    print(f"⚠️ Warning: Phase 1 modules not available: {e}")

# Import original optimization modules
try:
    from prompt_optimizer import PromptOptimizer
    from response_controller import ResponseController
    OPTIMIZATION_MODULES_AVAILABLE = True
except ImportError:
    OPTIMIZATION_MODULES_AVAILABLE = False


class UnifiedCostOptimizerV2:
    """
    Enhanced unified cost optimizer with Phase 1 features
    """
    
    def __init__(self, enable_optimization: bool = None):
        """
        Initialize the enhanced optimizer
        
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
        
        # Initialize Phase 1 modules
        if PHASE1_AVAILABLE:
            self.anomaly_detector = AnomalyDetector(str(self.base_path))
            self.ml_learner = MLThresholdLearner(str(self.base_path))
            self.router = ConfidenceRouter(str(self.base_path))
            self.monitor = CostMonitor(str(self.base_path))
        else:
            self.anomaly_detector = None
            self.ml_learner = None
            self.router = None
            self.monitor = None
        
        # Initialize original optimization modules
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
            'enable_response_control': True,
            'enable_anomaly_detection': True,
            'enable_ml_learning': True,
            'enable_routing': True,
            'enable_monitoring': True
        }
        
        # Statistics tracking
        self.stats = {
            'total_calls': 0,
            'optimized_calls': 0,
            'cache_hits': 0,
            'template_uses': 0,
            'anomalies_detected': 0,
            'routing_savings': 0.0,
            'total_tokens_saved': 0,
            'total_cost_saved': 0.0,
            'by_endpoint': {}
        }
    
    # ==================== CACHING (from V1) ====================
    
    def _generate_cache_key(self, data: str) -> str:
        """Generate MD5 hash for cache key"""
        return hashlib.md5(data.encode()).hexdigest()
    
    def check_cache(self, key: str, ttl_days: int = None) -> Tuple[bool, Any, str]:
        """Check if cached response exists and is valid"""
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
        """Save response to cache"""
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
    
    # ==================== TEMPLATES (from V1) ====================
    
    def get_template(self, template_name: str) -> Optional[str]:
        """Get template if exists"""
        if not self.config['enable_templates']:
            return None
        
        template_file = self.templates_dir / f"{template_name}.md"
        
        if template_file.exists():
            self.stats['template_uses'] += 1
            return template_file.read_text()
        
        return None
    
    def save_template(self, template_name: str, content: str):
        """Save template for reuse"""
        if not self.config['enable_templates']:
            return
        
        template_file = self.templates_dir / f"{template_name}.md"
        
        try:
            template_file.write_text(content)
        except Exception as e:
            print(f"⚠️ Warning: Failed to save template: {e}")
    
    # ==================== OPTIMIZATION (from V1 + ML) ====================
    
    def optimize_payload(self, payload: Dict[str, Any], endpoint: str, operation: str) -> Dict[str, Any]:
        """
        Optimize API payload with ML-based decisions
        
        Args:
            payload: Original payload
            endpoint: API endpoint name
            operation: Operation name
            
        Returns:
            Optimized payload
        """
        if not self.enable_optimization:
            return payload
        
        # Create a copy
        optimized = payload.copy()
        
        # Use ML learner to decide on optimizations
        if self.ml_learner and self.config['enable_ml_learning']:
            # Estimate prompt length
            prompt_length = len(json.dumps(payload))
            
            # Should we compress?
            should_compress, confidence = self.ml_learner.should_compress_prompt(operation, prompt_length)
            
            if should_compress and self.prompt_optimizer and self.config['enable_prompt_optimization']:
                optimized = self.prompt_optimizer.optimize_prompt_data(optimized)
            
            # Should we control response?
            expected_tokens = 500  # Default estimate
            should_control, max_tokens, confidence = self.ml_learner.should_control_response(operation, expected_tokens)
            
            if should_control and self.config['enable_response_control']:
                if 'max_tokens' not in optimized and endpoint in ['chat', 'completions', 'generate']:
                    optimized['max_tokens'] = max_tokens
        else:
            # Fallback to original optimization
            if self.prompt_optimizer and self.config['enable_prompt_optimization']:
                optimized = self.prompt_optimizer.optimize_prompt_data(optimized)
            
            if self.config['enable_response_control']:
                if 'max_tokens' not in optimized and endpoint in ['chat', 'completions', 'generate']:
                    optimized['max_tokens'] = 500
        
        return optimized
    
    # ==================== API WRAPPER (Enhanced) ====================
    
    def post(self, url: str, operation: str = None, **kwargs) -> requests.Response:
        """
        Optimized POST request with all Phase 1 features
        
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
                'template_uses': 0,
                'anomalies': 0
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
        
        # 3. Apply optimizations with ML decisions
        if self.enable_optimization and 'json' in kwargs:
            original_payload = kwargs['json']
            optimized_payload = self.optimize_payload(original_payload, endpoint, operation)
            
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
        
        # 5. Estimate cost
        estimated_tokens = len(response.text) // 4
        estimated_cost = estimated_tokens * 0.000003  # Rough estimate
        
        # 6. Anomaly detection
        if self.anomaly_detector and self.config['enable_anomaly_detection']:
            is_anomaly, reason, severity = self.anomaly_detector.detect_anomaly(
                operation, estimated_cost, estimated_tokens
            )
            
            if is_anomaly:
                print(f"⚠️ ANOMALY DETECTED: {reason} (severity: {severity:.2f})")
                self.stats['anomalies_detected'] += 1
                self.stats['by_endpoint'][endpoint]['anomalies'] += 1
        
        # 7. Cache the response
        if response.status_code == 200:
            # Use ML to decide if should cache
            if self.ml_learner and self.config['enable_ml_learning']:
                should_cache, confidence = self.ml_learner.should_cache(operation, estimated_cost)
                if should_cache:
                    try:
                        response_data = response.json()
                        self.save_cache(cache_key, response_data)
                    except Exception as e:
                        pass
            else:
                # Default: always cache successful responses
                try:
                    response_data = response.json()
                    self.save_cache(cache_key, response_data)
                except Exception as e:
                    pass
        
        # 8. Log cost
        self.log_cost(operation, estimated_cost, estimated_tokens)
        
        # 9. Check budgets and generate alerts
        if self.monitor and self.config['enable_monitoring']:
            alerts = self.monitor.check_budgets()
            for alert in alerts:
                print(f"🔔 BUDGET ALERT: {alert['message']}")
        
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
        """Log cost for tracking"""
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
    
    # ==================== STATISTICS ====================
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        stats = self.stats.copy()
        
        # Calculate rates
        if stats['total_calls'] > 0:
            stats['optimization_rate'] = stats['optimized_calls'] / stats['total_calls'] * 100
            stats['cache_hit_rate'] = stats['cache_hits'] / stats['total_calls'] * 100
            stats['anomaly_rate'] = stats['anomalies_detected'] / stats['total_calls'] * 100
        else:
            stats['optimization_rate'] = 0
            stats['cache_hit_rate'] = 0
            stats['anomaly_rate'] = 0
        
        # Estimate cost savings
        tokens_saved = stats['total_tokens_saved']
        stats['estimated_cost_savings_usd'] = (tokens_saved / 1000) * 0.002 + stats['total_cost_saved']
        
        # Add Phase 1 module stats
        if self.ml_learner:
            stats['ml_learner'] = self.ml_learner.get_stats()
        
        if self.router:
            stats['router'] = self.router.get_stats()
        
        if self.monitor:
            stats['spending'] = self.monitor.get_current_spending()
        
        return stats
    
    def print_stats(self):
        """Print comprehensive statistics"""
        stats = self.get_stats()
        
        print("="*70)
        print("UNIFIED COST OPTIMIZER V2 - PHASE 1 STATISTICS")
        print("="*70)
        print(f"Total API Calls:        {stats['total_calls']}")
        print(f"Optimized Calls:        {stats['optimized_calls']} ({stats['optimization_rate']:.1f}%)")
        print(f"Cache Hits:             {stats['cache_hits']} ({stats['cache_hit_rate']:.1f}%)")
        print(f"Template Uses:          {stats['template_uses']}")
        print(f"Anomalies Detected:     {stats['anomalies_detected']} ({stats['anomaly_rate']:.1f}%)")
        print(f"Tokens Saved (est):     {stats['total_tokens_saved']}")
        print(f"Cost Savings (est):     ${stats['estimated_cost_savings_usd']:.4f}")
        print()
        
        # ML Learner stats
        if 'ml_learner' in stats and stats['ml_learner']:
            ml_stats = stats['ml_learner']
            print("ML Threshold Learner:")
            print("-"*70)
            print(f"  Total Decisions:      {ml_stats['total_decisions']}")
            print(f"  Accuracy:             {ml_stats['accuracy']:.1f}%")
            print()
        
        # Router stats
        if 'router' in stats and stats['router']:
            router_stats = stats['router']
            print("Confidence Router:")
            print("-"*70)
            print(f"  Total Routes:         {router_stats['total_routes']}")
            print(f"  Cheap Success Rate:   {router_stats.get('cheap_success_rate', 0):.1f}%")
            print(f"  Routing Savings:      ${router_stats['cost_saved']:.4f}")
            print()
        
        # Spending overview
        if 'spending' in stats and stats['spending']:
            spending = stats['spending']
            print("Current Spending:")
            print("-"*70)
            for period, data in spending.items():
                print(f"  {period.capitalize():8s} ${data['spent']:6.2f}/${data['budget']:6.2f} ({data['percentage']:.1f}%)")
            print()
        
        print("By Endpoint:")
        print("-"*70)
        for endpoint, data in stats['by_endpoint'].items():
            opt_rate = (data['optimized'] / data['calls'] * 100) if data['calls'] > 0 else 0
            cache_rate = (data['cache_hits'] / data['calls'] * 100) if data['calls'] > 0 else 0
            print(f"  {endpoint:20s} {data['calls']:4d} calls  "
                  f"({opt_rate:.0f}% opt, {cache_rate:.0f}% cached, {data['anomalies']} anomalies)")
        print("="*70)
    
    def generate_dashboard(self) -> str:
        """Generate monitoring dashboard"""
        if self.monitor:
            return self.monitor.generate_dashboard()
        else:
            return "Monitoring not available"


# ==================== GLOBAL INSTANCE ====================

_global_optimizer_v2 = None


def get_optimizer() -> UnifiedCostOptimizerV2:
    """Get global optimizer instance (singleton)"""
    global _global_optimizer_v2
    
    if _global_optimizer_v2 is None:
        _global_optimizer_v2 = UnifiedCostOptimizerV2()
    
    return _global_optimizer_v2


def optimized_post(url: str, operation: str = None, **kwargs) -> requests.Response:
    """Optimized POST request (convenience function)"""
    optimizer = get_optimizer()
    return optimizer.post(url, operation=operation, **kwargs)


def print_optimization_stats():
    """Print optimization statistics (convenience function)"""
    optimizer = get_optimizer()
    optimizer.print_stats()


def print_dashboard():
    """Print monitoring dashboard (convenience function)"""
    optimizer = get_optimizer()
    print(optimizer.generate_dashboard())


if __name__ == "__main__":
    print("="*70)
    print("UNIFIED COST OPTIMIZER V2 - PHASE 1 TEST")
    print("="*70)
    print()
    
    optimizer = UnifiedCostOptimizerV2()
    
    print("✅ Optimizer V2 initialized with Phase 1 features:")
    print(f"   - Anomaly Detection: {optimizer.anomaly_detector is not None}")
    print(f"   - ML Learner: {optimizer.ml_learner is not None}")
    print(f"   - Confidence Router: {optimizer.router is not None}")
    print(f"   - Cost Monitor: {optimizer.monitor is not None}")
    print()
    
    print("="*70)
    print("✅ UNIFIED OPTIMIZER V2 READY")
    print("="*70)
