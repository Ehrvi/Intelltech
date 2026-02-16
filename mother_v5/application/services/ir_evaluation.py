"""
Information Retrieval Evaluation Framework

Based on:
- Willet et al. (2006): Evaluation metrics
- Manning et al. (2008): IR evaluation best practices

Implements:
- Precision@K
- Recall@K
- Mean Average Precision (MAP)
- Normalized Discounted Cumulative Gain (NDCG@K)
"""

import math
from typing import List, Dict, Set, Tuple


class IREvaluator:
    """
    IR Evaluation Framework.
    
    Based on standard IR evaluation metrics (Willet et al., 2006).
    """
    
    @staticmethod
    def precision_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
        """
        Precision@K: Fraction of top-K retrieved documents that are relevant.
        
        Formula: P@K = (# relevant docs in top K) / K
        
        Args:
            retrieved: List of retrieved document IDs (ordered by rank)
            relevant: Set of relevant document IDs (ground truth)
            k: Cutoff position
            
        Returns:
            Precision@K score [0, 1]
        """
        if k == 0 or not retrieved:
            return 0.0
        
        top_k = retrieved[:k]
        relevant_in_top_k = sum(1 for doc_id in top_k if doc_id in relevant)
        
        return relevant_in_top_k / k
    
    @staticmethod
    def recall_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
        """
        Recall@K: Fraction of relevant documents found in top-K results.
        
        Formula: R@K = (# relevant docs in top K) / (total # relevant docs)
        
        Args:
            retrieved: List of retrieved document IDs (ordered by rank)
            relevant: Set of relevant document IDs (ground truth)
            k: Cutoff position
            
        Returns:
            Recall@K score [0, 1]
        """
        if not relevant or k == 0:
            return 0.0
        
        top_k = retrieved[:k]
        relevant_in_top_k = sum(1 for doc_id in top_k if doc_id in relevant)
        
        return relevant_in_top_k / len(relevant)
    
    @staticmethod
    def average_precision(retrieved: List[str], relevant: Set[str]) -> float:
        """
        Average Precision: Mean of precision values at each relevant document position.
        
        Formula: AP = (1/|R|) × Σ(P@k × rel(k))
        where:
        - |R| = number of relevant documents
        - P@k = precision at position k
        - rel(k) = 1 if document at position k is relevant, 0 otherwise
        
        Args:
            retrieved: List of retrieved document IDs (ordered by rank)
            relevant: Set of relevant document IDs (ground truth)
            
        Returns:
            Average Precision score [0, 1]
        """
        if not relevant or not retrieved:
            return 0.0
        
        precisions = []
        relevant_count = 0
        
        for k, doc_id in enumerate(retrieved, 1):
            if doc_id in relevant:
                relevant_count += 1
                precision_at_k = relevant_count / k
                precisions.append(precision_at_k)
        
        if not precisions:
            return 0.0
        
        return sum(precisions) / len(relevant)
    
    @staticmethod
    def mean_average_precision(results: Dict[str, List[str]], 
                                ground_truth: Dict[str, Set[str]]) -> float:
        """
        Mean Average Precision (MAP): Mean of AP across all queries.
        
        Formula: MAP = (1/|Q|) × Σ(AP(q))
        where:
        - |Q| = number of queries
        - AP(q) = average precision for query q
        
        Args:
            results: Dict mapping query_id -> list of retrieved doc_ids
            ground_truth: Dict mapping query_id -> set of relevant doc_ids
            
        Returns:
            MAP score [0, 1]
        """
        if not results:
            return 0.0
        
        aps = []
        for query_id, retrieved in results.items():
            relevant = ground_truth.get(query_id, set())
            ap = IREvaluator.average_precision(retrieved, relevant)
            aps.append(ap)
        
        return sum(aps) / len(aps) if aps else 0.0
    
    @staticmethod
    def dcg_at_k(retrieved: List[str], relevance_scores: Dict[str, float], k: int) -> float:
        """
        Discounted Cumulative Gain@K.
        
        Formula: DCG@K = Σ(rel_i / log2(i+1))
        where:
        - rel_i = relevance score of document at position i
        - i = position (1-indexed)
        
        Args:
            retrieved: List of retrieved document IDs (ordered by rank)
            relevance_scores: Dict mapping doc_id -> relevance score
            k: Cutoff position
            
        Returns:
            DCG@K score
        """
        if k == 0 or not retrieved:
            return 0.0
        
        dcg = 0.0
        for i, doc_id in enumerate(retrieved[:k], 1):
            rel = relevance_scores.get(doc_id, 0.0)
            dcg += rel / math.log2(i + 1)
        
        return dcg
    
    @staticmethod
    def ndcg_at_k(retrieved: List[str], relevance_scores: Dict[str, float], k: int) -> float:
        """
        Normalized Discounted Cumulative Gain@K.
        
        Formula: NDCG@K = DCG@K / IDCG@K
        where:
        - DCG@K = actual DCG
        - IDCG@K = ideal DCG (perfect ranking)
        
        Args:
            retrieved: List of retrieved document IDs (ordered by rank)
            relevance_scores: Dict mapping doc_id -> relevance score
            k: Cutoff position
            
        Returns:
            NDCG@K score [0, 1]
        """
        # Calculate DCG
        dcg = IREvaluator.dcg_at_k(retrieved, relevance_scores, k)
        
        # Calculate IDCG (ideal DCG with perfect ranking)
        ideal_ranking = sorted(relevance_scores.keys(), 
                              key=lambda x: relevance_scores[x], 
                              reverse=True)
        idcg = IREvaluator.dcg_at_k(ideal_ranking, relevance_scores, k)
        
        if idcg == 0.0:
            return 0.0
        
        return dcg / idcg
    
    @staticmethod
    def evaluate_system(results: Dict[str, List[str]],
                        ground_truth: Dict[str, Set[str]],
                        k_values: List[int] = [1, 3, 5, 10]) -> Dict:
        """
        Comprehensive evaluation of IR system.
        
        Args:
            results: Dict mapping query_id -> list of retrieved doc_ids
            ground_truth: Dict mapping query_id -> set of relevant doc_ids
            k_values: List of K values for P@K and R@K
            
        Returns:
            Dict with all evaluation metrics
        """
        metrics = {
            "map": IREvaluator.mean_average_precision(results, ground_truth)
        }
        
        # Calculate P@K and R@K for each K
        for k in k_values:
            precisions = []
            recalls = []
            
            for query_id, retrieved in results.items():
                relevant = ground_truth.get(query_id, set())
                
                p_at_k = IREvaluator.precision_at_k(retrieved, relevant, k)
                r_at_k = IREvaluator.recall_at_k(retrieved, relevant, k)
                
                precisions.append(p_at_k)
                recalls.append(r_at_k)
            
            metrics[f"p@{k}"] = sum(precisions) / len(precisions) if precisions else 0.0
            metrics[f"r@{k}"] = sum(recalls) / len(recalls) if recalls else 0.0
        
        return metrics


