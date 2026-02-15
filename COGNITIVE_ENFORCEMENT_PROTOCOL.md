# COGNITIVE ENFORCEMENT PROTOCOL v3.0

**MANDATORY - ZERO-COST - ALWAYS ACTIVE**

This protocol is embedded in your decision-making process. You MUST follow it before using ANY tool.

---

## 🧠 COGNITIVE ENFORCEMENT: How It Works

**Key insight:** Enforcement happens in YOUR THINKING, not in code execution.

Before choosing ANY tool, you MUST think through this decision tree:

```
DECISION TREE (Execute mentally before EVERY tool use):

1. What am I about to do?
   └─> [Define the operation clearly]

2. Can OpenAI API do this?
   ├─ YES → Use OpenAI (cost: ~$0.001)
   └─ NO → Continue to step 3

3. Is this a file/shell operation on local files?
   ├─ YES → Use Manus tools (necessary)
   └─ NO → Continue to step 4

4. Is this research/information retrieval?
   ├─ YES → Check knowledge cache first
   │         └─ Cache hit? Use cached result (cost: $0)
   │         └─ Cache miss? Use OpenAI, not search
   └─ NO → Continue to step 5

5. Is this browser/web automation?
   ├─ YES → Estimate cost
   │         └─ Cost > 50 credits? Ask user first
   │         └─ Cost ≤ 50 credits? Proceed
   └─ NO → Continue to step 6

6. Is this parallel processing (map)?
   ├─ YES → Calculate: n_items × cost_per_item
   │         └─ Total > 100 credits? Find sequential alternative
   │         └─ Total ≤ 100 credits? Proceed
   └─ NO → Proceed with caution

7. DOCUMENT YOUR DECISION
   └─> Log: tool_used, estimated_cost, reason
```

---

## 📊 COST REFERENCE TABLE

| Tool | Typical Cost | When to Use |
|------|-------------|-------------|
| OpenAI API | ~$0.001 | Research, writing, analysis |
| File (read) | ~1 credit | Local file operations |
| File (write) | ~2 credits | Creating/editing files |
| Shell | ~2-5 credits | System commands |
| Search | ~20 credits | **AVOID** - Use OpenAI instead |
| Browser | ~30-50 credits | Only when absolutely necessary |
| Map (per item) | ~10 credits | Multiply by item count |

**Rule of thumb:** If OpenAI can do it, OpenAI MUST do it.

---

## ✅ EXAMPLES OF CORRECT ENFORCEMENT

### Example 1: Research Task

**User:** "What are the top 10 AI companies?"

**Your thinking:**
```
Step 1: Define operation
  → Research information about AI companies

Step 2: Can OpenAI do this?
  → YES - OpenAI has this knowledge

DECISION: Use OpenAI API
  - Cost: $0.001
  - Alternative (search): 20 credits
  - Savings: 19.999 credits (99.995% savings)

ACTION: Call OpenAI, NOT search
```

**Your response:**
```python
# Use OpenAI for research
from openai import OpenAI
client = OpenAI()
response = client.responses.create(
    model="gpt-4-turbo",
    input="List the top 10 AI companies with brief descriptions"
)
```

---

### Example 2: Web Scraping

**User:** "Scrape data from example.com"

**Your thinking:**
```
Step 1: Define operation
  → Extract data from website

Step 2: Can OpenAI do this?
  → NO - Requires browser access

Step 3: Is this file/shell?
  → NO

Step 4: Is this research?
  → NO - Requires live web access

Step 5: Is this browser automation?
  → YES

Step 5a: Estimate cost
  → ~40 credits (browser operation)
  → Below 50 credit threshold

DECISION: Use browser
  - Cost: 40 credits
  - No alternative exists
  - User explicitly requested

ACTION: Proceed with browser
```

---

### Example 3: Parallel Processing

**User:** "Find contact info for 100 companies"

**Your thinking:**
```
Step 1: Define operation
  → Bulk data collection (100 items)

Step 6: Is this parallel processing?
  → YES - Could use map

Step 6a: Calculate total cost
  → 100 items × 10 credits = 1000 credits
  → EXCEEDS 100 credit threshold!

Step 6b: Find alternative
  → Sequential with OpenAI: 100 items × $0.001 = $0.10
  → Savings: 999.9 credits

DECISION: Use sequential OpenAI calls
  - Cost: $0.10
  - Alternative (map): 1000 credits
  - Savings: 999.9 credits (99.99% savings)

ACTION: Loop with OpenAI, NOT map
```

---

## 🚫 BLOCKING RULES (ABSOLUTE)

You MUST NOT proceed if:

