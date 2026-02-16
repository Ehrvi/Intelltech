import logging
#!/usr/bin/env python3
"""
Knowledge Lookup - Refactored

Uses the centralized, in-memory KnowledgeCache for fast, semantic searches,
replacing the slow, keyword-based file search.
"""

from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass
from core.knowledge_cache import get_cache, KnowledgeCache

@dataclass
class KnowledgeResult:
    """Represents a unified knowledge search result from the cache."""
    location: str
    relevance_score: float
    excerpt: str
    source: str = "cache"

class KnowledgeLookup:
    """Leverages the KnowledgeCache to find existing knowledge before execution."""

    def __init__(self):
        """Initializes the lookup component by getting the global cache instance."""
        self.cache: KnowledgeCache = get_cache()

    def mandatory_lookup(self, task_description: str) -> Tuple[bool, Optional[KnowledgeResult]]:
        """
        Performs a mandatory search in the knowledge cache.

        Args:
            task_description: A natural language description of the task.

        Returns:
            A tuple of (found, result), where found is True if a relevant item
            was found in the cache, and result is the KnowledgeResult object.
        """
        search_result = self.cache.search(task_description)

        if search_result and search_result.get("cache_hit"):
            # Adapt the cache result to the KnowledgeResult format
            result = KnowledgeResult(
                location=search_result.get("metadata", {}).get("source_file", "N/A"),
                relevance_score=search_result.get("similarity", 0.0),
                excerpt=search_result.get("result", "")[:500] # Truncate for brevity
            )
            return (True, result)

        return (False, None)

# --- Test Execution ---
if __name__ == "__main__":
    from unittest.mock import patch

    print("="*70)
    print("🔍 MANDATORY KNOWLEDGE LOOKUP - REFACTORED")
    print("="*70)

    # Mock the cache search for a predictable test
    with patch.object(KnowledgeCache, 'search') as mock_search:
        # --- Test Case 1: Cache Hit ---
        print("\nTesting a query that should result in a cache hit...")
        mock_search.return_value = {
            "cache_hit": True,
            "query": "Como funciona o sistema de inicialização?",
            "result": "O sistema de inicialização é ativado pelo bootstrap.sh, que executa o mandatory_init.py.",
            "similarity": 0.95,
            "metadata": {"source_file": "/home/ubuntu/manus_global_knowledge/INITIALIZER.md"}
        }

        lookup = KnowledgeLookup()
        found, result = lookup.mandatory_lookup("Como o sistema é inicializado?")

        if found and result:
            print("✅ FOUND: Existing knowledge exists!")
            print(f"   Relevance: {result.relevance_score:.2%}")
            print(f"   Location: {result.location}")
            print(f"   Excerpt: \"{result.excerpt}\"")
        else:
            print("❌ FAILED: Expected a cache hit but got a miss.")

        # --- Test Case 2: Cache Miss ---
        print("\nTesting a query that should result in a cache miss...")
        mock_search.return_value = None

        found_miss, result_miss = lookup.mandatory_lookup("Qual a receita de bolo de chocolate?")

        if not found_miss:
            print("✅ NOT FOUND: No existing knowledge found, as expected.")
        else:
            print("❌ FAILED: Expected a cache miss but got a hit.")

    print("\n✅ Knowledge lookup refactoring test complete!")
