#!/usr/bin/env python3
"""
Anna's Archive Integration Workflow
Provides workflow for searching and using academic papers from Anna's Archive

MANDATORY: Use this workflow for ALL academic research
"""

import os
import sys

def print_annas_archive_workflow():
    """Print the Anna's Archive workflow guide"""
    
    workflow = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    📚 ANNA'S ARCHIVE WORKFLOW                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  MANDATORY for ALL academic research                                        ║
║  URL: https://annas-archive.org                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

## WHEN TO USE

✅ MUST use Anna's Archive when:
- Creating permanent knowledge (lessons, protocols, documentation)
- Making scientific claims that need peer-reviewed backing
- Researching academic topics (psychology, economics, engineering, etc.)
- Citing specific research findings or methodologies
- Building theoretical frameworks

❌ Can skip Anna's Archive when:
- Researching current events or news
- Looking for technical documentation (APIs, tools)
- Cost optimization system explicitly blocks (rare)
- Time-sensitive tasks where speed is critical

---

## WORKFLOW

### Step 1: Identify Research Needs

Before searching, clearly define:
- What specific knowledge do you need?
- What claims need scientific backing?
- What methodologies or frameworks to research?

### Step 2: Search Anna's Archive

**Method 1: Via Web Browser**
1. Navigate to https://annas-archive.org
2. Search for:
   - Specific papers (author + year + title)
   - Topics (e.g., "persuasion psychology")
   - Authors (e.g., "Robert Cialdini")
3. Filter by:
   - Type: Academic papers, books
   - Language: English
   - Format: PDF

**Method 2: Via Search Tool**
```python
# Use Manus search tool with type="research"
search(
    type="research",
    queries=["Cialdini persuasion principles", "influence psychology"]
)
```

### Step 3: Download and Read Papers

**Priority papers to download:**
1. Seminal works (highly cited, foundational)
2. Recent reviews/meta-analyses (comprehensive overview)
3. Specific studies (for particular claims)

**How to read efficiently:**
1. Abstract: Get overview (2 min)
2. Introduction: Understand context (5 min)
3. Methodology: Assess rigor (5 min)
4. Results: Extract key findings (10 min)
5. Discussion: Understand implications (5 min)
6. References: Find related papers (2 min)

**Total time per paper:** ~30 minutes for thorough reading

### Step 4: Extract and Synthesize

**What to extract:**
- Key findings and statistics
- Methodologies and frameworks
- Theoretical models
- Practical applications
- Limitations and caveats

**How to cite:**
```markdown
According to Cialdini's research on influence, there are six universal 
principles of persuasion: reciprocity, commitment, social proof, authority, 
liking, and scarcity.[1]

[1] Cialdini, R. B. (2001). "Influence: Science and Practice" (4th ed.). 
Allyn & Bacon.
```

### Step 5: Integrate into Knowledge

**For permanent knowledge:**
1. Create "Scientific Foundation" section
2. Cite specific papers for each claim
3. Include full references section
4. Cross-reference related papers

**For temporary tasks:**
1. Cite key papers inline
2. Include condensed references
3. Focus on actionable insights

---

## CITATION STANDARDS

### Academic Papers
```
[1] Author(s). (Year). "Title." Journal, Volume(Issue), Pages. DOI.

Example:
[1] Petty, R. E., & Cacioppo, J. T. (1986). "The Elaboration Likelihood 
Model of Persuasion." Advances in Experimental Social Psychology, 19, 123-205.
```

### Books
```
[1] Author(s). (Year). "Title" (Edition). Publisher.

Example:
[1] Kahneman, D. (2011). "Thinking, Fast and Slow." Farrar, Straus and Giroux.
```

### Book Chapters
```
[1] Author(s). (Year). "Chapter Title." In Editor(s) (Eds.), Book Title 
(pp. pages). Publisher.
```

---

## QUALITY CRITERIA

**Good academic sources:**
✅ Peer-reviewed journals
✅ University press books
✅ Meta-analyses and systematic reviews
✅ Highly cited papers (>100 citations)
✅ Recent publications (<10 years for most fields)

**Avoid:**
❌ Predatory journals
❌ Non-peer-reviewed sources
❌ Blog posts or opinion pieces
❌ Outdated research (>20 years, unless seminal)
❌ Single studies without replication

