# Cognitive Enforcement Protocol

**Version:** 1.0  
**Date:** 2026-02-15  
**Purpose:** Enable autonomous, cost-effective decision-making by the AI agent

---

## 🧠 Core Principle

**"When facing a problem, always respond with the best solution instead of asking what to choose. Solving problems autonomously with wisdom is also cost savings."**

---

## 🎯 The Decision Framework

### Before EVERY Tool Call

**MANDATORY Mental Checklist:**

```
1. Can OpenAI API do this?
   ├─→ YES: Use OpenAI (0.001 credits)
   └─→ NO: Continue to step 2

2. Does it require browser/MCP/files/shell?
   ├─→ YES: Use Manus (necessary)
   └─→ NO: Go back to step 1 (you missed something)

3. Is this client-facing or strategic?
   ├─→ YES: Consider quality over cost
   └─→ NO: Optimize for cost

4. Log the decision
   └─→ ALWAYS: Record tool, cost, reason
```

---

## 💰 Cost Reference Table

| Tool | Cost (credits) | When to Use | Alternative |
|------|----------------|-------------|-------------|
| **OpenAI API** | 0.001 | Research, analysis, writing, code | DEFAULT |
| file_read | 1 | Reading files | No alternative |
| file_write | 2 | Writing files | No alternative |
| shell | 3 | System commands | No alternative |
| search | 20 | Web search | **OpenAI** (20,000x cheaper) |
| browser | 40 | Web scraping, login | Only when necessary |
| map | 10/item | Parallel processing | OpenAI sequential (for <10 items) |
| generate | 15 | Image/video generation | Only when necessary |

---

## 🚫 Common Mistakes to Avoid

### Mistake 1: Using `search` for Research

**Wrong:**
```python
# Cost: 20 credits
search("top 10 construction companies in Australia")
```

**Right:**
```python
# Cost: 0.001 credits (20,000x cheaper)
openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "List top 10 construction companies in Australia"}]
)
```

**Savings:** 19.999 credits (99.995%)

### Mistake 2: Using Manus for Text Analysis

**Wrong:**
```python
# Cost: 40 credits
# Use Manus to summarize document
```

**Right:**
```python
# Cost: 0.001 credits
openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": f"Summarize: {document}"}]
)
```

**Savings:** 39.999 credits (99.998%)

### Mistake 3: Using `map` for Small Batches

**Wrong:**
```python
# Cost: 50 credits (5 items × 10 credits)
map(items=5, task="analyze company")
```

**Right:**
```python
# Cost: 0.001 credits
for item in items:
    openai.chat.completions.create(...)
```

**Savings:** 49.999 credits (99.998%)

---

## ✅ When to Use Manus (Expensive Tools)

### Valid Use Cases

1. **Browser Operations**
   - Web scraping (no API available)
   - Login to websites
   - Interactive web apps
   - **Cost:** 40 credits (justified)

2. **MCP Operations**
   - Gmail (send/read emails)
   - Google Calendar (manage events)
   - **Cost:** Variable (justified)

3. **File System Operations**
   - Reading/writing files
   - Shell commands
   - **Cost:** 1-3 credits (necessary)

4. **Parallel Processing (Large Scale)**
   - >20 homogeneous items
   - Time-critical bulk operations
   - **Cost:** 10/item (justified if >20 items)

---

## 🎓 Decision Examples

### Example 1: Research Task

**Task:** "Find top 10 mining companies in Indonesia"

**Decision Process:**
1. Can OpenAI do this? → **YES** (has this knowledge)
2. Use OpenAI API
3. Cost: 0.001 credits
4. Log: `log_cost("Research mining companies", "openai", 0.001, alternative_tool="search", alternative_cost=20)`

**Savings:** 19.999 credits

### Example 2: Web Scraping

**Task:** "Scrape company website for contact information"

**Decision Process:**
1. Can OpenAI do this? → **NO** (needs browser)
2. Does it require browser? → **YES**
3. Use Manus browser
4. Cost: 40 credits
5. Log: `log_cost("Scrape website", "browser", 40, reason="No API available")`

**Justified:** No alternative exists

### Example 3: Code Generation

**Task:** "Generate Python script for data analysis"

**Decision Process:**
1. Can OpenAI do this? → **YES** (excellent at code)
2. Use OpenAI API
3. Cost: 0.001 credits
4. Log: `log_cost("Generate code", "openai", 0.001, alternative_tool="manus", alternative_cost=30)`

**Savings:** 29.999 credits

### Example 4: Bulk Email Lookup

**Task:** "Find emails for 50 executives"

**Decision Process:**
1. Can OpenAI do this? → **NO** (needs real-time data)
2. Can Apollo API do this? → **YES**
3. Use Apollo API
4. Cost: 0.5 credits (50 × 0.01)
5. Log: `log_cost("Email lookup", "apollo", 0.5, alternative_tool="map", alternative_cost=500)`

**Savings:** 499.5 credits

---

## 📊 Logging Protocol

### At Task Start (MANDATORY)

```python
from core.precise_cost_tracker import start_task

start_task("Task description")
```

### After EVERY Operation (MANDATORY)

```python
from core.precise_cost_tracker import log_op

log_op(
    tool="Tool used",
    action="What was done",
    cost_credits=precise_cost,  # From cost table, not estimate
    alternative_tool="What else could have been used",
    alternative_cost=cost_of_alternative,
    quality_score=0-100  # Optional
)
```

### At Task End (MANDATORY)

```python
from core.precise_cost_tracker import end_task

report = end_task()
print(report)  # Show compact cost report to user
```

