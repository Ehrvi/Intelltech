# P3: Always Optimize Cost - ENFORCED

## Prime Directive
**Achieve 75-90% cost savings while maintaining quality ≥80%**

---

## MANDATORY CHECKLIST (Before EVERY API Call)

### 1. CHECK CACHE FIRST ✅
```
❓ Is this exact request cached?
❓ Is cache still valid (< 30 days)?
✅ YES → Use cache (FREE)
❌ NO → Continue to step 2
```

### 2. CHECK TEMPLATE ✅
```
❓ Does a template exist for this operation?
❓ Can template be filled locally?
✅ YES → Use template (FREE)
❌ NO → Continue to step 3
```

### 3. CHECK LOCAL TOOLS ✅
```
❓ Can this be done with local tools?
   - sed/awk/grep for text
   - Python stdlib for data
   - Local validation
✅ YES → Use local (FREE)
❌ NO → Continue to step 4
```

### 4. OPTIMIZE PROMPT ✅
```
✅ Remove redundant phrases
✅ Compress whitespace
✅ Use shorthand
✅ Limit to 500 tokens max
✅ Specify output format (JSON/concise)
```

### 5. SELECT RIGHT MODEL ✅
```
Simple task? → gpt-4o-mini (16x cheaper)
Complex task? → gpt-4o (full power)
```

### 6. BATCH IF POSSIBLE ✅
```
❓ Can this be batched with other operations?
✅ YES → Wait and batch (40-60% savings)
❌ NO → Proceed with single call
```

### 7. LOG COST ✅
```
✅ Log operation name
✅ Log actual cost
✅ Log tokens used
✅ Log savings achieved
```

---

## ENFORCEMENT RULES (V3.3 UPDATE)

### ⚖️ The Prime Rule of Optimization

**CORRECTNESS > COST.**

Cost optimization must **NEVER** come at the expense of fulfilling task requirements or ensuring quality. Saving money by skipping a required step is a **CRITICAL FAILURE**, not a success.

**New Blocking Violation:**
- ❌ **Skipping required research or validation steps to save cost.** This is a direct violation of P1 and P4, and will be blocked.

---


### BLOCKING Violations
These will **BLOCK** the operation:

1. ❌ API call without checking cache
2. ❌ API call when template exists
3. ❌ API call when local tool works
4. ❌ Unoptimized prompt (>500 tokens)
5. ❌ Wrong model selection
6. ❌ No cost logging

### WARNING Violations
These will generate **WARNING**:

1. ⚠️ Cache hit rate < 70%
2. ⚠️ Template usage < 60%
3. ⚠️ Local-first < 80%
4. ⚠️ Cost > budget
5. ⚠️ No batching when possible

---

## COST TARGETS

### Per Operation Type
- Research: $0.02-0.05 (with caching: $0.00)
- Generation: $0.01-0.03 (with templates: $0.00)
- Validation: $0.01-0.02 (local first: $0.00)
- Analysis: $0.02-0.04 (with caching: $0.00)

### Per Session
- Simple task: $0.05-0.10
- Medium task: $0.10-0.25
- Complex task: $0.25-0.50
- **Target: 75-90% below baseline**

---

## OPTIMIZATION TECHNIQUES

### 1. Caching (70-90% savings)
```python
# Before API call
cached = check_cache(prompt)
if cached:
    return cached  # FREE!

# After API call
save_cache(prompt, response)
```

### 2. Templates (80-95% savings)
```python
# Check template first
template = get_template("operation_name")
if template:
    return template.format(**data)  # FREE!
```

### 3. Local Tools (100% savings)
```bash
# Use local tools
cat file.txt | grep "pattern" | awk '{print $1}'  # FREE!
```

### 4. Prompt Optimization (30-50% savings)
```
Bad:  "Please could you analyze this data and provide..."
Good: "Analyze: [data]. Format: JSON"
```

### 5. Batching (40-60% savings)
```
Bad:  10 separate API calls
Good: 1 API call with 10 items
```

---

## MONITORING

### Daily Metrics
- Total cost
- Total saved
- Savings rate (target: ≥75%)
- Cache hit rate (target: ≥70%)
- Template usage (target: ≥60%)
- Local-first rate (target: ≥80%)

### Weekly Review
- Cost trends
- Optimization opportunities
- New templates needed
- Cache cleanup

---

## EXAMPLES

### Example 1: Research (With Optimization)
```
Request: "Research design principles"

Step 1: Check cache
→ Cache hit! (30 days old, still valid)
→ Return cached result
→ Cost: $0.00 (saved $0.05)
→ Time: <1ms
```

### Example 2: Document Generation (With Template)
```
Request: "Generate project report"

Step 1: Check cache → Miss
Step 2: Check template → Hit!
→ Fill template with data
→ Cost: $0.00 (saved $0.15)
→ Time: 10ms
```

### Example 3: Text Processing (Local Tool)
```
Request: "Extract emails from file"

Step 1: Check cache → Miss
Step 2: Check template → Miss
Step 3: Check local → grep works!
→ Use: grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
→ Cost: $0.00 (saved $0.02)
→ Time: 5ms
```

### Example 4: API Call (Optimized)
```
Request: "Analyze complex business strategy"

Step 1: Check cache → Miss
Step 2: Check template → Miss
Step 3: Check local → Too complex
Step 4: Optimize prompt
→ Original: 800 tokens
→ Optimized: 400 tokens
→ Savings: 50%
Step 5: Select model → gpt-4o (complex task)
Step 6: Make call
→ Cost: $0.03 (saved $0.03 from optimization)
Step 7: Cache result
→ Next time: FREE!
```

---

## ANTI-PATTERNS

### ❌ DON'T DO THIS
1. Make API call without checking cache
2. Generate content when template exists
3. Use API for simple text operations
4. Send unoptimized prompts
5. Use expensive model for simple tasks
6. Make multiple calls when one batch works
7. Ignore cost logging
8. No monitoring or review

### ✅ DO THIS INSTEAD
1. Always check cache first
2. Always check templates
3. Prefer local tools
4. Optimize every prompt
5. Select right model
6. Batch operations
7. Log all costs
8. Review and optimize weekly

---

## COMPLIANCE

### How to Check
```bash
python3 /home/ubuntu/manus_global_knowledge/core/aggressive_cost_optimizer.py
```

### Expected Output
```
Savings Rate: ≥75%
Cache Hit Rate: ≥70%
Template Usage: ≥60%
Local-First: ≥80%
```

---

## COST REPORT (Required)

Every conversation MUST end with:
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    💰 COST OPTIMIZATION REPORT                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Total Cost:        $X.XX USD                                                ║
║  Total Saved:       $X.XX USD                                                ║
║  Savings Rate:      XX%                                                      ║
║  Target Met:        ✅/❌ (≥75%)                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

**Violations = BLOCKING**
**Target: 75-90% savings**
**Quality: Maintain ≥80%**

---

**"Somente unidos seremos mais fortes!"** 💰🚀
