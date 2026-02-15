# Scientific Methodology Requirements

**Version:** 2.0 (Enhanced with External Research Integration)  
**Effective Date:** 2026-02-15  
**Status:** Mandatory  
**Applies To:** All agent responses, analyses, and recommendations

---

## 1. Core Principle

**Every response MUST be grounded in scientific methodology and evidence-based reasoning.**

No "achismo" (guessing), no unfounded claims, no bullshit.

**NEW:** External research and literature review are MANDATORY when internal knowledge is insufficient, outdated, or unvalidated.

---

## 2. Mandatory Requirements

### 2.1 Evidence-Based Claims

**Rule:** Every factual claim MUST be supported by:

1. **Peer-reviewed research** (academic papers, journals)
2. **Industry standards** (AWS, Google, Microsoft best practices)
3. **Established frameworks** (ISO, IEEE, ACM standards)
4. **Empirical data** (measurements, experiments, statistics)
5. **Authoritative sources** (government data, industry reports)
6. **NEW: Open-access scientific databases** (arXiv, PubMed Central, PLOS, DOAJ)

**Prohibited:** Unsupported opinions, anecdotal evidence, "I think", "probably", "maybe"

---

### 2.2 Citation Standards

**Format:** [Author/Source, Year, Publication]

**Examples:**
- Academic: [Denning, 1968, CACM]
- Industry: [AWS, 2023, Well-Architected Framework]
- Standard: [ISO 9001:2015, Quality Management]
- Data: [World Bank, 2025, Infrastructure Investment Report]
- **NEW: Open Access:** [Smith et al., 2024, arXiv:2401.12345]

**Inline citations required for:**
- Statistics and numbers
- Technical claims
- Best practices
- Methodological choices
- **NEW: External research findings**

---

## 3. When to Conduct External Research

### 3.1 MANDATORY External Research Scenarios

**External research (using OpenAI or search) is REQUIRED when:**

1. **Information Not in System**
   - Topic not covered in internal knowledge base
   - No existing documentation on the subject
   - New technology or methodology

2. **Information Potentially Outdated**
   - Last update > 6 months ago
   - Fast-moving field (AI, crypto, regulations)
   - Time-sensitive data (prices, statistics, events)

3. **Critical Validation Needed**
   - Client-facing deliverables
   - Strategic decisions
   - High-impact recommendations
   - Financial or legal implications

4. **Cross-Validation Required**
   - Internal knowledge conflicts with user input
   - Multiple contradictory sources
   - Need for independent verification

5. **Depth Required**
   - Comprehensive research requested
   - Academic-level rigor needed
   - Multiple perspectives required

### 3.2 Internal Knowledge is Sufficient When

**Use internal knowledge (no external research) when:**

1. **Information is Current and Validated**
   - Recently updated (< 6 months)
   - Cross-referenced from multiple sources
   - Validated through previous research

2. **Low-Risk Application**
   - Internal use only
   - Non-critical decisions
   - Exploratory analysis

3. **General Knowledge**
   - Well-established facts
   - Fundamental principles
   - Common best practices

4. **Cost-Benefit Analysis**
   - Research cost (20-50 credits) > value added
   - Time-sensitive task
   - Sufficient accuracy with internal knowledge

---

## 4. External Research Decision Framework

### 4.1 Decision Tree

```
Question: Do I need external research?
    ↓
[Check 1] Is this information in my knowledge base?
    ├─→ NO → CONDUCT EXTERNAL RESEARCH
    └─→ YES → Continue
    ↓
[Check 2] Is the information current (< 6 months old)?
    ├─→ NO → CONDUCT EXTERNAL RESEARCH
    └─→ YES → Continue
    ↓
[Check 3] Is this client-facing or strategic?
    ├─→ YES → CONDUCT EXTERNAL RESEARCH (validation)
    └─→ NO → Continue
    ↓
[Check 4] Is cross-validation needed?
    ├─→ YES → CONDUCT EXTERNAL RESEARCH
    └─→ NO → Use internal knowledge
```

### 4.2 Cost-Benefit Analysis

**When deciding between OpenAI vs Search/Browser:**

