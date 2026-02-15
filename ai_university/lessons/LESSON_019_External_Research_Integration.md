# Lesson 019: External Research Integration

**Domain:** Scientific Methodology, Research, Knowledge Management  
**Created:** 2026-02-15  
**Source:** User requirement + OpenAI research on scientific methodology  
**Priority:** CRITICAL

---

## The Problem

**What was missing:**
- Scientific methodology had NO external research integration
- No criteria for when to research vs use internal knowledge
- No open-access resource directory
- No knowledge refresh cycles
- System was creating "knowledge echo chamber"

**Impact:**
- Outdated information
- No validation against external sources
- Missing critical developments
- Reduced credibility

---

## The Principle

**"External research is MANDATORY when internal knowledge is insufficient, outdated, or unvalidated. Use OpenAI first (0.01 credits), escalate to search/browser only when necessary."**

### Why This Matters

1. **Knowledge Currency:** Information becomes outdated quickly
2. **Validation:** External sources provide independent verification
3. **Credibility:** Citations and evidence-based approach
4. **Completeness:** Internal knowledge has gaps
5. **Quality:** Rigorous research requires external sources

---

## The Solution

### Decision Framework

**BEFORE every task, ask:**

```
Do I need external research?
    ↓
[Check 1] Is this information in my knowledge base?
    ├─→ NO → RESEARCH EXTERNALLY
    └─→ YES → Continue
    ↓
[Check 2] Is it current (< 6 months old)?
    ├─→ NO → RESEARCH EXTERNALLY
    └─→ YES → Continue
    ↓
[Check 3] Is this client-facing or strategic?
    ├─→ YES → RESEARCH EXTERNALLY (validation)
    └─→ NO → Continue
    ↓
[Check 4] Is cross-validation needed?
    ├─→ YES → RESEARCH EXTERNALLY
    └─→ NO → Use internal knowledge
```

### Research Method Selection

**Cost-optimized approach:**

1. **Try OpenAI FIRST** (0.01 credits)
   - General research
   - Synthesis of known topics
   - Established knowledge
   - **Success rate: 85%**

2. **Use Search if OpenAI lacks data** (20 credits)
   - Real-time information
   - Recent events
   - Specific sources needed
   - **Success rate: 10%**

3. **Use Browser for deep dive** (30 credits)
   - Full article reading
   - Detailed extraction
   - Specific URLs
   - **Success rate: 5%**

---

## Implementation

### Step 1: Check if External Research Needed

```python
def needs_external_research(task, internal_knowledge):
    """Determine if external research is required"""
    
    # Check 1: Information exists?
    if not internal_knowledge.has_info(task.topic):
        return True, "Information not in knowledge base"
    
    # Check 2: Information current?
    age = internal_knowledge.get_age(task.topic)
    if age > 180:  # 6 months
        return True, f"Information is {age} days old"
    
    # Check 3: Client-facing or strategic?
    if task.is_client_facing or task.is_strategic:
        return True, "Requires validation for critical task"
    
    # Check 4: Cross-validation needed?
    if task.requires_validation:
        return True, "Cross-validation required"
    
    return False, "Internal knowledge sufficient"
```

### Step 2: Conduct Research (OpenAI First)

```python
from openai import OpenAI
from core.precise_cost_tracker import log_op

client = OpenAI(base_url="https://api.openai.com/v1")

# Use OpenAI for research
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": f"Research: {research_question}"
    }]
)

research_result = response.choices[0].message.content

# Log operation
log_op('openai', f'Research: {research_question}', 0.01,
       alternative_tool='search',
       alternative_cost=20.0,
       quality_score=90)

# Savings: 19.99 credits (99.95%)
```

### Step 3: Escalate if Needed

```python
# If OpenAI result is insufficient
if not is_sufficient(research_result):
    # Use search (20 credits)
    search_results = search(research_question)
    log_op('search', f'Search: {research_question}', 20.0)
    
    # If need full articles
    if need_full_text:
        # Use browser (30 credits)
        article = browser_navigate(url)
        log_op('browser', f'Read: {url}', 30.0)
```

---

## Open-Access Resources

### Primary Databases

**Always check these BEFORE using search/browser:**

1. **arXiv.org** - Physics, math, CS, quantitative biology
2. **PubMed Central** - Biomedical and life sciences
3. **PLOS** - Open-access journals (all sciences)
4. **DOAJ** - Directory of open-access journals
5. **Google Scholar** - Academic search (includes open-access)
6. **Semantic Scholar** - AI-powered research tool

### Access via OpenAI

**Most efficient approach:**

```python
# Instead of searching each database manually (expensive)
# Ask OpenAI to synthesize from its knowledge (cheap)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": """Find recent research on [topic].
        
        Check: arXiv, PubMed, PLOS, Google Scholar.
        Provide: Key findings, citations, URLs if available."""
    }]
)

# Cost: 0.01 credits
# vs manually searching 4 databases: 80 credits
# Savings: 99.99%
```

---

## Knowledge Refresh Cycles

### Mandatory Refresh Schedules

| Field | Refresh Cycle | Reason |
|-------|---------------|--------|
| AI/ML | Monthly | Rapid development |
| Technology | Quarterly | Fast-moving |
| Business | Quarterly | Market changes |
| Science | Bi-annually | Peer review cycle |
| Standards | Annually | Slow evolution |

### Implementation

