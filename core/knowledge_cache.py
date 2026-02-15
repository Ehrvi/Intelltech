#!/usr/bin/env python3
"""
Knowledge Cache with Semantic Search

Prevents duplicate work by caching and reusing previous results.
Fixes BUG-005: No Knowledge Reuse

Based on: Reimers, N. & Gurevych, I. (2019). "Sentence-BERT: Sentence 
Embeddings using Siamese BERT-Networks"
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from openai import OpenAI

class KnowledgeCache:
    """Semantic knowledge cache for reusing previous work"""
    
    def __init__(self, base_path: Path = Path("/home/ubuntu/manus_global_knowledge")):
        self.base_path = base_path
        self.cache_dir = base_path / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        self.cache_file = self.cache_dir / "knowledge.jsonl"
        self.embeddings_file = self.cache_dir / "embeddings.jsonl"
        
        self.client = OpenAI()
        self.similarity_threshold = 0.85  # 85% similarity = cache hit
    
    def search(self, query: str) -> Optional[Dict]:
        """
        Search cache for similar queries
        
        Args:
            query: The query to search for
        
        Returns:
            Cached result if found, None otherwise
        """
        if not self.cache_file.exists():
            return None
        
        # Get query embedding
        query_embedding = self._get_embedding(query)
        
        # Search through cache
        best_match = None
        best_similarity = 0
        
        with open(self.cache_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                
                # Calculate similarity
                cached_embedding = entry.get('embedding')
                if cached_embedding:
                    similarity = self._cosine_similarity(query_embedding, cached_embedding)
                    
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match = entry
        
        # Return if similarity exceeds threshold
        if best_similarity >= self.similarity_threshold:
            return {
                'query': best_match['query'],
                'result': best_match['result'],
                'timestamp': best_match['timestamp'],
                'similarity': best_similarity,
                'cache_hit': True
            }
        
        return None
    
    def save(self, query: str, result: str, metadata: Optional[Dict] = None):
        """
        Save query and result to cache
        
        Args:
            query: The original query
            result: The result/answer
            metadata: Optional metadata
        """
        # Get embedding
        embedding = self._get_embedding(query)
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'result': result,
            'embedding': embedding,
            'metadata': metadata or {}
        }
        
        # Append to cache
        with open(self.cache_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding vector for text using OpenAI"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            # Fallback: return zero vector if embedding fails
            return [0.0] * 1536
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        if not self.cache_file.exists():
            return {
                'total_entries': 0,
                'cache_size_kb': 0
            }
        
        # Count entries
        with open(self.cache_file, 'r') as f:
            entries = sum(1 for _ in f)
        
        # Get file size
        size_kb = self.cache_file.stat().st_size / 1024
        
        return {
            'total_entries': entries,
            'cache_size_kb': size_kb
        }
    
    def clear_old_entries(self, days: int = 30):
        """Remove entries older than N days"""
        if not self.cache_file.exists():
            return
        
        cutoff = datetime.now().timestamp() - (days * 86400)
        
        # Read all entries
        entries = []
        with open(self.cache_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                timestamp = datetime.fromisoformat(entry['timestamp']).timestamp()
                if timestamp > cutoff:
                    entries.append(entry)
        
        # Rewrite file with only recent entries
        with open(self.cache_file, 'w') as f:
            for entry in entries:
                f.write(json.dumps(entry) + '\n')


# Convenience functions
_cache = None

def get_cache() -> KnowledgeCache:
    """Get the global cache instance"""
    global _cache
    if _cache is None:
        _cache = KnowledgeCache()
    return _cache


def search_cache(query: str) -> Optional[Dict]:
    """Quick cache search"""
    return get_cache().search(query)


def save_to_cache(query: str, result: str, metadata: Optional[Dict] = None):
    """Quick cache save"""
    get_cache().save(query, result, metadata)


if __name__ == '__main__':
    # Demo usage
    cache = KnowledgeCache()
    
    print("Testing Knowledge Cache...")
    print("=" * 70)
    
    # Save some knowledge
    print("Saving knowledge to cache...")
    cache.save(
        query="What are the top AI companies?",
        result="OpenAI, Google DeepMind, Anthropic, Microsoft, Meta",
        metadata={'source': 'research', 'quality': 95}
    )
    
    # Search for exact match
    print("\nSearching for exact match...")
    result = cache.search("What are the top AI companies?")
    if result:
        print(f"✅ Cache hit! Similarity: {result['similarity']:.2%}")
        print(f"   Result: {result['result']}")
    else:
        print("❌ Cache miss")
    
    # Search for similar query
    print("\nSearching for similar query...")
    result = cache.search("List the best AI companies")
    if result:
        print(f"✅ Cache hit! Similarity: {result['similarity']:.2%}")
        print(f"   Result: {result['result']}")
    else:
        print("❌ Cache miss")
    
    # Get stats
    print("\nCache statistics:")
    stats = cache.get_stats()
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Cache size: {stats['cache_size_kb']:.2f} KB")
    
    print("=" * 70)