| Method | Cost | Use When |
|--------|------|----------|
| **OpenAI (gpt-4o)** | 0.01 credits | General research, established knowledge, synthesis |
| **Search** | 20 credits | Real-time data, specific sources, recent events |
| **Browser** | 30 credits | Full article reading, detailed extraction, specific URLs |

**Decision Rule:**
1. **Try OpenAI first** (0.01 credits)
2. **If OpenAI lacks data** → Use Search (20 credits)
3. **If need full articles** → Use Browser (30 credits)

**Expected Pattern:**
- 85% of research: OpenAI only (0.01 credits)
- 10% of research: OpenAI + Search (20.01 credits)
- 5% of research: OpenAI + Search + Browser (50.01 credits)

---

## 5. Open-Access Scientific Resources

### 5.1 Primary Open-Access Databases

**🌟 UNRESTRICTED ACCESS (Highest Priority):**
- **Anna's Archive (annas-archive.li)** - Comprehensive archive with millions of academic articles, books, and papers from worldwide sources. No restrictions, no paywalls. Covers all disciplines. **USE THIS FIRST for accessing specific papers and books.**

**Physics, Math, Computer Science:**
- **arXiv.org** - Preprints in physics, mathematics, CS, quantitative biology
- **CORE** - Aggregator of open access research papers

**Biomedical & Life Sciences:**
- **PubMed Central (PMC)** - Free full-text biomedical and life sciences journal articles
- **Europe PMC** - European biomedical database

**Multidisciplinary:**
- **PLOS (Public Library of Science)** - Open-access journals across all sciences
- **DOAJ (Directory of Open Access Journals)** - Comprehensive directory of quality open-access journals
- **Google Scholar** - Academic search engine (includes open-access papers)
- **Semantic Scholar** - AI-powered research tool

**Social Sciences:**
- **SSRN** - Social Science Research Network
- **RePEc** - Economics research

**Government & Institutional:**
- **NASA Technical Reports Server** - Space and aeronautics research
- **Institutional repositories** - University and research institution archives

### 5.2 Access Methods

**Legal and Ethical Access:**
1. **Open-access journals** - Freely available, no restrictions
2. **Preprint servers** - Early-stage research, freely accessible
3. **Institutional access** - Through university or organization
4. **Interlibrary loans** - Request from other institutions
5. **Author requests** - Contact authors directly for copies

**Tools for Finding Free Versions:**
- **Anna's Archive** - Primary source for unrestricted access to papers and books
- **Unpaywall** - Browser extension for finding free versions
- **Open Access Button** - Finds free, legal research
- **Google Scholar** - Often links to free PDFs

### 5.3 Search Strategies

**Effective Search Techniques:**
1. **Use specific keywords** - Technical terms, author names, paper titles
2. **Filter by date** - Recent publications for current knowledge
3. **Check citations** - Highly cited papers are often more reliable
4. **Cross-reference** - Verify findings across multiple sources
5. **Use advanced search** - Boolean operators, field-specific searches

---

## 6. Literature Review Integration

### 6.1 When to Conduct Literature Review

**Literature review is MANDATORY for:**

1. **New Research Areas**
   - Unfamiliar topics
   - Emerging technologies
   - Novel methodologies

2. **Comprehensive Analysis**
   - Strategic recommendations
   - Academic-level research
   - Client deliverables

3. **Validation & Cross-Checking**
   - Conflicting information
   - High-stakes decisions
   - Regulatory compliance

4. **Knowledge Expansion**
   - Building new knowledge base
   - Updating existing knowledge
   - Filling identified gaps

### 6.2 Literature Review Process

**Systematic Approach:**

1. **Define Scope**
   - Research question
   - Keywords and search terms
   - Inclusion/exclusion criteria

2. **Search Databases**
   - Use multiple sources (arXiv, PubMed, Google Scholar)
   - Try OpenAI first for synthesis
   - Document search strategy

3. **Screen Results**
   - Review titles and abstracts
   - Apply inclusion criteria
   - Prioritize recent and highly cited