**Example:**
```python
log_cost(
    operation="Research top 10 construction companies",
    tool="openai",
    cost=0.001,
    alternative_tool="search",
    alternative_cost=20,
    reason="OpenAI has this knowledge, 20,000x cheaper",
    quality_score=95
)
```

---

## 🎯 Autonomous Decision-Making Rules

### Rule 1: Default to Cheapest

**Always start with the cheapest option that can achieve the required quality.**

- Research/Analysis/Writing/Code → **OpenAI** (default)
- Only escalate to Manus if OpenAI cannot do it

### Rule 2: Don't Ask, Decide

**When facing a problem, implement the best solution immediately.**

- ❌ "Should I use OpenAI or search?"
- ✅ Use OpenAI (obvious best choice)

### Rule 3: Justify Expensive Choices

**If using a tool >10 credits, document why.**

- Browser: "No API available, must scrape"
- Map: "100 items, parallel processing necessary"
- Search: "OpenAI doesn't have real-time data on this topic"

### Rule 4: Learn and Adapt

**Track outcomes and adjust decisions.**

- If OpenAI quality < 80% → Consider alternatives
- If Manus was used unnecessarily → Learn for next time
- If savings < 75% → Review decision process

---

## 🔄 Continuous Improvement

### Weekly Review

**Every Monday, analyze:**
1. Total operations
2. Cost per operation
3. Savings rate (target: 75-90%)
4. Quality scores
5. Tool usage patterns

**Adjust:**
- Update cost estimates based on actual usage
- Identify patterns of waste
- Refine decision rules

### Monthly Optimization

**Every month:**
1. Compare OpenAI vs Manus quality
2. Identify tasks that could be automated
3. Update routing rules
4. Create new AI University lessons

---

## 🚨 Red Flags

### Immediate Action Required If:

1. **Savings rate < 50%**
   - Review all tool selections
   - Identify wasteful patterns
   - Retrain decision process

2. **Using `search` frequently**
   - Almost always wrong
   - OpenAI can handle 95% of research

3. **Using `map` for small batches**
   - Threshold: >20 items
   - Below that: sequential OpenAI

4. **No logs being generated**
   - System not working
   - Restart enforcement

---

## 💡 Wisdom Principles

### Principle 1: Time is Money

**Don't spend 10 minutes deciding between two 1-credit options.**

- Quick decision > Perfect decision
- Autonomy > Asking for permission

### Principle 2: Quality Threshold

**80% quality is often good enough.**

- Don't over-optimize
- Diminishing returns above 80%
- Client-facing: aim for 90%+

### Principle 3: Fail Fast

**If OpenAI doesn't work, escalate quickly.**

- Try OpenAI first (0.001 credits)
- If quality < 80%, use Manus
- Don't retry OpenAI multiple times

### Principle 4: Document Decisions

**Every decision is a learning opportunity.**

- Log all operations
- Track outcomes
- Build knowledge base

---

## 📈 Success Metrics

### Target Performance

- **Savings Rate:** 75-90%
- **Quality Score:** ≥80%
- **OpenAI Usage:** 90% of tasks
- **Manus Usage:** 10% of tasks (only when necessary)
- **Cost per Operation:** <5 credits average

### Current Baseline (Before Enforcement)

- Savings Rate: 0%
- OpenAI Usage: 0%
- Manus Usage: 100%
- Cost per Operation: ~30 credits

### Expected Improvement

- Savings: +75-90%
- Cost reduction: 90-95%
- Annual savings: $40K-45K

---

## 🔧 Implementation Checklist

### At Conversation Start

- [x] Run bootstrap script
- [x] Initialize enforcement system
- [x] Load AI University lessons
- [x] Load cost reference table
- [x] Activate cognitive enforcement

### Before Each Operation

- [ ] Check: Can OpenAI do this?
- [ ] If no: Check if browser/MCP/files required
- [ ] Select cheapest capable tool
- [ ] Prepare to log decision

### After Each Operation

- [ ] Log operation with cost
- [ ] Record alternative and savings
- [ ] Note quality score
- [ ] Update metrics

### End of Day

- [ ] Review operations log
- [ ] Calculate savings rate
- [ ] Identify improvement opportunities
- [ ] Update lessons learned

---

## 🎓 Integration with AI University

**This protocol is Lesson 017:**

- **Domain:** Cost Optimization, Decision Making
- **Priority:** CRITICAL
- **Enforcement:** Mandatory for all tasks
- **Success Rate:** TBD (tracking starts now)

**Related Lessons:**
- LESSON_01: Cost Optimization
- LESSON_016: Follow Learned Lessons
- LESSON_011: Effective Task Prioritization

---

## 📝 Summary

**The Golden Rule:**

> "Before every tool call: Can OpenAI do this? If yes, use OpenAI. If no, use the minimum necessary tool. Always log the decision. Never ask, always decide."

**Expected Outcome:**

- 90% of tasks use OpenAI (0.001 credits each)
- 10% of tasks use Manus (only when necessary)
- 75-90% cost savings
- Autonomous, wise decision-making
- Continuous learning and improvement

---

## 🔄 Weekly Self-Improvement (AUTOMATIC)

**Every Monday:**

```python
from core.self_improvement import learn_and_improve

report = learn_and_improve()
print(report)
```

**System will:**
- Analyze last 7 days of operations
- Identify wasteful patterns
- Learn new optimization rules
- Generate recommendations
- Improve decision-making automatically

---

**Status:** Active and Enforced  
**Last Updated:** 2026-02-15  
**Next Review:** 2026-02-22
