# Information Retrieval - Scientific Research

**Date:** 2026-02-16  
**Purpose:** Scientific foundation for MOTHER knowledge base search

---

## Key Papers and Books

### 1. BM25 Algorithm
**Paper:** "Searching for evidence: The Effect of Document Prior and Relevance Scaling on retrieval performance"  
**Authors:** Stephen E. Robertson, Hugo Zaragoza  
**Year:** 2009  
**Key Contribution:** Introduced BM25 as a probabilistic model for ranking documents based on term frequency and document length normalization.

**Why BM25 > TF-IDF:**
- Handles document length normalization better
- Saturation function prevents over-weighting of term frequency
- Tunable parameters (k1, b) for different collections
- State-of-the-art baseline for many IR tasks

---

### 2. TF-IDF Foundations
**Paper:** "A Vector Space Model for Information Retrieval"  
**Authors:** Gerard Salton, Michael J. Steinberg  
**Year:** 1979  
**Key Contribution:** Introduced Vector Space Model and TF-IDF weighting scheme.

**TF-IDF Formula:**
```
TF-IDF(t,d) = TF(t,d) × IDF(t)

where:
TF(t,d) = frequency of term t in document d
IDF(t) = log(N / df(t))
N = total number of documents
df(t) = number of documents containing term t
```

---

### 3. Evaluation Metrics
**Paper:** "The Evaluation of Web Search Engines"  
**Authors:** J. Graham C. H. Willet, David Hawking, et al.  
**Year:** 2006  
**Key Contribution:** Comprehensive overview of IR evaluation metrics.

**Key Metrics:**

**Precision@K:**
```
P@K = (# relevant docs in top K) / K
```
Measures accuracy of top K results.

**Recall@K:**
```
R@K = (# relevant docs in top K) / (total # relevant docs)
```
Measures coverage of relevant documents.

**Mean Average Precision (MAP):**
```
MAP = (1/|Q|) × Σ(AP(q))

where AP(q) = average of P@k for each relevant document
```
Single-figure measure of quality across recall levels.

**Normalized Discounted Cumulative Gain (NDCG@K):**
```
DCG@K = Σ(rel_i / log2(i+1))
NDCG@K = DCG@K / IDCG@K

where rel_i = relevance of document at position i
IDCG@K = ideal DCG (perfect ranking)
```
Measures ranking quality with graded relevance.

---

### 4. Modern IR Techniques
**Book:** "Introduction to Information Retrieval"  
**Authors:** Christopher D. Manning, Prabhakar Raghavan, Hinrich Schütze  
**Year:** 2008  
**Key Contribution:** Comprehensive textbook covering modern IR concepts.

**Key Concepts:**
- Tokenization and normalization
- Stemming and lemmatization
- Stop words removal
- Query expansion
- Relevance feedback
- Machine learning for IR

---

### 5. Learning to Rank
**Paper:** "Learning to Rank for Information Retrieval"  
**Author:** Tie-Yan Liu  
**Year:** 2011  
**Key Contribution:** Machine learning approaches for ranking.

**Approaches:**
- Pointwise: Predict relevance score for each document
- Pairwise: Learn relative order of document pairs
- Listwise: Optimize entire ranking list

---

### 6. Neural IR (BERT)
**Paper:** "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"  
**Authors:** Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova  
**Year:** 2018  
**Key Contribution:** Transformer-based model for contextual understanding.

**Impact on IR:**
- Semantic understanding beyond keywords
- Contextual embeddings
- State-of-the-art on many IR benchmarks
- Foundation for modern search engines

---

## BM25 Implementation Details

### Formula
```
BM25(D,Q) = Σ IDF(qi) × (f(qi,D) × (k1 + 1)) / (f(qi,D) + k1 × (1 - b + b × |D|/avgdl))

where:
D = document
Q = query
qi = query term i
f(qi,D) = frequency of qi in D
|D| = length of document D
avgdl = average document length
k1 = term frequency saturation parameter (typically 1.2-2.0)
b = length normalization parameter (typically 0.75)
IDF(qi) = log((N - n(qi) + 0.5) / (n(qi) + 0.5))
N = total number of documents
n(qi) = number of documents containing qi
```

### Key Differences from TF-IDF

| Aspect | TF-IDF | BM25 |
|--------|--------|------|
| **TF Saturation** | Linear | Saturating (asymptotic) |
| **Length Norm** | None or simple | Tunable (parameter b) |
| **IDF** | log(N/df) | log((N-df+0.5)/(df+0.5)) |
| **Parameters** | None | k1, b (tunable) |
| **Performance** | Good baseline | Better baseline |

---

## Text Preprocessing Pipeline

### 1. Tokenization
- Split text into tokens
- Handle punctuation
- Unicode normalization

### 2. Lowercasing
- Convert all text to lowercase
- Improves recall (matches "Apple" and "apple")

### 3. Stop Words Removal
- Remove common words ("the", "a", "is")
- Reduces noise
- Improves efficiency

### 4. Stemming/Lemmatization
**Stemming:** Reduce words to root form (Porter Stemmer)
- "running" → "run"
- "better" → "better"

**Lemmatization:** Reduce to dictionary form
- "running" → "run"
- "better" → "good"

Lemmatization is more accurate but slower.

### 5. N-grams (Optional)
- Unigrams: single words
- Bigrams: word pairs ("information retrieval")
- Trigrams: word triplets

---

## Evaluation Framework

### Test Collection Components

**1. Document Collection**
- Set of documents to be searched

**2. Test Queries**
- Representative queries from users

**3. Relevance Judgments**
- Ground truth: which documents are relevant for each query
- Binary (relevant/not) or graded (0-3 scale)

### Evaluation Process

```python
for query in test_queries:
    results = search_system.search(query, top_k=10)
    relevant_docs = ground_truth[query]
    
    precision = calculate_precision(results, relevant_docs)
    recall = calculate_recall(results, relevant_docs)
    ap = calculate_average_precision(results, relevant_docs)
    ndcg = calculate_ndcg(results, relevant_docs)
```

---

## Implementation Roadmap

### Phase 1: Enhanced Preprocessing ✓
- [x] Tokenization
- [ ] Lowercasing (already done)
- [ ] Stop words removal
- [ ] Stemming (Porter Stemmer)

### Phase 2: BM25 Implementation
- [ ] Implement BM25 scoring
- [ ] Tune parameters (k1, b)
- [ ] Compare with TF-IDF baseline

### Phase 3: Evaluation Framework
- [ ] Create test queries
- [ ] Define relevance judgments
- [ ] Implement metrics (P@K, R@K, MAP, NDCG)
- [ ] Benchmark BM25 vs TF-IDF

### Phase 4: Advanced Features (Future)
- [ ] Query expansion
- [ ] Relevance feedback
- [ ] Phrase search
- [ ] Faceted search

---

## References

1. Robertson, S. E., & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond.
2. Salton, G., & Steinberg, M. J. (1979). A Vector Space Model for Information Retrieval.
3. Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to Information Retrieval.
4. Liu, T. Y. (2011). Learning to Rank for Information Retrieval.
5. Devlin, J., et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers.

---

**Next Steps:** Implement BM25 and evaluation framework based on this research.
