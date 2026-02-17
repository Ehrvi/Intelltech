#!/usr/bin/env python3
"""
Anomaly Detection for Cost Optimization
Detects unusual spending patterns and alerts in real-time

Based on:
- Statistical outlier detection (Z-score)
- Rolling window analysis
- Threshold-based alerts

Author: Manus AI
Date: 2026-02-16
"""

import json
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class AnomalyDetector:
    """
    Detects anomalies in API usage and costs
    """
    
    def __init__(self, base_path: str = "/home/ubuntu/manus_global_knowledge"):
        """
        Initialize anomaly detector
        
        Args:
            base_path: Base path for logs and data
        """
        self.base_path = Path(base_path)
        self.logs_dir = self.base_path / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        self.cost_log = self.logs_dir / "cost_tracking.jsonl"
        self.anomaly_log = self.logs_dir / "anomalies.jsonl"
        
        # Configuration
        self.config = {
            'z_score_threshold': 3.0,  # Standard deviations for outlier
            'rolling_window_hours': 24,  # Window for rolling statistics
            'min_samples': 10,  # Minimum samples needed for detection
            'cost_spike_threshold': 2.0,  # 2x average is a spike
            'token_spike_threshold': 2.0,  # 2x average is a spike
        }
        
        # Cache for statistics
        self.stats_cache = {
            'last_update': None,
            'stats': None
        }
    
    def _load_recent_costs(self, hours: int = 24) -> List[Dict]:
        """
        Load recent cost entries from log
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            List of cost entries
        """
        if not self.cost_log.exists():
            return []
        
        cutoff = datetime.now() - timedelta(hours=hours)
        entries = []
        
        try:
            with open(self.cost_log, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['timestamp'])
                    
                    if entry_time > cutoff:
                        entries.append(entry)
        except Exception as e:
            print(f"⚠️ Warning: Failed to load cost log: {e}")
        
        return entries
    
    def _calculate_statistics(self, entries: List[Dict]) -> Dict:
        """
        Calculate statistical metrics from entries
        
        Args:
            entries: List of cost entries
            
        Returns:
            Dict with statistics
        """
        if len(entries) < self.config['min_samples']:
            return None
        
        costs = [e['cost'] for e in entries]
        tokens = [e['tokens'] for e in entries]
        
        # By operation
        by_operation = defaultdict(lambda: {'costs': [], 'tokens': []})
        for entry in entries:
            op = entry['operation']
            by_operation[op]['costs'].append(entry['cost'])
            by_operation[op]['tokens'].append(entry['tokens'])
        
        stats = {
            'total_entries': len(entries),
            'cost': {
                'mean': np.mean(costs),
                'std': np.std(costs),
                'median': np.median(costs),
                'min': np.min(costs),
                'max': np.max(costs),
                'total': np.sum(costs)
            },
            'tokens': {
                'mean': np.mean(tokens),
                'std': np.std(tokens),
                'median': np.median(tokens),
                'min': np.min(tokens),
                'max': np.max(tokens),
                'total': np.sum(tokens)
            },
            'by_operation': {}
        }
        
        # Calculate per-operation stats
        for op, data in by_operation.items():
            if len(data['costs']) >= 3:  # Need at least 3 samples
                stats['by_operation'][op] = {
                    'cost_mean': np.mean(data['costs']),
                    'cost_std': np.std(data['costs']),
                    'token_mean': np.mean(data['tokens']),
                    'token_std': np.std(data['tokens']),
                    'count': len(data['costs'])
                }
        
        return stats
    
    def get_statistics(self, force_refresh: bool = False) -> Optional[Dict]:
        """
        Get current statistics (cached)
        
        Args:
            force_refresh: Force refresh of cache
            
        Returns:
            Statistics dict or None
        """
        # Check cache
        if not force_refresh and self.stats_cache['last_update']:
            age = (datetime.now() - self.stats_cache['last_update']).seconds
            if age < 300:  # Cache for 5 minutes
                return self.stats_cache['stats']
        
        # Refresh statistics
        entries = self._load_recent_costs(self.config['rolling_window_hours'])
        stats = self._calculate_statistics(entries)
        
        self.stats_cache['last_update'] = datetime.now()
        self.stats_cache['stats'] = stats
        
        return stats
    
    def detect_anomaly(self, operation: str, cost: float, tokens: int) -> Tuple[bool, str, float]:
        """
        Detect if a cost entry is anomalous
        
        Args:
            operation: Operation name
            cost: Cost in USD
            tokens: Number of tokens
            
        Returns:
            Tuple of (is_anomaly, reason, severity)
            severity: 0.0 (normal) to 1.0 (critical)
        """
        stats = self.get_statistics()
        
        if stats is None:
            # Not enough data yet
            return (False, "Insufficient data for anomaly detection", 0.0)
        
        anomalies = []
        max_severity = 0.0
        
        # 1. Check global cost anomaly (Z-score)
        if stats['cost']['std'] > 0:
            z_score = (cost - stats['cost']['mean']) / stats['cost']['std']
            if abs(z_score) > self.config['z_score_threshold']:
                severity = min(abs(z_score) / 10.0, 1.0)  # Cap at 1.0
                anomalies.append(f"Cost Z-score: {z_score:.2f}")
                max_severity = max(max_severity, severity)
        
        # 2. Check cost spike (relative to mean)
        cost_ratio = cost / stats['cost']['mean'] if stats['cost']['mean'] > 0 else 0
        if cost_ratio > self.config['cost_spike_threshold']:
            severity = min(cost_ratio / 10.0, 1.0)
            anomalies.append(f"Cost spike: {cost_ratio:.1f}x average")
            max_severity = max(max_severity, severity)
        
        # 3. Check token spike
        token_ratio = tokens / stats['tokens']['mean'] if stats['tokens']['mean'] > 0 else 0
        if token_ratio > self.config['token_spike_threshold']:
            severity = min(token_ratio / 10.0, 1.0)
            anomalies.append(f"Token spike: {token_ratio:.1f}x average")
            max_severity = max(max_severity, severity)
        
        # 4. Check operation-specific anomaly
        if operation in stats['by_operation']:
            op_stats = stats['by_operation'][operation]
            
            if op_stats['cost_std'] > 0:
                op_z_score = (cost - op_stats['cost_mean']) / op_stats['cost_std']
                if abs(op_z_score) > self.config['z_score_threshold']:
                    severity = min(abs(op_z_score) / 10.0, 1.0)
                    anomalies.append(f"Operation '{operation}' Z-score: {op_z_score:.2f}")
                    max_severity = max(max_severity, severity)
        
        # Determine if anomalous
        is_anomaly = len(anomalies) > 0
        reason = "; ".join(anomalies) if anomalies else "Normal"
        
        # Log anomaly
        if is_anomaly:
            self._log_anomaly(operation, cost, tokens, reason, max_severity)
        
        return (is_anomaly, reason, max_severity)
    
    def _log_anomaly(self, operation: str, cost: float, tokens: int, reason: str, severity: float):
        """
        Log detected anomaly
        
        Args:
            operation: Operation name
            cost: Cost in USD
            tokens: Number of tokens
            reason: Reason for anomaly
            severity: Severity level (0-1)
        """
        anomaly_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'cost': cost,
            'tokens': tokens,
            'reason': reason,
            'severity': severity
        }
        
        try:
            with open(self.anomaly_log, 'a') as f:
                f.write(json.dumps(anomaly_entry) + '\n')
        except Exception as e:
            print(f"⚠️ Warning: Failed to log anomaly: {e}")
    
    def get_recent_anomalies(self, hours: int = 24) -> List[Dict]:
        """
        Get recent anomalies
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            List of anomaly entries
        """
        if not self.anomaly_log.exists():
            return []
        
        cutoff = datetime.now() - timedelta(hours=hours)
        anomalies = []
        
        try:
            with open(self.anomaly_log, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['timestamp'])
                    
                    if entry_time > cutoff:
                        anomalies.append(entry)
        except Exception as e:
            print(f"⚠️ Warning: Failed to load anomaly log: {e}")
        
        return anomalies
    
    def generate_report(self) -> str:
        """
        Generate anomaly detection report
        
        Returns:
            Report string
        """
        stats = self.get_statistics(force_refresh=True)
        anomalies = self.get_recent_anomalies(hours=24)
        
        report = "="*70 + "\n"
        report += "ANOMALY DETECTION REPORT (24 hours)\n"
        report += "="*70 + "\n\n"
        
        if stats is None:
            report += "⚠️ Insufficient data for anomaly detection\n"
            report += f"   Need at least {self.config['min_samples']} samples\n"
        else:
            report += f"Total Entries:        {stats['total_entries']}\n"
            report += f"Average Cost:         ${stats['cost']['mean']:.4f}\n"
            report += f"Cost Std Dev:         ${stats['cost']['std']:.4f}\n"
            report += f"Total Cost:           ${stats['cost']['total']:.2f}\n"
            report += f"Average Tokens:       {stats['tokens']['mean']:.0f}\n"
            report += f"Total Tokens:         {stats['tokens']['total']:.0f}\n"
            report += "\n"
        
        report += f"Anomalies Detected:   {len(anomalies)}\n"
        
        if anomalies:
            report += "\n"
            report += "Recent Anomalies:\n"
            report += "-"*70 + "\n"
            
            for anomaly in anomalies[-10:]:  # Show last 10
                timestamp = anomaly['timestamp'][:19]  # Remove microseconds
                severity_label = "🔴 CRITICAL" if anomaly['severity'] > 0.7 else "🟡 WARNING"
                report += f"{severity_label} [{timestamp}]\n"
                report += f"  Operation: {anomaly['operation']}\n"
                report += f"  Cost: ${anomaly['cost']:.4f}, Tokens: {anomaly['tokens']}\n"
                report += f"  Reason: {anomaly['reason']}\n"
                report += "\n"
        
        report += "="*70 + "\n"
        
        return report


def main():
    """Test the anomaly detector"""
    detector = AnomalyDetector()
    
    print("Testing Anomaly Detector...")
    print()
    
    # Test with normal values
    print("Test 1: Normal value")
    is_anomaly, reason, severity = detector.detect_anomaly("test_op", 0.05, 100)
    print(f"  Anomaly: {is_anomaly}, Reason: {reason}, Severity: {severity:.2f}")
    print()
    
    # Test with spike
    print("Test 2: Cost spike")
    is_anomaly, reason, severity = detector.detect_anomaly("test_op", 5.00, 10000)
    print(f"  Anomaly: {is_anomaly}, Reason: {reason}, Severity: {severity:.2f}")
    print()
    
    # Generate report
    print(detector.generate_report())


if __name__ == "__main__":
    main()
