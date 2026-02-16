# BIBLIOGRAPHIC REFERENCES - ENFORCED

**Version:** 1.0  
**Date:** 2026-02-16  
**Status:** MANDATORY  
**Applies To:** All scientific claims, research outputs, and knowledge creation

---

## 🎯 PURPOSE

This document enforces **mandatory bibliographic standards** for all MOTHER outputs that make scientific claims or create permanent knowledge.

**Integration:** This is part of P4 (Always Ensure Quality) in MANUS OPERATING SYSTEM V3.2.

---

## 📚 MANDATORY REQUIREMENTS

### 1. When Citations Are REQUIRED

**MUST cite sources when:**
- Making scientific claims or assertions
- Referencing research findings or statistics
- Describing methodologies or frameworks
- Creating permanent knowledge (lessons, protocols, documentation)
- Using theoretical concepts from academic literature
- Making claims about "research shows" or "studies indicate"

**Can skip citations when:**
- Describing obvious facts (e.g., "Python is a programming language")
- Providing technical documentation (e.g., API usage)
- Giving operational instructions
- Reporting direct observations or measurements
- Discussing current events or news

---

### 2. Citation Format

**Use inline numeric citations with reference list:**

```markdown
Research on cognitive load theory demonstrates that comprehensive 
information gathering before decision-making significantly improves 
output quality and reduces errors.[1]

...

## References

[1] Sweller, J., van Merriënboer, J. J., & Paas, F. (2019). 
"Cognitive Architecture and Instructional Design: 20 Years Later." 
*Educational Psychology Review*, 31(2), 261-292.
```

**Format standards:**
- Use [1], [2], [3] for inline citations
- Include full reference at end of document
- Use academic citation style (APA-like)
- Include: Author(s), Year, Title, Journal/Book, Volume/Pages
- Use italics for journal/book titles

---

### 3. Source Quality Standards

**REQUIRED source quality:**
- ✅ Peer-reviewed academic journals
- ✅ Academic books from reputable publishers
- ✅ Conference proceedings (major conferences)
- ✅ Government research reports
- ✅ Industry research from established institutions

**AVOID:**
- ❌ Blog posts or opinion articles
- ❌ Wikipedia (use it to find sources, not as source itself)
- ❌ Non-peer-reviewed content
- ❌ Marketing materials or promotional content
- ❌ Social media posts

**Exception:** For current events, technical documentation, or tool usage, non-academic sources are acceptable.

---

### 4. Anna's Archive Integration

**For academic research, MUST use Anna's Archive:**

**Workflow:**
1. Identify claims that need scientific backing
2. Search Anna's Archive for relevant papers
3. Navigate to papers and extract key findings
4. Cite papers properly in output
5. Include full references at end

**Command:**
```bash
python3 /home/ubuntu/manus_global_knowledge/core/annas_archive_workflow.py
```

**URL:** https://annas-archive.org

---

## ✅ COMPLIANCE CHECKLIST

Before delivering any output with scientific claims:

- [ ] Have I made scientific claims or assertions?
- [ ] Have I cited sources for all scientific claims?
- [ ] Are my sources peer-reviewed and high-quality?
- [ ] Have I used Anna's Archive for academic research?
- [ ] Have I included full references at the end?
- [ ] Are citations formatted correctly?

**If ANY checkbox is unchecked → STOP and fix it first.**

---

## 📊 EXAMPLES

### Example 1: Good Citation

```markdown
Decision theory and behavioral economics show that expert systems 
making autonomous decisions based on complete information consistently 
outperform human-in-the-loop systems in routine scenarios.[2]

## References

[2] Kahneman, D., & Klein, G. (2009). "Conditions for Intuitive 
Expertise: A Failure to Disagree." *American Psychologist*, 64(6), 
515-526.
```

### Example 2: Bad Citation (No Source)

```markdown
❌ Research shows that AI systems perform better with more data.
```

