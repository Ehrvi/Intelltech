"""
MOTHER V5 - Semantic Search

NLP-powered knowledge retrieval using vector embeddings.
Simplified version using OpenAI embeddings (no heavy dependencies).
"""

from typing import List, Tuple, Dict
from dataclasses import dataclass
import json
import os
from openai import OpenAI
import numpy as np


@dataclass
class SearchResult:
    """Search result with relevance score"""
    document: str
    score: float
    metadata: Dict


class SemanticSearch:
    """
    Semantic search using vector embeddings.
    
    Uses OpenAI embeddings for simplicity (no need for sentence-transformers).
    """
    
    def __init__(self, knowledge_base_path: str = None):
        """
        Initialize Semantic Search.
        
        Args:
            knowledge_base_path: Path to knowledge base directory
        """
        self.client = OpenAI()
        self.kb_path = knowledge_base_path or "/home/ubuntu/manus_global_knowledge/docs"
        self.documents: List[str] = []
        self.embeddings: List[List[float]] = []
        self.metadata: List[Dict] = []
        self.index_path = "/home/ubuntu/manus_global_knowledge/mother_v5/domain/models/semantic_index.json"
    
    def index_documents(self, documents: List[str], metadata: List[Dict] = None):
        """
        Create vector index of documents.
        
        Args:
            documents: List of document texts
            metadata: Optional metadata for each document
        """
        self.documents = documents
        self.metadata = metadata or [{} for _ in documents]
        
        # Generate embeddings using OpenAI
        print(f"Generating embeddings for {len(documents)} documents...")
        self.embeddings = []
        
        # Batch process (OpenAI supports batch embeddings)
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            batch_embeddings = self._get_embeddings(batch)
            self.embeddings.extend(batch_embeddings)
        
        # Save index
        self.save_index()
        print(f"Index created with {len(self.embeddings)} embeddings")
    
    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings from OpenAI.
        
        Args:
            texts: List of texts
            
        Returns:
            List of embedding vectors
        """
        # Use OpenAI's embedding model
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        
        return [item.embedding for item in response.data]
    
    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """
        Find most relevant documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of search results
        """
        if not self.embeddings:
            self.load_index()
        
        if not self.embeddings:
            return []
        
        # Get query embedding
        query_embedding = self._get_embeddings([query])[0]
        
        # Calculate cosine similarity with all documents
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            similarities.append((i, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k results
        results = []
        for i, score in similarities[:top_k]:
            results.append(SearchResult(
                document=self.documents[i],
                score=score,
                metadata=self.metadata[i]
            ))
        
        return results
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity (0-1)
        """
        # Convert to numpy arrays
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        # Cosine similarity
        dot_product = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        
        return dot_product / (norm1 * norm2)
    
    def save_index(self):
        """Save index to disk"""
        index_data = {
            "documents": self.documents,
            "embeddings": self.embeddings,
            "metadata": self.metadata
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
        
        self.documents = index_data.get("documents", [])
        self.embeddings = index_data.get("embeddings", [])
        self.metadata = index_data.get("metadata", [])
    
    def index_knowledge_base(self):
        """
        Index all documents in knowledge base.
        """
        documents = []
        metadata = []
        
        # Walk through knowledge base directory
        for root, dirs, files in os.walk(self.kb_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                            # Split into chunks (1000 chars each)
                            chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
                            
                            for chunk_idx, chunk in enumerate(chunks):
                                documents.append(chunk)
                                metadata.append({
                                    "file": file_path,
                                    "chunk": chunk_idx
                                })
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
        
        print(f"Found {len(documents)} document chunks")
        self.index_documents(documents, metadata)


# Example usage
if __name__ == "__main__":
    search = SemanticSearch()
    
    # Example documents
    documents = [
        "Reinforcement learning is a type of machine learning where agents learn by interacting with an environment.",
        "Content marketing involves creating valuable content to attract and engage a target audience.",
        "Venture capital is a form of private equity financing for startups with high growth potential.",
        "Semantic search uses natural language processing to understand the meaning of queries.",
        "SHMS (Structural Health Monitoring System) uses sensors to monitor the condition of structures."
    ]
    
    # Index documents
    search.index_documents(documents)
    
    # Search
    query = "How does machine learning work?"
    results = search.search(query, top_k=3)
    
    print(f"\nQuery: {query}\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. Score: {result.score:.3f}")
        print(f"   {result.document[:100]}...\n")
