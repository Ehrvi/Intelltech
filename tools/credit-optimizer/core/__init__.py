"""
Manus Global Knowledge System - Core Module
Includes cost optimization for Manus credits
"""

from .manus_credit_optimizer import (
    get_optimizer,
    read_file_cached,
    compress_context,
    optimize_response,
    get_stats
)

__all__ = [
    'get_optimizer',
    'read_file_cached',
    'compress_context',
    'optimize_response',
    'get_stats'
]