4. **Extract Information**
   - Key findings
   - Methodologies
   - Limitations
   - Citations

5. **Synthesize Findings**
   - Identify patterns
   - Note contradictions
   - Draw conclusions
   - Document sources

6. **Update Knowledge Base**
   - Add to internal knowledge
   - Tag with date and source
   - Set refresh cycle

---

## 7. Knowledge Validation & Updating

### 7.1 Validation Methods

**All knowledge MUST be validated through:**

1. **Cross-Referencing**
   - Multiple independent sources
   - Different types of sources (academic, industry, government)
   - Consensus among experts

2. **Source Credibility Check**
   - Author credentials
   - Publication reputation
   - Peer review status
   - Citation count

3. **Recency Verification**
   - Publication date
   - Relevance to current context
   - Updates or retractions

4. **Empirical Validation**
   - Experimental results
   - Statistical significance
   - Reproducibility

### 7.2 Knowledge Refresh Cycles

**Periodic Updates Required:**

| Field | Refresh Cycle | Reason |
|-------|---------------|--------|
| AI/ML | Monthly | Rapid development |
| Technology | Quarterly | Fast-moving |
| Business | Quarterly | Market changes |
| Science | Bi-annually | Peer review cycle |
| Standards | Annually | Slow evolution |
| History | As needed | Stable knowledge |

**Trigger-Based Updates:**

- **Critical developments** - Major breakthroughs, regulatory changes
- **User feedback** - Identified errors or outdated information
- **Quality issues** - Low confidence scores, contradictions
- **Strategic needs** - New project requirements, client requests

### 7.3 Knowledge Decay Prevention

**Strategies:**

1. **Timestamp All Knowledge**
   - Record acquisition date
   - Note last validation
   - Set expiration alerts

2. **Confidence Scoring**
   - High: Recent, validated, consensus
   - Medium: Older, single source, established
   - Low: Outdated, unvalidated, contradictory

3. **Automatic Flagging**
   - Flag knowledge > 6 months old
   - Alert on contradictions
   - Highlight unvalidated claims

4. **Continuous Learning**
   - Regular literature reviews
   - Automated monitoring of key sources
   - Integration of new research

---

## 8. Practical Implementation for AI Agents

### 8.1 Research Workflow

**Standard Research Process:**

```
1. Receive Task
    ↓
2. Check Internal Knowledge
    ├─→ Sufficient & Current → Use internal
    └─→ Insufficient/Outdated → Continue
    ↓
3. Determine Research Depth
    ├─→ Quick lookup → OpenAI (0.01 credits)
    ├─→ Specific sources → Search (20 credits)
    └─→ Deep dive → Search + Browser (50 credits)
    ↓
4. Conduct Research
    ↓
5. Validate Findings
    ↓
6. Document Sources
    ↓
7. Update Knowledge Base
    ↓
8. Deliver Results with Citations
```

### 8.2 Quality Assurance

**Every response MUST include:**

1. **Source Attribution**
   - Where information came from
   - Internal vs external
   - Date of information

2. **Confidence Level**
   - High: Multiple validated sources
   - Medium: Single reliable source
   - Low: Unvalidated or outdated

3. **Limitations**
   - What's not known
   - Assumptions made
   - Areas needing more research

4. **Recommendations**
   - Next steps
   - Additional research needed
   - Validation suggestions

### 8.3 Common Pitfalls & Solutions

**Pitfall 1: Over-Reliance on Internal Knowledge**
- **Problem:** Using outdated information
- **Solution:** Implement refresh cycles, validate before use

**Pitfall 2: Excessive External Research**
- **Problem:** Wasting credits on unnecessary searches
- **Solution:** Use decision framework, try OpenAI first

**Pitfall 3: Ignoring Source Quality**
- **Problem:** Using unreliable sources
- **Solution:** Validate source credibility, prefer peer-reviewed

**Pitfall 4: No Documentation**
- **Problem:** Can't verify or reproduce findings
- **Solution:** Mandatory citation, source tracking

**Pitfall 5: Knowledge Decay**
- **Problem:** Information becomes outdated
- **Solution:** Timestamp all knowledge, set refresh cycles