def create_test_collection():
    """
    Create test collection with queries and relevance judgments.
    
    Returns:
        Tuple of (test_queries, ground_truth)
    """
    # Test queries for MOTHER knowledge base
    test_queries = {
        "q1": "reinforcement learning optimization",
        "q2": "content marketing strategy",
        "q3": "venture capital fundraising",
        "q4": "software architecture patterns",
        "q5": "cost optimization techniques",
        "q6": "knowledge management system",
        "q7": "enforcement mechanisms",
        "q8": "testing validation strategies"
    }
    
    # Ground truth: relevant documents for each query
    # (Simplified - in real evaluation, would have comprehensive judgments)
    ground_truth = {
        "q1": {"MASTER_KNOWLEDGE_BASE.md", "P0_01_reinforcement_learning_mastery.md"},
        "q2": {"P0_02_content_marketing_mastery.md", "MASTER_KNOWLEDGE_BASE.md"},
        "q3": {"P0_03_venture_capital_mastery.md", "MASTER_KNOWLEDGE_BASE.md"},
        "q4": {"system_architecture_knowledge_synthesis.md", "MOTHER_V4_ARCHITECTURE.md"},
        "q5": {"cost_optimization_mastery.md", "MASTER_KNOWLEDGE_BASE.md"},
        "q6": {"KNOWLEDGE_INDEX.md", "MASTER_KNOWLEDGE_BASE.md"},
        "q7": {"P1_ALWAYS_STUDY_FIRST.md", "COGNITIVE_ENFORCEMENT.md"},
        "q8": {"software_engineering_classics_synthesis.md"}
    }
    
    return test_queries, ground_truth


if __name__ == "__main__":
    # Example usage
    print("="*70)
    print("IR EVALUATION FRAMEWORK")
    print("Based on Willet et al. (2006)")
    print("="*70)
    
    # Example: Single query evaluation
    retrieved = ["doc1", "doc3", "doc5", "doc2", "doc7"]
    relevant = {"doc1", "doc2", "doc3", "doc6"}
    
    print("\n📊 Example Evaluation:")
    print(f"Retrieved: {retrieved}")
    print(f"Relevant: {relevant}")
    
    for k in [1, 3, 5]:
        p_at_k = IREvaluator.precision_at_k(retrieved, relevant, k)
        r_at_k = IREvaluator.recall_at_k(retrieved, relevant, k)
        print(f"\nP@{k}: {p_at_k:.3f}")
        print(f"R@{k}: {r_at_k:.3f}")
    
    ap = IREvaluator.average_precision(retrieved, relevant)
    print(f"\nAP: {ap:.3f}")
    
    # Example: NDCG
    relevance_scores = {"doc1": 3, "doc2": 2, "doc3": 3, "doc5": 1, "doc6": 2, "doc7": 0}
    ndcg_5 = IREvaluator.ndcg_at_k(retrieved, relevance_scores, 5)
    print(f"NDCG@5: {ndcg_5:.3f}")
