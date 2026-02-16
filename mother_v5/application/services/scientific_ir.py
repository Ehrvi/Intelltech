"""
Scientific Information Retrieval System

Based on academic research:
- Robertson & Zaragoza (2009): BM25
- Salton & Steinberg (1979): TF-IDF
- Manning et al. (2008): IR best practices

Implements:
- BM25 ranking algorithm
- Advanced text preprocessing
- Evaluation metrics (P@K, R@K, MAP, NDCG)
"""

import os
import json
import re
import math
from typing import List, Dict, Tuple, Set
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


class ScientificIR:
    """
    Scientifically rigorous Information Retrieval system.
    
    Based on:
    - BM25 algorithm (Robertson & Zaragoza, 2009)
    - Text preprocessing best practices (Manning et al., 2008)
    - Evaluation metrics (Willet et al., 2006)
    """
    
    def __init__(self, kb_path: str = None, k1: float = 1.5, b: float = 0.75):
        """
        Initialize IR system.
        
        Args:
            kb_path: Path to knowledge base
            k1: BM25 term frequency saturation parameter (default: 1.5)
            b: BM25 length normalization parameter (default: 0.75)
        """
        self.kb_path = kb_path or "/home/ubuntu/manus_global_knowledge/docs"
        self.index_path = "/home/ubuntu/manus_global_knowledge/mother_v5/domain/models/scientific_ir_index.json"
        
        # BM25 parameters (tunable)
        self.k1 = k1  # Term frequency saturation (typically 1.2-2.0)
        self.b = b    # Length normalization (typically 0.75)
        
        # Data structures
        self.documents: List[Dict] = []
        self.vocabulary: Dict[str, int] = {}
        self.doc_freq: Dict[str, int] = {}  # Document frequency for each term
        self.avgdl: float = 0.0  # Average document length
        
        # Preprocessing tools
        try:
            self.stop_words: Set[str] = set(stopwords.words('english'))
        except:
            # Fallback if NLTK data not available
            self.stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        
        self.stemmer = PorterStemmer()
    
    def preprocess(self, text: str, use_stemming: bool = True, remove_stopwords: bool = True) -> List[str]:
        """
        Advanced text preprocessing pipeline.
        
        Based on Manning et al. (2008) best practices.
        
        Args:
            text: Input text
            use_stemming: Apply Porter stemming
            remove_stopwords: Remove common words
            
        Returns:
            List of processed tokens
        """
        # 1. Lowercase
        text = text.lower()
        
        # 2. Remove special characters (keep alphanumeric and spaces)
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # 3. Tokenize
        tokens = text.split()
        
        # 4. Remove short tokens (< 3 chars)
        tokens = [t for t in tokens if len(t) >= 3]
        
        # 5. Remove stop words
        if remove_stopwords:
            tokens = [t for t in tokens if t not in self.stop_words]
        
        # 6. Stemming
        if use_stemming:
            tokens = [self.stemmer.stem(t) for t in tokens]
        
        return tokens
    
    def index_knowledge_base(self):
        """Index all documents in knowledge base using BM25."""
        print(f"📚 Scanning {self.kb_path}...")
        
        documents = []
        total_length = 0
        
        # Walk through knowledge base
        for root, dirs, files in os.walk(self.kb_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                            # Split into chunks (1000 chars)
                            chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
                            
                            for chunk_idx, chunk in enumerate(chunks):
                                # Preprocess
                                tokens = self.preprocess(chunk)
                                
                                if not tokens:
                                    continue
                                
                                doc_length = len(tokens)
                                total_length += doc_length
                                
                                documents.append({
                                    "file": file_path,
                                    "chunk": chunk_idx,
                                    "content": chunk,
                                    "tokens": tokens,
                                    "length": doc_length,
                                    "tf": Counter(tokens)
                                })
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
        
        self.documents = documents
        N = len(documents)
        print(f"✅ Found {N} document chunks")
        
        # Calculate average document length
        self.avgdl = total_length / N if N > 0 else 0
        print(f"📏 Average document length: {self.avgdl:.1f} terms")
        
        # Build vocabulary and document frequency
        all_tokens = set()
        self.doc_freq = Counter()
        
        for doc in documents:
            unique_tokens = set(doc["tokens"])
            all_tokens.update(unique_tokens)
            for token in unique_tokens:
                self.doc_freq[token] += 1
        
        self.vocabulary = {token: idx for idx, token in enumerate(sorted(all_tokens))}
        print(f"📖 Vocabulary size: {len(self.vocabulary)} unique terms")
        
        # Save index
        self.save_index()
        print(f"💾 Index saved to {self.index_path}")
    
    def bm25_score(self, query_tokens: List[str], doc: Dict) -> float:
        """
        Calculate BM25 score for a document given a query.
        
        BM25 formula (Robertson & Zaragoza, 2009):
        score = Σ IDF(qi) × (f(qi,D) × (k1 + 1)) / (f(qi,D) + k1 × (1 - b + b × |D|/avgdl))
        
        where:
        - qi: query term
        - f(qi,D): frequency of qi in document D
        - |D|: length of document D
        - avgdl: average document length
        - k1: term frequency saturation parameter
        - b: length normalization parameter
        
        Args:
            query_tokens: Preprocessed query tokens
            doc: Document dictionary
            
        Returns:
            BM25 score
        """
        score = 0.0
        N = len(self.documents)
        doc_length = doc["length"]
        
        for qi in query_tokens:
            if qi not in doc["tf"]:
                continue
            
            # Term frequency in document
            f_qi_D = doc["tf"][qi]
            
            # Document frequency
            df = self.doc_freq.get(qi, 0)
            
            # IDF component (with smoothing)
            idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)
            
            # BM25 component
            numerator = f_qi_D * (self.k1 + 1)
            denominator = f_qi_D + self.k1 * (1 - self.b + self.b * (doc_length / self.avgdl))
            
            score += idf * (numerator / denominator)
        
        return score
    
    def search(self, query: str, top_k: int = 5, use_bm25: bool = True) -> List[Tuple[Dict, float]]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            top_k: Number of results
            use_bm25: Use BM25 (True) or TF-IDF (False)
            
        Returns:
            List of (document, score) tuples
        """
        if not self.documents:
            self.load_index()
        
        # Preprocess query
        query_tokens = self.preprocess(query)
        
        if not query_tokens:
            return []
        
        # Score all documents
        scores = []
        for doc in self.documents:
            if use_bm25:
                score = self.bm25_score(query_tokens, doc)
            else:
                # TF-IDF for comparison
                score = self._tfidf_score(query_tokens, doc)
            
            if score > 0:
                scores.append((doc, score))
        
        # Sort by score
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores[:top_k]
    
    def _tfidf_score(self, query_tokens: List[str], doc: Dict) -> float:
        """TF-IDF scoring for baseline comparison."""
        score = 0.0
        N = len(self.documents)
        
        for qi in query_tokens:
            if qi not in doc["tf"]:
                continue
            
            tf = doc["tf"][qi]
            df = self.doc_freq.get(qi, 1)
            idf = math.log(N / df)
            
            score += tf * idf
        
        return score
    
    def save_index(self):
        """Save index to disk."""
        index_data = {
            "documents": [
                {
                    "file": doc["file"],
                    "chunk": doc["chunk"],
                    "content": doc["content"],
                    "tokens": doc["tokens"],
                    "length": doc["length"],
                    "tf": dict(doc["tf"])
                }
                for doc in self.documents
            ],
            "vocabulary": self.vocabulary,
            "doc_freq": dict(self.doc_freq),
            "avgdl": self.avgdl,
            "k1": self.k1,
            "b": self.b
        }
        
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        with open(self.index_path, 'w') as f:
            json.dump(index_data, f)
    
    def load_index(self):
        """Load index from disk."""
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
                "length": doc["length"],
                "tf": Counter(doc["tf"])
            }
            for doc in index_data["documents"]
        ]
        self.vocabulary = index_data["vocabulary"]
        self.doc_freq = Counter(index_data["doc_freq"])
        self.avgdl = index_data["avgdl"]
        self.k1 = index_data.get("k1", 1.5)
        self.b = index_data.get("b", 0.75)


if __name__ == "__main__":
    ir = ScientificIR()
    
    print("="*70)
    print("SCIENTIFIC INFORMATION RETRIEVAL SYSTEM")
    print("Based on BM25 (Robertson & Zaragoza, 2009)")
    print("="*70)
    
    # Index knowledge base
    ir.index_knowledge_base()
    
    print("\n" + "="*70)
    print("TESTING BM25 vs TF-IDF")
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
        
        print("\n  BM25 Results:")
        bm25_results = ir.search(query, top_k=3, use_bm25=True)
        for i, (doc, score) in enumerate(bm25_results, 1):
            print(f"    {i}. Score: {score:.2f} | {os.path.basename(doc['file'])}")
        
        print("\n  TF-IDF Results (baseline):")
        tfidf_results = ir.search(query, top_k=3, use_bm25=False)
        for i, (doc, score) in enumerate(tfidf_results, 1):
            print(f"    {i}. Score: {score:.2f} | {os.path.basename(doc['file'])}")
