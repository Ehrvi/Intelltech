# SCIENTIFIC METHODOLOGY REQUIREMENTS

**Version:** 4.0 (Operating System V2.0 Integration)  
**Effective Date:** 2026-02-16  
**Status:** MANDATORY - Integrated with MANUS OPERATING SYSTEM V2.0  
**Applies To:** All agent responses, analyses, and recommendations

---

## 🎯 INTEGRATION WITH OPERATING SYSTEM V2.0

**This protocol is now part of the unified MANUS OPERATING SYSTEM V2.0.**

**Primary Source:** `/home/ubuntu/manus_global_knowledge/MANUS_OPERATING_SYSTEM.md`

**This document provides detailed implementation guidance for:**
- P1: Always Study First
- P4: Always Ensure Quality

**For the complete framework, refer to the Operating System V2.0.**

---

## 1. Core Principles

### 1.1 Scientific Foundation is Mandatory

**Implements:** Operating System V2.0 - P4: Always Ensure Quality

**Every output MUST be scientifically grounded and factually correct.**

No "achismo" (guessing), no unfounded claims, no bullshit.

**MANDATORY STANDARD:**
- **ALWAYS seek scientific knowledge** (default behavior)
- **Scientific research MUST be quality research, not superficial** (deep, thorough, comprehensive)
- **ALL outputs must be scientifically grounded** (not optional)
- **AI University lessons MUST have quality bibliographic references** (non-negotiable)
- **Only skip research if cost optimization system explicitly blocks** (rare exception)

**Enforcement:**
- Level: CRITICAL - BLOCKING
- Target: ≥80% quality score
- Enforced by: `master_enforcer.py::check_quality_standards()`

---

### 1.2 Research is Default, Not Exception

**Implements:** Operating System V2.0 - P1: Always Study First

**Default behavior:**
```
Task received → Study internal knowledge → Research externally if needed
```

**NOT this:**
```
Task received → Look for reasons to skip research
```

**Research Sources (in order of preference):**
1. **Internal Knowledge** (0.5 credits) - Check first
2. **OpenAI API** (0.01 credits) - Use for general research
3. **Anna's Archive** (via search) - Use for academic papers
4. **Web Search** (20 credits) - Use for current data
5. **Browser** (30 credits) - Use for deep investigation

**Enforcement:**
- Level: CRITICAL - BLOCKING
- Target: 100% compliance
- Enforced by: `master_enforcer.py::check_study_phase()`

---

### 1.3 Quality Research, Not Superficial

**Implements:** Operating System V2.0 - P4: Always Ensure Quality

**Scientific research MUST be quality research:**

**NOT quality research:**
- Quick searches
- Reading only abstracts
- Single source
- Superficial understanding
- Uncritical acceptance

**Quality research:**
- Multiple authoritative sources (minimum 3)
- Deep reading and understanding
- Critical evaluation
- Cross-referencing
- Synthesis of knowledge
- Verification of claims
- **MANDATORY: Bibliographic references for all scientific claims**

**The rule:** If doing research at all → Do quality research. Don't waste time and credits on superficial research.

**Scientific Basis:** Evidence-based practice demonstrates that properly cited research has 3x higher reliability and enables verification and reproducibility.[1]

[1] Sackett, D. L., Rosenberg, W. M., Gray, J. A., Haynes, R. B., & Richardson, W. S. (1996). "Evidence based medicine: what it is and what it isn't." *BMJ*, 312(7023), 71-72.

---

### 1.4 Quality Over Cost for Permanent Knowledge

**When creating permanent knowledge (AI University lessons, protocols, documentation):**
- Quality is PRIORITY #1
- Cost is secondary
- Use Guardian validation (≥80% quality)
- Invest in thorough research
- Create lasting value

**When solving temporary tasks:**
- Balance quality and cost
- Use cost optimization
- Still maintain scientific standards
- But don't over-invest

---

## 2. The 12-Step Scientific Method

**Implements:** Operating System V2.0 - P1 and P4

### Phase 1: Study (P1: Always Study First)

**Step 1: Study Internal Knowledge**
- Check MASTER_INDEX
- Review relevant lessons
- Search knowledge cache
- Understand existing knowledge
- **Tool:** `file_read` (0.5 credits)

**Step 2: Research Externally**
- Use OpenAI for general research (0.01 credits)
- Use Anna's Archive for academic papers
- Use web search for current data (20 credits)
- Cross-reference multiple sources
- **Tools:** OpenAI API, search, browser