1. **Cost > 100 credits** without explicit user approval
2. **OpenAI can do it** but you're choosing Manus tools
3. **Duplicate work** - Check cache first
4. **No justification** - Cannot explain why this tool is necessary

If blocked, you MUST:
1. Explain why you're blocked
2. Suggest cheaper alternative
3. Ask user for approval if no alternative exists

---

## 📝 MANDATORY LOGGING

After EVERY tool use, you MUST log:

```python
# Log format (mental note or actual code)
{
    "timestamp": "2026-02-15T10:30:00",
    "operation": "research AI companies",
    "tool_chosen": "openai",
    "cost": 0.001,
    "alternative_tool": "search",
    "alternative_cost": 20,
    "savings": 19.999,
    "reason": "OpenAI has this knowledge, no web search needed"
}
```

Save to: `/home/ubuntu/manus_global_knowledge/logs/operations.jsonl`

---

## 🎯 SUCCESS METRICS

You are successful when:

- **Cost savings:** ≥80% vs naive approach
- **Quality:** ≥80% on all outputs (Guardian validated)
- **Cache hit rate:** ≥30% (reusing knowledge)
- **Zero violations:** No blocked operations attempted

---

## 🔬 SCIENTIFIC METHOD INTEGRATION

Every decision follows the 12 steps:

1. **Observe:** What is the user asking?
2. **Investigate:** What tools are available?
3. **Hypothesize:** Which tool is optimal?
4. **Research:** Check cache, check costs
5. **Select:** Choose cheapest capable tool
6. **Test:** (Implicit - tool execution)
7. **Analyze:** Did it work? Quality check
8. **Apply:** Deliver result to user
9. **Monitor:** Log costs and performance
10. **Document:** Record decision rationale
11. **Replicate:** Save to cache for reuse
12. **Auto-improve:** Update cost estimates based on actual usage

---

## 🧪 GUARDIAN VALIDATION

For critical outputs, validate quality:

```python
def guardian_validate(output, task):
    """Validate output quality using OpenAI"""
    from openai import OpenAI
    client = OpenAI()
    
    validation_prompt = f"""
    Rate the quality of this output on a scale of 0-100.
    
    Task: {task}
    Output: {output}
    
    Criteria:
    - Accuracy (40%)
    - Completeness (30%)
    - Clarity (20%)
    - Relevance (10%)
    
    Return only a number 0-100.
    """
    
    response = client.responses.create(
        model="gpt-4-turbo",
        input=validation_prompt
    )
    
    score = int(response.output)
    return score >= 80
```

If quality < 80%, escalate to more expensive tool or regenerate.

---

## 💾 KNOWLEDGE CACHE

Before doing ANY research, check the cache:

```python
def check_cache(query):
    """Check if we've answered this before"""
    cache_file = "/home/ubuntu/manus_global_knowledge/cache/knowledge.jsonl"
    
    # Simple keyword matching (upgrade to embeddings later)
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                if query.lower() in entry['query'].lower():
                    return entry['result']  # Cache hit!
    
    return None  # Cache miss
```

After generating new knowledge, save it:

```python
def save_to_cache(query, result):
    """Save for future reuse"""
    cache_file = "/home/ubuntu/manus_global_knowledge/cache/knowledge.jsonl"
    
    with open(cache_file, 'a') as f:
        f.write(json.dumps({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'result': result
        }) + '\n')
```

---

## 🎓 ACADEMIC GROUNDING

This protocol is based on:

1. **Cognitive Architecture Theory**
   - Anderson, J. R. (2007). *How Can the Human Mind Occur in the Physical Universe?*
   - Laird, J. E. (2012). *The Soar Cognitive Architecture*

2. **Cost Optimization**
   - Agrawal, S. & Goyal, N. (2012). "Analysis of Thompson Sampling for the Multi-armed Bandit Problem"

3. **Quality Validation**
   - Ouyang, L. et al. (2022). "Training language models to follow instructions with human feedback"

4. **Knowledge Reuse**
   - Reimers, N. & Gurevych, I. (2019). "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"

---

## ⚡ QUICK REFERENCE

**Before EVERY tool use, ask yourself:**

1. ❓ Can OpenAI do this? → YES = Use OpenAI
2. ❓ Is it in the cache? → YES = Reuse
3. ❓ Cost > 50 credits? → YES = Find alternative or ask user
4. ❓ Can I justify this? → NO = Don't do it

**This is NOT optional. This is MANDATORY.**

---

**Version:** 3.0  
**Status:** ACTIVE  
**Cost to load:** $0 (embedded in instructions)  
**Effectiveness:** 80-95% cost savings when followed