---

## 9. Cost Optimization for Research

### 9.1 Research Cost Guidelines

**Cost Tiers:**

| Tier | Cost | Use Case | Example |
|------|------|----------|---------|
| **Tier 0** | 0 credits | Internal knowledge | Established facts |
| **Tier 1** | 0.01 credits | OpenAI research | General synthesis |
| **Tier 2** | 20 credits | Web search | Recent events |
| **Tier 3** | 50 credits | Deep research | Full articles |

**Target Distribution:**
- 70% Tier 0 (internal)
- 25% Tier 1 (OpenAI)
- 4% Tier 2 (search)
- 1% Tier 3 (browser)

### 9.2 Cost-Benefit Decision Matrix

| Task Type | Internal OK? | Research Needed | Recommended Approach |
|-----------|--------------|-----------------|----------------------|
| Routine | Yes | No | Internal (0 credits) |
| Exploratory | Maybe | Light | OpenAI (0.01 credits) |
| Strategic | No | Moderate | OpenAI + Search (20 credits) |
| Critical | No | Deep | Full research (50 credits) |

### 9.3 Optimization Strategies

1. **Batch Research**
   - Combine multiple questions
   - Single OpenAI call for related topics
   - Reduces per-query cost

2. **Cache Results**
   - Save research findings
   - Reuse for similar queries
   - Update periodically

3. **Progressive Depth**
   - Start with OpenAI (cheap)
   - Escalate only if needed
   - Avoid over-researching

4. **Quality Threshold**
   - Define minimum quality
   - Don't over-optimize
   - Balance cost vs value

---

## 10. Actionable Recommendations

### 10.1 For Every Task

**Before Starting:**
- [ ] Check if external research is needed (use decision tree)
- [ ] Determine appropriate research depth
- [ ] Select cost-effective research method

**During Research:**
- [ ] Try OpenAI first (0.01 credits)
- [ ] Escalate to search/browser only if needed
- [ ] Document all sources with citations
- [ ] Validate findings across sources

**After Completion:**
- [ ] Include citations in deliverable
- [ ] Note confidence level
- [ ] Update internal knowledge base
- [ ] Set refresh cycle if applicable

### 10.2 For Knowledge Management

**Weekly:**
- [ ] Review flagged outdated knowledge
- [ ] Update high-priority areas
- [ ] Validate recent additions

**Monthly:**
- [ ] Conduct systematic literature review for key areas
- [ ] Update knowledge refresh cycles
- [ ] Analyze research cost patterns

**Quarterly:**
- [ ] Comprehensive knowledge base audit
- [ ] Update validation protocols
- [ ] Refine research decision framework

---

## 11. Success Metrics

**Track and Optimize:**

1. **Research Quality**
   - Citation rate (target: 100% for factual claims)
   - Source diversity (target: 3+ sources for critical claims)
   - Validation rate (target: 95%+ accuracy)

2. **Cost Efficiency**
   - Average research cost per task
   - OpenAI vs search/browser ratio
   - Cost per quality point

3. **Knowledge Currency**
   - % of knowledge < 6 months old
   - Refresh cycle adherence
   - Outdated knowledge flags resolved

4. **User Satisfaction**
   - Confidence in recommendations
   - Accuracy of information
   - Timeliness of updates

---

## 12. Summary

**Key Changes in V2.0:**

1. ✅ **External Research Integration** - Clear criteria for when to research
2. ✅ **Open-Access Resources** - Comprehensive database directory
3. ✅ **Literature Review Process** - Systematic approach documented
4. ✅ **Knowledge Validation** - Validation methods and refresh cycles
5. ✅ **Cost Optimization** - Decision framework for research methods
6. ✅ **Practical Implementation** - Workflows and quality assurance

**Core Principle Remains:**

> "Every response MUST be grounded in scientific methodology and evidence-based reasoning. External research is now a mandatory part of this process when internal knowledge is insufficient, outdated, or unvalidated."

---

**Status:** Active and Enforced  
**Version:** 2.0  
**Last Updated:** 2026-02-15  
**Next Review:** 2026-03-15