---

## COST-BENEFIT ANALYSIS

**When to invest time in deep research:**
- Creating AI University lessons (permanent knowledge)
- Building frameworks for repeated use
- Making critical business decisions
- Establishing thought leadership

**When to use lighter research:**
- One-time tasks
- Time-sensitive deliverables
- Topics with existing internal knowledge
- Non-critical applications

**Rule of thumb:**
- Permanent knowledge: 2-4 hours research (10-15 papers)
- Important tasks: 1-2 hours research (5-7 papers)
- Routine tasks: 15-30 minutes research (2-3 papers)

---

## INTEGRATION WITH MOTHER

**P1: Always Study First**
- Anna's Archive is part of "Study First"
- Check internal knowledge → OpenAI → Anna's Archive → Web

**P3: Always Optimize Cost**
- Anna's Archive is FREE (no API costs)
- Time investment pays off for permanent knowledge
- Skip for temporary tasks if time-constrained

**P4: Always Ensure Quality**
- Guardian validation requires proper citations
- Anna's Archive provides authoritative sources
- Quality score ≥80% needs academic backing

**P5: Always Report Accurately**
- Include research time in cost report
- Document papers consulted
- Track knowledge creation vs. task execution

---

## EXAMPLES

### Example 1: Creating AI University Lesson on Persuasion

**Research process:**
1. Search Anna's Archive: "Cialdini influence persuasion"
2. Download: "Influence: Science and Practice" (2001)
3. Search: "Petty Cacioppo elaboration likelihood model"
4. Download: ELM paper (1986)
5. Search: "Kahneman Tversky cognitive biases"
6. Download: "Thinking, Fast and Slow" (2011)
7. Read all 3 sources (90 minutes total)
8. Extract key frameworks and findings
9. Create lesson with proper citations
10. Validate with Guardian (≥80%)

**Result:** High-quality permanent knowledge

### Example 2: Quick Research for Copywriting Task

**Research process:**
1. Search Anna's Archive: "copywriting persuasion"
2. Download: Top meta-analysis paper
3. Skim abstract and results (15 minutes)
4. Extract 3-4 key principles
5. Apply to copywriting task
6. Cite paper inline

**Result:** Scientifically-backed copy in minimal time

---

## TROUBLESHOOTING

**Problem:** Can't find specific paper
**Solution:** 
- Try alternative search terms
- Search by author name
- Look for related review papers
- Use Google Scholar to find DOI, then search DOI

**Problem:** Paper is too technical
**Solution:**
- Read abstract and discussion only
- Look for review papers (more accessible)
- Use OpenAI to summarize key points
- Focus on practical implications

**Problem:** Too many results
**Solution:**
- Filter by citation count (>100)
- Filter by date (last 10 years)
- Look for meta-analyses first
- Prioritize top-tier journals

**Problem:** Limited time
**Solution:**
- Use OpenAI for initial overview
- Download 2-3 most cited papers
- Read abstracts only
- Extract key citations for later deep dive

---

## ENFORCEMENT

**This workflow is MANDATORY for:**
- ✅ Creating permanent knowledge
- ✅ Making scientific claims
- ✅ Academic research topics
- ✅ Guardian validation (≥80%)

**Violations will result in:**
- ❌ Guardian score < 80%
- ❌ Output rejection
- ❌ Revision requirement

**Compliance check:**
```python
from core.mandatory_scientific_enforcement import enforce_scientific_standards

result = enforce_scientific_standards({
    'research_log': {
        'requires_academic_papers': True,
        'used_annas_archive': True  # MUST be True
    },
    ...
})
```

---

## RESOURCES

- **Anna's Archive:** https://annas-archive.org
- **Google Scholar:** https://scholar.google.com (for finding papers)
- **Sci-Hub:** Alternative source (use as backup)
- **Library Genesis:** Alternative source (use as backup)

---

**Remember:** Anna's Archive is a FREE resource that provides access to the world's 
knowledge. Use it to create high-quality, scientifically-backed work that stands 
the test of time.

**"Knowledge is power. Free knowledge is unstoppable."**
"""
    
    return workflow

def main():
    """Print the workflow"""
    print(print_annas_archive_workflow())

if __name__ == "__main__":
    main()
