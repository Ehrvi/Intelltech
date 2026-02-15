#!/usr/bin/env python3
"""
Knowledge Cache with In-Memory Indexing and Retry Logic

Adds resilience to network errors by implementing retry logic for embedding generation.
"""

import json
import numpy as np
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from openai import OpenAI, APIConnectionError

class KnowledgeCache:
    """A semantic knowledge cache using an in-memory vector index."""
    
    def __init__(self, base_path: Path = Path("/home/ubuntu/manus_global_knowledge"), similarity_threshold: float = 0.85):
        self.base_path = base_path
        self.cache_dir = base_path / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "knowledge_cache.jsonl"
        
        self.client = OpenAI()
        self.similarity_threshold = similarity_threshold
        
        self._embeddings: Optional[np.ndarray] = None
        self._metadata: List[Dict] = []
        self._load_cache_into_memory()

    def _load_cache_into_memory(self):
        if not self.cache_file.exists():
            return
        embeddings, metadata = [], []
        with self.cache_file.open("r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if "embedding" in entry and "query" in entry:
                        embeddings.append(entry["embedding"])
                        meta = {k: v for k, v in entry.items() if k != "embedding"}
                        metadata.append(meta)
                except json.JSONDecodeError:
                    continue
        if embeddings:
            self._embeddings = np.array(embeddings, dtype=np.float32)
            self._metadata = metadata

    def search(self, query: str) -> Optional[Dict]:
        if self._embeddings is None or len(self._embeddings) == 0:
            return None

        query_embedding = self._get_embedding_with_retry(query)
        if query_embedding is None:
            return None

        similarities = self._cosine_similarity_numpy(np.array(query_embedding, dtype=np.float32), self._embeddings)
        best_index = np.argmax(similarities)
        best_similarity = similarities[best_index]

        if best_similarity >= self.similarity_threshold:
            best_match_meta = self._metadata[best_index]
            return {**best_match_meta, "similarity": float(best_similarity), "cache_hit": True}
        
        return None

    def save(self, query: str, result: str, metadata: Optional[Dict] = None):
        embedding = self._get_embedding_with_retry(query)
        if embedding is None:
            print(f"Skipping cache save for query \"{query}\" due to embedding failure.")
            return

        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "result": result,
            "embedding": embedding,
            "metadata": metadata or {}
        }
        
        with self.cache_file.open("a") as f:
            f.write(json.dumps(entry) + "\n")
        
        embedding_np = np.array([embedding], dtype=np.float32)
        if self._embeddings is None:
            self._embeddings = embedding_np
        else:
            self._embeddings = np.vstack([self._embeddings, embedding_np])
        
        self._metadata.append({k: v for k, v in entry.items() if k != "embedding"})

    def _get_embedding_with_retry(self, text: str, max_retries: int = 3, delay: float = 1.0) -> Optional[List[float]]:
        """Gets an embedding with retry logic for transient network errors."""
        for attempt in range(max_retries):
            try:
                response = self.client.embeddings.create(model="text-embedding-3-small", input=text.strip())
                return response.data[0].embedding
            except APIConnectionError as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
            except Exception as e:
                print(f"An unexpected error occurred while getting embedding: {e}")
                return None
        print(f"Failed to get embedding for \"{text}\" after {max_retries} attempts.")
        return None

    def _cosine_similarity_numpy(self, vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
        vec1_norm = np.linalg.norm(vec1)
        if vec1_norm == 0: return np.zeros(vec2.shape[0])
        vec2_norm = np.linalg.norm(vec2, axis=1)
        vec2_norm[vec2_norm == 0] = 1e-9
        return np.dot(vec2, vec1) / (vec1_norm * vec2_norm)

_cache_instance: Optional[KnowledgeCache] = None

def get_cache() -> KnowledgeCache:
    global _cache_instance
    if _cache_instance is None:
        try:
            import numpy
        except ImportError:
            import subprocess, sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
        _cache_instance = KnowledgeCache()
    return _cache_instance