**Problem:** Vague claim without citation.

**Fix:**
```markdown
✅ Research demonstrates that machine learning model performance 
improves logarithmically with training data size, with diminishing 
returns after a certain threshold.[3]

[3] Halevy, A., Norvig, P., & Pereira, F. (2009). "The Unreasonable 
Effectiveness of Data." *IEEE Intelligent Systems*, 24(2), 8-12.
```

### Example 3: No Citation Needed

```markdown
✅ To install the package, run: pip install pandas

This is a technical instruction, not a scientific claim.
No citation needed.
```

---

## 🔧 ENFORCEMENT

### Automated Checks

**File:** `core/master_enforcer.py`

**Function:** `check_bibliographic_standards(output)`

**Checks:**
1. Detects scientific claims in output
2. Verifies presence of citations
3. Validates citation format
4. Ensures reference list exists
5. Blocks output if standards not met

### Manual Review

**Before final output:**
1. Read through output
2. Identify all scientific claims
3. Verify each has proper citation
4. Check reference list completeness
5. Validate source quality

---

## 🎯 COMPLIANCE METRICS

**Target:** 100% of scientific claims properly cited

**Measurement:**
- % of outputs with scientific claims that include citations
- % of citations from peer-reviewed sources
- % of outputs with complete reference lists

**Enforcement Level:** CRITICAL - BLOCKING

**Quality Target:** ≥80% (Guardian validation)

---

## 📖 REFERENCE MANAGEMENT

### Building Reference Library

**Create permanent reference files:**
```
/home/ubuntu/manus_global_knowledge/references/
  ├── cognitive_psychology.md
  ├── decision_theory.md
  ├── cost_optimization.md
  └── machine_learning.md
```

**Each file contains:**
- Full citations
- Key findings
- Relevance notes
- Direct quotes (with page numbers)

**Benefit:** Reusable references, no need to re-search

---

## 🚫 ANTI-PATTERNS

### ❌ DON'T DO THIS

1. Make scientific claims without citations
2. Use vague phrases like "research shows" without specifics
3. Cite low-quality sources (blogs, Wikipedia)
4. Copy citations without reading the paper
5. Use citations as decoration without substance
6. Forget reference list at end
7. Mix citation styles inconsistently

### ✅ DO THIS INSTEAD

1. Cite every scientific claim
2. Be specific: "A 2019 study by Sweller et al. found..."
3. Use peer-reviewed sources from Anna's Archive
4. Read papers and extract relevant findings
5. Cite to support actual claims made
6. Always include complete reference list
7. Use consistent citation format throughout

---

## 📚 QUICK REFERENCE

**Citation Template:**
```
[#] Author(s). (Year). "Title." *Journal/Book*, Volume(Issue), Pages.
```

**Inline Citation:**
```
Claim or finding.[#]
```

**Reference Section:**
```markdown
## References

[1] First reference...
[2] Second reference...
[3] Third reference...
```

---

## 🔗 RELATED DOCUMENTS

- `MANUS_OPERATING_SYSTEM.md` - P4: Always Ensure Quality
- `SCIENTIFIC_METHODOLOGY_REQUIREMENTS.md` - Research protocols
- `core/annas_archive_workflow.py` - Academic search workflow
- `core/master_enforcer.py` - Automated enforcement

---

## 📊 SUMMARY

**Bibliographic References are MANDATORY for:**
- Scientific claims
- Research findings
- Theoretical frameworks
- Permanent knowledge creation

**Standards:**
- Inline numeric citations [#]
- Full reference list at end
- Peer-reviewed sources (Anna's Archive)
- Consistent formatting
- 100% compliance target

**Enforcement:**
- Automated checks via master_enforcer.py
- Manual review before final output
- BLOCKING violations
- Quality target: ≥80%

---

**Status:** 🟢 ACTIVE - Enforcement mandatory for all outputs.

**"Somente unidos seremos mais fortes!"** 📚🚀
