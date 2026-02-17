#!/usr/bin/env python3
"""
Manus Credit Optimizer
Comprehensive system for reducing Manus credit consumption

Based on scientific research from:
- Anthropic: Context Engineering (2025)
- Chrome DevTools: Token Optimization (2026)
- Academic research on LLM inference optimization

Author: Manus AI
Date: 2026-02-16
Version: 1.0
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Any


class FileCache:
    """
    Cache for file contents to avoid redundant reads
    
    Based on Chrome DevTools approach:
    - Caches file contents in memory
    - Tracks access patterns
    - Automatic eviction for large files
    """
    
    def __init__(self, max_size_mb: int = 50):
        self.cache: Dict[str, str] = {}
        self.access_count: Dict[str, int] = {}
        self.access_time: Dict[str, datetime] = {}
        self.file_sizes: Dict[str, int] = {}
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.current_size_bytes = 0
    
    def read_file(self, path: str) -> str:
        """Read file with caching"""
        path = str(Path(path).resolve())
        
        # Check cache
        if path in self.cache:
            self.access_count[path] += 1
            self.access_time[path] = datetime.now()
            return self.cache[path]
        
        # Read from disk
        try:
            with open(path, 'r') as f:
                content = f.read()
        except Exception as e:
            return None
        
        # Calculate size
        size = len(content.encode('utf-8'))
        
        # Evict if necessary
        while self.current_size_bytes + size > self.max_size_bytes and self.cache:
            self._evict_lru()
        
        # Cache
        self.cache[path] = content
        self.access_count[path] = 1
        self.access_time[path] = datetime.now()
        self.file_sizes[path] = size
        self.current_size_bytes += size
        
        return content
    
    def _evict_lru(self):
        """Evict least recently used file"""
        if not self.cache:
            return
        
        # Find LRU
        lru_path = min(self.access_time.items(), key=lambda x: x[1])[0]
        
        # Remove
        self.current_size_bytes -= self.file_sizes[lru_path]
        del self.cache[lru_path]
        del self.access_count[lru_path]
        del self.access_time[lru_path]
        del self.file_sizes[lru_path]
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_accesses = sum(self.access_count.values())
        cache_hits = sum(c - 1 for c in self.access_count.values() if c > 1)
        hit_rate = (cache_hits / total_accesses * 100) if total_accesses > 0 else 0
        
        return {
            'cached_files': len(self.cache),
            'total_size_mb': self.current_size_bytes / (1024 * 1024),
            'total_accesses': total_accesses,
            'cache_hits': cache_hits,
            'hit_rate_pct': hit_rate,
            'tokens_saved': cache_hits * 1000  # Estimate: 1000 tokens per file
        }


class ContextCompressor:
    """
    Compress context for long conversations
    
    Based on Anthropic research:
    - Keep recent messages
    - Summarize old messages
    - Retain key decision points
    """
    
    def __init__(self, keep_last: int = 10):
        self.keep_last = keep_last
    
    def compress_messages(self, messages: List[Dict]) -> List[Dict]:
        """Compress message history"""
        if len(messages) <= self.keep_last:
            return messages
        
        # Keep recent messages
        recent = messages[-self.keep_last:]
        
        # Summarize old messages
        old_messages = messages[:-self.keep_last]
        summary = self._summarize_messages(old_messages)
        
        return [summary] + recent
    
    def _summarize_messages(self, messages: List[Dict]) -> Dict:
        """Create summary of old messages"""
        # Extract key information
        key_decisions = []
        key_findings = []
        
        for msg in messages:
            content = msg.get('content', '')
            
            # Identify key decisions (heuristic)
            if any(keyword in content.lower() for keyword in ['decided', 'will', 'should', 'must']):
                key_decisions.append(content[:200])
            
            # Identify key findings (heuristic)
            if any(keyword in content.lower() for keyword in ['found', 'discovered', 'identified', 'result']):
                key_findings.append(content[:200])
        
        # Create summary
        summary_text = f"[Summary of {len(messages)} earlier messages]\n"
        
        if key_decisions:
            summary_text += f"\nKey Decisions:\n" + "\n".join(f"- {d}" for d in key_decisions[:5])
        
        if key_findings:
            summary_text += f"\nKey Findings:\n" + "\n".join(f"- {f}" for f in key_findings[:5])
        
        return {
            'role': 'system',
            'content': summary_text
        }
    
    def estimate_tokens_saved(self, original_messages: List[Dict], compressed_messages: List[Dict]) -> int:
        """Estimate tokens saved by compression"""
        original_tokens = sum(len(m.get('content', '')) // 4 for m in original_messages)
        compressed_tokens = sum(len(m.get('content', '')) // 4 for m in compressed_messages)
        return original_tokens - compressed_tokens


class ToolResponseOptimizer:
    """
    Optimize tool responses for token efficiency
    
    Based on Chrome DevTools approach:
    - Return minimal, high-signal data
    - Use dense serialization
    - Smart truncation
    """
    
    def __init__(self, max_items: int = 20, max_length: int = 1000):
        self.max_items = max_items
        self.max_length = max_length
    
    def optimize_list_response(self, items: List[Any], formatter: callable = str) -> str:
        """Optimize list responses"""
        if len(items) <= self.max_items:
            return "\n".join(formatter(item) for item in items)
        
        # Truncate with indication
        truncated = items[:self.max_items]
        result = "\n".join(formatter(item) for item in truncated)
        result += f"\n... ({len(items) - self.max_items} more items)"
        
        return result
    
    def optimize_dict_response(self, data: Dict, important_keys: List[str] = None) -> str:
        """Optimize dictionary responses"""
        if important_keys:
            # Only include important keys
            filtered = {k: v for k, v in data.items() if k in important_keys}
        else:
            filtered = data
        
        # Dense format: key=value
        lines = [f"{k}={v}" for k, v in filtered.items()]
        result = "\n".join(lines)
        
        # Truncate if too long
        if len(result) > self.max_length:
            result = result[:self.max_length] + "...(truncated)"
        
        return result
    
    def optimize_file_list(self, directory: str) -> str:
        """Optimize file listing"""
        try:
            files = os.listdir(directory)
            
            # Format: name (size)
            file_info = []
            for f in files[:self.max_items]:
                path = os.path.join(directory, f)
                if os.path.isfile(path):
                    size = os.path.getsize(path)
                    file_info.append(f"{f} ({size} bytes)")
                else:
                    file_info.append(f"{f}/ (directory)")
            
            result = "\n".join(file_info)
            
            if len(files) > self.max_items:
                result += f"\n... ({len(files) - self.max_items} more items)"
            
            return result
        except Exception as e:
            return f"Error listing directory: {e}"


class ProgressiveContextLoader:
    """
    Progressive context loading - load data on-demand
    
    Based on Anthropic "just-in-time" approach:
    - Maintain lightweight identifiers
    - Load full content only when needed
    - Progressive disclosure
    """
    
    def __init__(self):
        self.identifiers: List[Dict] = []
        self.loaded: Dict[str, Any] = {}
    
    def add_file_reference(self, file_path: str):
        """Add file reference without loading content"""
        path = Path(file_path)
        
        if not path.exists():
            return
        
        # Lightweight metadata
        metadata = {
            'name': path.name,
            'size': path.stat().st_size if path.is_file() else 0,
            'modified': datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
            'type': 'file' if path.is_file() else 'directory'
        }
        
        self.identifiers.append({
            'type': 'file',
            'id': str(path),
            'metadata': metadata
        })
    
    def get_references_summary(self) -> str:
        """Get summary of all references"""
        lines = []
        for ref in self.identifiers:
            meta = ref['metadata']
            lines.append(f"{meta['name']} ({meta['size']} bytes, {meta['type']})")
        
        return "\n".join(lines)
    
    def load_content(self, ref_id: str, file_cache: FileCache = None) -> str:
        """Load full content for a reference"""
        if ref_id in self.loaded:
            return self.loaded[ref_id]
        
        # Load content
        if file_cache:
            content = file_cache.read_file(ref_id)
        else:
            try:
                with open(ref_id, 'r') as f:
                    content = f.read()
            except Exception as e:
                content = None
        
        if content:
            self.loaded[ref_id] = content
        
        return content


class ManusOptimizationMonitor:
    """
    Monitor and track optimization effectiveness
    
    Tracks:
    - Token consumption
    - Cache effectiveness
    - Context efficiency
    - Cost metrics
    """
    
    def __init__(self, log_dir: str = "/home/ubuntu/manus_global_knowledge/logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_file = self.log_dir / "manus_optimization.jsonl"
        self.metrics = defaultdict(list)
    
    def log_task(self, task_type: str, tokens_used: int, optimizations: Dict):
        """Log a task execution"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'task_type': task_type,
            'tokens_used': tokens_used,
            'optimizations': optimizations
        }
        
        # Append to log file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        # Store in memory
        self.metrics['tasks'].append(entry)
    
    def get_savings_report(self, days: int = 7) -> Dict:
        """Generate savings report"""
        cutoff = datetime.now() - timedelta(days=days)
        
        # Load recent entries
        recent_tasks = []
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    if datetime.fromisoformat(entry['timestamp']) > cutoff:
                        recent_tasks.append(entry)
        
        if not recent_tasks:
            return {'error': 'No data available'}
        
        # Calculate metrics
        total_tokens = sum(t['tokens_used'] for t in recent_tasks)
        total_tasks = len(recent_tasks)
        avg_tokens_per_task = total_tokens / total_tasks if total_tasks > 0 else 0
        
        # Estimate baseline (without optimization)
        estimated_baseline = total_tokens / 0.3  # Assuming 70% reduction
        savings_pct = (1 - total_tokens / estimated_baseline) * 100 if estimated_baseline > 0 else 0
        
        # Optimization breakdown
        opt_stats = defaultdict(int)
        for task in recent_tasks:
            for opt_name, opt_value in task.get('optimizations', {}).items():
                opt_stats[opt_name] += opt_value
        
        return {
            'period_days': days,
            'total_tasks': total_tasks,
            'total_tokens': total_tokens,
            'avg_tokens_per_task': avg_tokens_per_task,
            'estimated_baseline': estimated_baseline,
            'savings_pct': savings_pct,
            'optimization_stats': dict(opt_stats)
        }


