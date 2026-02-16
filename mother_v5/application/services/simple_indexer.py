"""
Simple Knowledge Base Indexer

Creates a searchable index without requiring external APIs.
Uses TF-IDF for relevance scoring.
"""

import os
import json
import re
from typing import List, Dict, Tuple
from collections import Counter
import math


class SimpleIndexer:
    """
    Simple keyword-based indexer using TF-IDF.
    """
    
    def __init__(self, kb_path: str = None):
        """Initialize indexer"""
        self.kb_path = kb_path or "/home/ubuntu/manus_global_knowledge/docs"
        self.index_path = "/home/ubuntu/manus_global_knowledge/mother_v5/domain/models/simple_index.json"
        self.documents: List[Dict] = []
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Convert to lowercase and split
        text = text.lower()
        # Remove special characters except spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        # Split and filter
        tokens = [t for t in text.split() if len(t) > 2]
        return tokens
    
    def index_knowledge_base(self):
        """Index all documents in knowledge base"""
        print(f"📚 Scanning {self.kb_path}...")
        
        documents = []
        
        # Walk through knowledge base
        for root, dirs, files in os.walk(self.kb_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                            # Split into chunks
                            chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
                            
                            for chunk_idx, chunk in enumerate(chunks):
                                tokens = self.tokenize(chunk)
                                documents.append({
                                    "file": file_path,
                                    "chunk": chunk_idx,
                                    "content": chunk,
                                    "tokens": tokens,
                                    "tf": Counter(tokens)
                                })
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
        
        self.documents = documents
        print(f"✅ Found {len(documents)} document chunks")
        
        # Build vocabulary
        all_tokens = set()
        for doc in documents:
            all_tokens.update(doc["tokens"])
        
        self.vocabulary = {token: idx for idx, token in enumerate(sorted(all_tokens))}
        print(f"📖 Vocabulary size: {len(self.vocabulary)} unique terms")
        
        # Calculate IDF
        self._calculate_idf()
        print(f"📊 IDF calculated for {len(self.idf)} terms")
        
        # Save index
        self.save_index()
        print(f"💾 Index saved to {self.index_path}")
    
    def _calculate_idf(self):
        """Calculate inverse document frequency"""
        N = len(self.documents)
        
        # Count documents containing each term
        df = Counter()
        for doc in self.documents:
            unique_tokens = set(doc["tokens"])
            for token in unique_tokens:
                df[token] += 1
        
        # Calculate IDF
        self.idf = {}
        for token, doc_freq in df.items():
            self.idf[token] = math.log(N / doc_freq)
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            List of (document, score) tuples
        """
        if not self.documents:
            self.load_index()
        
        # Tokenize query
        query_tokens = self.tokenize(query)
        query_tf = Counter(query_tokens)
        
        # Calculate query TF-IDF
        query_tfidf = {}
        for token, tf in query_tf.items():
            if token in self.idf:
                query_tfidf[token] = tf * self.idf[token]
        
        # Score all documents
        scores = []
        for doc in self.documents:
            score = 0.0
            for token, query_weight in query_tfidf.items():
                if token in doc["tf"]:
                    doc_weight = doc["tf"][token] * self.idf.get(token, 0)
                    score += query_weight * doc_weight
            
            if score > 0:
                scores.append((doc, score))
        
        # Sort by score
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores[:top_k]
    
    def save_index(self):
        """Save index to disk"""
        index_data = {
            "documents": [
                {
                    "file": doc["file"],
                    "chunk": doc["chunk"],
                    "content": doc["content"],
                    "tokens": doc["tokens"],
                    "tf": dict(doc["tf"])
                }
                for doc in self.documents
            ],
            "vocabulary": self.vocabulary,
            "idf": self.idf
        }
        
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        with open(self.index_path, 'w') as f:
            json.dump(index_data, f)
    
    def load_index(self):
        """Load index from disk"""
        if not os.path.exists(self.index_path):
            return
        
        with open(self.index_path, 'r') as f:
            index_data = json.load(f)
        
        self.documents = [
            {
                "file": doc["file"],
                "chunk": doc["chunk"],
                "content": doc["content"],
                "tokens": doc["tokens"],
                "tf": Counter(doc["tf"])
            }
            for doc in index_data["documents"]
        ]
        self.vocabulary = index_data["vocabulary"]
        self.idf = index_data["idf"]


if __name__ == "__main__":
    indexer = SimpleIndexer()
    
    print("="*70)
    print("SIMPLE KNOWLEDGE BASE INDEXER")
    print("="*70)
    
    # Index knowledge base
    indexer.index_knowledge_base()
    
    print("\n" + "="*70)
    print("TESTING SEARCH")
    print("="*70)
    
    # Test queries
    queries = [
        "reinforcement learning",
        "content marketing",
        "venture capital",
        "software architecture"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: {query}")
        results = indexer.search(query, top_k=3)
        
        for i, (doc, score) in enumerate(results, 1):
            print(f"\n{i}. Score: {score:.2f}")
            print(f"   File: {os.path.basename(doc['file'])}")
            print(f"   Preview: {doc['content'][:100]}...")