**Step 3: Understand Deeply**
- Synthesize information
- Identify patterns
- Evaluate critically
- Form comprehensive understanding
- **Tool:** Internal reasoning

---

### Phase 2: Analyze (P4: Always Ensure Quality)

**Step 4: Define Problem**
- Clarify objectives
- Identify constraints
- Determine success criteria
- **Tool:** Internal reasoning

**Step 5: Formulate Hypothesis**
- Propose solution approach
- Identify assumptions
- Consider alternatives
- **Tool:** Internal reasoning

**Step 6: Design Method**
- Plan execution steps
- Select appropriate tools
- Optimize for cost and quality
- **Tool:** Internal reasoning + cost optimization

---

### Phase 3: Execute (P3: Always Optimize Cost)

**Step 7: Collect Data**
- Gather required information
- Use cost-optimized tools
- Validate data quality
- **Tools:** OpenAI (preferred), search, browser

**Step 8: Process Data**
- Clean and organize
- Apply analysis methods
- Generate insights
- **Tools:** Python, shell, file operations

**Step 9: Validate Results**
- Cross-check findings
- Test assumptions
- Verify accuracy
- **Tools:** Guardian (for critical outputs)

---

### Phase 4: Deliver (P5: Always Report Accurately)

**Step 10: Synthesize Findings**
- Integrate all insights
- Draw conclusions
- Identify implications
- **Tool:** Internal reasoning

**Step 11: Document Results**
- Create clear documentation
- Include citations
- Explain methodology
- **Tool:** `file_write`

**Step 12: Report to User**
- Present findings clearly
- Include cost report
- Provide recommendations
- **Tool:** `message` with cost report

---

## 3. Quality Standards

### 3.1 Source Quality

**Authoritative sources (preferred):**
- Academic papers (peer-reviewed)
- Government publications
- Industry standards
- Established textbooks
- Reputable organizations

**Acceptable sources:**
- Technical documentation
- Professional blogs (verified experts)
- News from credible outlets
- Company official publications

**Avoid:**
- Random blogs
- Unverified claims
- Social media posts
- Promotional content
- Outdated information

---

### 3.2 Citation Standards

**Every factual claim MUST be cited.**

**MANDATORY REQUIREMENT:** All scientific claims, research findings, statistics, and methodological statements MUST include bibliographic references.

**Citation format (inline numeric):**
```markdown
According to [source name], [claim].[1]

[1]: Author(s). (Year). "Title." *Publication*, Volume(Issue), Pages. DOI/URL.
```

**Example (Academic):**
```markdown
Research demonstrates that vector embeddings enable semantic similarity search with 95%+ accuracy.[1]

[1]: Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018). "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." arXiv:1810.04805.
```

**Example (Technical Documentation):**
```markdown
According to the OpenAI documentation, GPT-4o costs $5 per 1M input tokens.[1]

[1]: OpenAI. (2026). "Pricing." https://openai.com/pricing (accessed 2026-02-16).
```

**Citation Requirements:**
- Academic papers: Author, year, title, journal, volume, pages, DOI
- Books: Author, year, title, edition, publisher
- Websites: Organization, year, title, URL, access date
- Technical docs: Organization, year, title, URL, access date

**When to cite:**
- ✅ Scientific findings and research results
- ✅ Statistical data and percentages
- ✅ Methodological approaches and frameworks
- ✅ Theoretical concepts and principles
- ✅ Technical specifications and standards
- ❌ Common knowledge (e.g., "water boils at 100°C")
- ❌ Your own original analysis (but cite sources used)

**Scientific Basis:** Proper citation enables verification, reproducibility, and builds on existing knowledge - core principles of scientific method.[1]

[1]: Merton, R. K. (1973). *The Sociology of Science: Theoretical and Empirical Investigations*. University of Chicago Press.

---

### 3.3 Validation Requirements

**For critical outputs (lessons, protocols, permanent knowledge):**
- MUST use Guardian validation
- Target: ≥80% quality score
- If score < 80%: Revise and revalidate
- Document validation results

**For routine outputs:**
- Self-validation sufficient
- Cross-check key facts
- Verify calculations
- Ensure logical consistency

---

## 4. Research Workflows

### 4.1 General Research Workflow

```
1. Check internal knowledge (file_read, 0.5 credits)
   ↓
2. Use OpenAI for overview (0.01 credits)
   ↓
3. If needed: Deep research (search/browser, 20-30 credits)
   ↓
4. Synthesize and validate
   ↓
5. Document with citations
```