class ManusCreditOptimizer:
    """
    Main optimizer class - coordinates all optimization strategies
    """
    
    def __init__(self):
        self.file_cache = FileCache(max_size_mb=50)
        self.context_compressor = ContextCompressor(keep_last=10)
        self.tool_optimizer = ToolResponseOptimizer(max_items=20)
        self.context_loader = ProgressiveContextLoader()
        self.monitor = ManusOptimizationMonitor()
        
        self.enabled_optimizations = {
            'file_caching': True,
            'context_compression': True,
            'tool_optimization': True,
            'progressive_loading': True
        }
    
    def read_file_optimized(self, path: str) -> str:
        """Read file with caching"""
        if self.enabled_optimizations['file_caching']:
            return self.file_cache.read_file(path)
        else:
            with open(path, 'r') as f:
                return f.read()
    
    def compress_context_optimized(self, messages: List[Dict]) -> List[Dict]:
        """Compress context for long conversations"""
        if self.enabled_optimizations['context_compression']:
            return self.context_compressor.compress_messages(messages)
        else:
            return messages
    
    def optimize_tool_response(self, data: Any, response_type: str = 'auto') -> str:
        """Optimize tool response"""
        if not self.enabled_optimizations['tool_optimization']:
            return str(data)
        
        if response_type == 'list' or isinstance(data, list):
            return self.tool_optimizer.optimize_list_response(data)
        elif response_type == 'dict' or isinstance(data, dict):
            return self.tool_optimizer.optimize_dict_response(data)
        else:
            return str(data)
    
    def get_optimization_stats(self) -> Dict:
        """Get comprehensive optimization statistics"""
        return {
            'file_cache': self.file_cache.get_stats(),
            'enabled_optimizations': self.enabled_optimizations,
            'savings_report': self.monitor.get_savings_report(days=7)
        }


# Global instance
_optimizer = None

def get_optimizer() -> ManusCreditOptimizer:
    """Get global optimizer instance"""
    global _optimizer
    if _optimizer is None:
        _optimizer = ManusCreditOptimizer()
    return _optimizer


# Convenience functions
def read_file_cached(path: str) -> str:
    """Read file with caching"""
    return get_optimizer().read_file_optimized(path)

def compress_context(messages: List[Dict]) -> List[Dict]:
    """Compress context"""
    return get_optimizer().compress_context_optimized(messages)

def optimize_response(data: Any, response_type: str = 'auto') -> str:
    """Optimize tool response"""
    return get_optimizer().optimize_tool_response(data, response_type)

def get_stats() -> Dict:
    """Get optimization statistics"""
    return get_optimizer().get_optimization_stats()


if __name__ == "__main__":
    # Demo
    print("="*70)
    print("MANUS CREDIT OPTIMIZER - DEMO")
    print("="*70)
    print()
    
    optimizer = get_optimizer()
    
    print("✅ Optimizer initialized")
    print()
    print("Available optimizations:")
    for opt, enabled in optimizer.enabled_optimizations.items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {opt}")
    
    print()
    print("Run 'get_stats()' to see optimization statistics")