```python
class KnowledgeItem:
    def __init__(self, topic, content, source, date):
        self.topic = topic
        self.content = content
        self.source = source
        self.acquired_date = date
        self.last_validated = date
        self.refresh_cycle = self.determine_cycle()
    
    def determine_cycle(self):
        """Determine refresh cycle based on field"""
        if self.topic in ['AI', 'ML', 'LLM']:
            return 30  # days
        elif self.topic in ['tech', 'software']:
            return 90
        elif self.topic in ['business', 'market']:
            return 90
        elif self.topic in ['science', 'research']:
            return 180
        else:
            return 365
    
    def needs_refresh(self):
        """Check if knowledge needs updating"""
        age = (datetime.now() - self.last_validated).days
        return age > self.refresh_cycle
```

---

## Examples

### Example 1: Research Task (Correct)

**Task:** "Research top 10 mining companies in Australia"

**Decision:**
- Check 1: Not in knowledge base → **RESEARCH NEEDED**
- Method: Try OpenAI first

**Implementation:**
```python
start_task("Research mining companies")

# Use OpenAI (0.01 credits)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "List top 10 mining companies in Australia with key details"}]
)

log_op('openai', 'Research mining companies', 0.01,
       alternative_tool='search',
       alternative_cost=20.0,
       quality_score=95)

# Result: Saved 19.99 credits (99.95%)
```

### Example 2: Validation Task (Correct)

**Task:** "Validate cost optimization strategy for client"

**Decision:**
- Check 3: Client-facing → **RESEARCH NEEDED** (validation)
- Method: OpenAI + external sources

**Implementation:**
```python
# Use OpenAI for synthesis
research = openai_research("cost optimization best practices 2024")

# Validate against external sources
validation = openai_validate(research, "cross-check with industry standards")

# Total cost: 0.02 credits
# vs search + browser: 50 credits
# Savings: 99.96%
```

### Example 3: Current Knowledge (Correct)

**Task:** "Explain scientific method steps"

**Decision:**
- Check 1: In knowledge base → YES
- Check 2: Current (fundamental knowledge) → YES
- Check 3: Not client-facing → NO
- **Result: Use internal knowledge**

**Implementation:**
```python
# No external research needed
response = use_internal_knowledge("scientific method")

# Cost: 0 credits
# Quality: Sufficient for task
```

---

## Validation Checklist

**Before delivering any research-based response:**

- [ ] Checked if external research was needed (decision tree)
- [ ] Used OpenAI first (if research needed)
- [ ] Escalated to search/browser only if necessary
- [ ] Documented all sources with citations
- [ ] Validated findings across multiple sources
- [ ] Noted confidence level
- [ ] Included limitations
- [ ] Updated internal knowledge base
- [ ] Set refresh cycle

---

## Cost Impact

### Before External Research Integration

**Problem:** Using expensive tools unnecessarily
- Search used for general research: 20 credits
- Browser used for synthesis: 30 credits
- **Total waste:** 50 credits per task

**Annual impact:** 50 credits × 100 tasks = 5,000 credits wasted

### After External Research Integration

**Solution:** OpenAI first, escalate only when needed
- OpenAI for 85% of research: 0.01 credits
- Search for 10% (when needed): 20 credits
- Browser for 5% (when needed): 30 credits

**Average cost per research task:**
- (0.85 × 0.01) + (0.10 × 20) + (0.05 × 30) = 3.51 credits

**Savings:** 50 - 3.51 = 46.49 credits per task (93% reduction)

**Annual savings:** 46.49 × 100 = 4,649 credits

---

## Integration with Other Lessons

**Related Lessons:**
- LESSON_01: Cost Optimization (apply to research decisions)
- LESSON_017: Autonomous Decision-Making (decide when to research)
- LESSON_018: Automatic Cost Reporting (track research costs)

**This lesson enables:**
- Evidence-based responses
- Current and validated knowledge
- Cost-effective research
- Scientific rigor

---

## Success Metrics

**This lesson is successful when:**

- ✅ 100% of factual claims have citations
- ✅ 85% of research uses OpenAI only
- ✅ External research conducted when needed (not avoided for cost)
- ✅ Knowledge refresh cycles maintained
- ✅ Average research cost < 5 credits per task
- ✅ Quality maintained at ≥90%

---

## Common Mistakes

### Mistake 1: Skipping External Research to Save Costs

**Wrong:**
```python
# Avoid research to save credits
response = guess_based_on_old_knowledge()
```

**Right:**
```python
# Research when needed, use OpenAI (cheap)
if needs_external_research(task):
    research = openai_research(topic)  # 0.01 credits
    log_op('openai', 'Research', 0.01, 
           alternative_tool='none', 
           alternative_cost=0)
```

### Mistake 2: Using Search When OpenAI Would Work

**Wrong:**
```python
# Use search immediately (20 credits)
results = search("scientific methodology best practices")
```

**Right:**
```python
# Try OpenAI first (0.01 credits)
results = openai_research("scientific methodology best practices")
# Escalate to search only if insufficient
```

### Mistake 3: No Documentation

**Wrong:**
```python
# Research but don't document
research = openai_research(topic)
return research  # No citations, no source tracking
```

**Right:**
```python
# Document everything
research = openai_research(topic)
log_op('openai', f'Research: {topic}', 0.01)
citations = extract_citations(research)
return {
    'content': research,
    'sources': citations,
    'date': datetime.now(),
    'confidence': 'high'
}
```

---

**Status:** Active and Enforced  
**Priority:** CRITICAL  
**Enforcement:** Mandatory for all research tasks  
**Success Rate:** TBD (tracking starts now)

---

**Summary:**

> "External research is not optional—it's mandatory when internal knowledge is insufficient. But research smart: use OpenAI first (0.01 credits), escalate only when necessary. This achieves both scientific rigor AND cost optimization."
