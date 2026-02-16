"""
Comprehensive Comparison: BM25 vs TF-IDF

Scientific validation of IR system using evaluation metrics.
"""

import sys
import os
sys.path.append('/home/ubuntu/manus_global_knowledge/mother_v5')

from application.services.scientific_ir import ScientificIR
from application.services.ir_evaluation import IREvaluator, create_test_collection


def run_comparison():
    """Run comprehensive BM25 vs TF-IDF comparison."""
    
    print("="*70)
    print("SCIENTIFIC IR SYSTEM VALIDATION")
    print("Comparing BM25 vs TF-IDF Baseline")
    print("="*70)
    
    # Initialize IR system
    ir = ScientificIR()
    
    # Load index (already created)
    if not os.path.exists(ir.index_path):
        print("\n⚠️  Index not found. Creating...")
        ir.index_knowledge_base()
    else:
        print("\n✅ Loading existing index...")
        ir.load_index()
        print(f"   Documents: {len(ir.documents)}")
        print(f"   Vocabulary: {len(ir.vocabulary)} terms")
        print(f"   Avg doc length: {ir.avgdl:.1f} terms")
    
    # Get test collection
    test_queries, ground_truth = create_test_collection()
    
    print(f"\n📋 Test Collection:")
    print(f"   Queries: {len(test_queries)}")
    print(f"   Ground truth judgments: {sum(len(v) for v in ground_truth.values())}")
    
    # Run both systems
    print("\n🔍 Running BM25...")
    bm25_results = {}
    for query_id, query_text in test_queries.items():
        results = ir.search(query_text, top_k=10, use_bm25=True)
        # Extract filenames as doc IDs
        bm25_results[query_id] = [os.path.basename(doc["file"]) for doc, score in results]
    
    print("🔍 Running TF-IDF...")
    tfidf_results = {}
    for query_id, query_text in test_queries.items():
        results = ir.search(query_text, top_k=10, use_bm25=False)
        tfidf_results[query_id] = [os.path.basename(doc["file"]) for doc, score in results]
    
    # Evaluate both systems
    print("\n📊 EVALUATION RESULTS")
    print("="*70)
    
    bm25_metrics = IREvaluator.evaluate_system(bm25_results, ground_truth, k_values=[1, 3, 5, 10])
    tfidf_metrics = IREvaluator.evaluate_system(tfidf_results, ground_truth, k_values=[1, 3, 5, 10])
    
    # Print comparison table
    print(f"\n{'Metric':<15} {'BM25':>10} {'TF-IDF':>10} {'Winner':>10}")
    print("-"*50)
    
    for metric in sorted(bm25_metrics.keys()):
        bm25_val = bm25_metrics[metric]
        tfidf_val = tfidf_metrics[metric]
        
        if bm25_val > tfidf_val:
            winner = "BM25 ✓"
            improvement = ((bm25_val - tfidf_val) / tfidf_val * 100) if tfidf_val > 0 else 0
        elif tfidf_val > bm25_val:
            winner = "TF-IDF"
            improvement = ((tfidf_val - bm25_val) / bm25_val * 100) if bm25_val > 0 else 0
        else:
            winner = "Tie"
            improvement = 0
        
        print(f"{metric.upper():<15} {bm25_val:>10.3f} {tfidf_val:>10.3f} {winner:>10}")
        
        if winner != "Tie" and improvement > 0:
            print(f"{'':15} (improvement: +{improvement:.1f}%)")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    bm25_wins = sum(1 for m in bm25_metrics if bm25_metrics[m] > tfidf_metrics[m])
    tfidf_wins = sum(1 for m in tfidf_metrics if tfidf_metrics[m] > bm25_metrics[m])
    
    print(f"\nBM25 wins: {bm25_wins}/{len(bm25_metrics)} metrics")
    print(f"TF-IDF wins: {tfidf_wins}/{len(tfidf_metrics)} metrics")
    
    if bm25_wins > tfidf_wins:
        print("\n✅ BM25 is the better algorithm for this collection!")
    elif tfidf_wins > bm25_wins:
        print("\n⚠️  TF-IDF performed better (unexpected)")
    else:
        print("\n🤝 Both algorithms perform similarly")
    
    # Detailed query-by-query analysis
    print("\n" + "="*70)
    print("QUERY-BY-QUERY ANALYSIS")
    print("="*70)
    
    for query_id in sorted(test_queries.keys()):
        query_text = test_queries[query_id]
        relevant = ground_truth.get(query_id, set())
        
        bm25_retrieved = bm25_results[query_id]
        tfidf_retrieved = tfidf_results[query_id]
        
        bm25_p5 = IREvaluator.precision_at_k(bm25_retrieved, relevant, 5)
        tfidf_p5 = IREvaluator.precision_at_k(tfidf_retrieved, relevant, 5)
        
        print(f"\n{query_id}: \"{query_text}\"")
        print(f"  Relevant docs: {len(relevant)}")
        print(f"  BM25 P@5: {bm25_p5:.3f}")
        print(f"  TF-IDF P@5: {tfidf_p5:.3f}")
        
        if bm25_p5 > tfidf_p5:
            print(f"  Winner: BM25 ✓")
        elif tfidf_p5 > bm25_p5:
            print(f"  Winner: TF-IDF")
        else:
            print(f"  Winner: Tie")
    
    print("\n" + "="*70)
    print("VALIDATION COMPLETE")
    print("="*70)
    
    return bm25_metrics, tfidf_metrics


if __name__ == "__main__":
    run_comparison()