**Cost-optimized:** Start cheap, go deeper only if needed.

---

### 4.2 Academic Research Workflow

```
1. Check internal knowledge
   ↓
2. Search Anna's Archive for papers
   ↓
3. Read and analyze papers
   ↓
4. Cross-reference findings
   ↓
5. Synthesize with proper citations
   ↓
6. Validate with Guardian (≥80%)
```

**Quality-focused:** Invest in thorough research for permanent knowledge.

---

### 4.3 Current Data Research Workflow

```
1. Check if internal knowledge is current
   ↓
2. If outdated: Use web search (20 credits)
   ↓
3. Verify data from multiple sources
   ↓
4. Document with timestamps
   ↓
5. Update knowledge cache
```

**Currency-focused:** Ensure data is up-to-date and accurate.

---

## 5. Integration with Operating System V2.0

### 5.1 Relationship to Core Principles

| Scientific Method | Operating System Principle |
|-------------------|----------------------------|
| Study Internal Knowledge | P1: Always Study First |
| Research Externally | P1: Always Study First |
| Understand Deeply | P1: Always Study First |
| Optimize Tool Selection | P3: Always Optimize Cost |
| Validate Quality | P4: Always Ensure Quality |
| Document Results | P5: Always Report Accurately |

---

### 5.2 Enforcement Integration

**Master Enforcer checks:**
- `check_study_phase()` - Validates Steps 1-3
- `check_quality_standards()` - Validates Steps 9-11
- `check_cost_report()` - Validates Step 12

**Legacy enforcers:**
- Guardian validation system
- Quality scoring system
- Citation verification

---

## 6. Compliance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Research completion | 100% | % tasks with research phase |
| Source quality | ≥80% | % authoritative sources |
| Citation coverage | 100% | % claims with citations |
| Quality score | ≥80% | Guardian validation score |
| Method adherence | ≥95% | % tasks following 12 steps |

---

## 7. Implementation Checklist

### Before Starting Research
- [ ] Checked internal knowledge first
- [ ] Identified knowledge gaps
- [ ] Planned research approach
- [ ] Selected cost-optimized tools

### During Research
- [ ] Using multiple authoritative sources (≥3)
- [ ] Reading deeply, not superficially
- [ ] Cross-referencing information
- [ ] Documenting sources as I go

### After Research
- [ ] Synthesized findings
- [ ] Validated quality
- [ ] Cited all sources
- [ ] Ready to deliver results

---

## 8. Examples

### Example 1: Creating AI University Lesson

**Task:** Create lesson on cost optimization

**Scientific Method Applied:**
1. Study existing lessons (file_read)
2. Research cost optimization best practices (OpenAI)
3. Search for academic papers (Anna's Archive)
4. Define lesson objectives
5. Formulate key principles
6. Design lesson structure
7. Collect examples and data
8. Process and organize content
9. Validate with Guardian (≥80%)
10. Synthesize final lesson
11. Document with citations
12. Deliver to user with cost report

**Result:** High-quality, scientifically grounded lesson with proper citations.

---

### Example 2: Answering User Question

**Task:** "What is the best approach for web scraping?"

**Scientific Method Applied:**
1. Check internal knowledge (file_read)
2. Research current best practices (OpenAI)
3. Understand deeply (synthesis)
4. Define user's specific needs
5. Formulate recommendation
6. Design solution approach
7. Collect supporting evidence
8. Process and organize
9. Validate approach
10. Synthesize recommendation
11. Document reasoning
12. Deliver with cost report

**Result:** Well-researched, practical recommendation with clear reasoning.

---

## 9. Version History

**V4.0 (2026-02-16):**
- Integrated with MANUS OPERATING SYSTEM V2.0
- Mapped 12 steps to 5 Core Principles
- Added Master Enforcer integration
- Clarified research workflows
- Updated compliance metrics

**V3.0 (2026-02-15):**
- Made scientific foundation mandatory
- Established quality research standards
- Added Guardian validation requirements
- Created 12-step methodology

**V2.0 (2026-02-14):**
- Expanded research requirements
- Added citation standards
- Introduced quality metrics

**V1.0 (2026-02-13):**
- Initial methodology definition
- Basic research principles

---

**For the complete framework, see:** `MANUS_OPERATING_SYSTEM.md`

**Status:** 🟢 ACTIVE - Integrated with Operating System V2.0
