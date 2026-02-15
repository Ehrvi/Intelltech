# LESSON CONTRIBUTION GUIDE

## How to Contribute a New Lesson

### Step 1: Choose a Topic

Identify a gap in the current AI University curriculum or an area where you have expertise.

**Current Lessons:** Check `/ai_university/lessons/` for existing topics

**Good Topics:**
- Specific techniques or methodologies
- Common problems and solutions
- Best practices in a domain
- Tool usage and optimization
- Decision-making frameworks

**Avoid:**
- Topics already covered
- Overly broad subjects
- Purely theoretical content without practical application

### Step 2: Use the Template

Copy the lesson template from `/contributions/templates/lesson_template.md`

Fill in all sections with detailed, actionable content.

**Required Sections:**
- Overview: Brief introduction (2-3 paragraphs)
- Learning Objectives: 3-5 specific, measurable objectives
- Core Concepts: 2-4 main concepts with key points
- Practical Applications: 2-3 real-world examples
- Common Pitfalls: 2-3 mistakes to avoid
- Scientific Basis: Research supporting the lesson
- Success Metrics: Measurable outcomes
- References: 3+ academic or technical sources

### Step 3: Follow Quality Standards

**Writing Style:**
- Clear, concise, professional
- Active voice preferred
- Technical accuracy required
- Examples must be realistic and tested

**Citations:**
- MANDATORY for all scientific claims
- Use academic format: Author(s). (Year). "Title." *Publication*, Volume(Issue), Pages.
- Minimum 3 references per lesson

**Code Examples:**
- Must be functional and tested
- Include comments explaining key parts
- Follow language best practices

**Formatting:**
- Use Markdown syntax
- Consistent heading levels
- Tables for structured data
- Code blocks with language tags

### Step 4: Validate Your Lesson

Run the validation script:

```bash
python3.11 /home/ubuntu/manus_global_knowledge/core/lesson_contribution_system.py validate your_lesson.md
```

This checks:
- All required sections present
- Citations properly formatted
- Code examples valid
- Success metrics defined
- No duplicate content

### Step 5: Submit for Review

Place your lesson in `/contributions/pending/` and run:

```bash
python3.11 /home/ubuntu/manus_global_knowledge/core/lesson_contribution_system.py submit your_lesson.md
```

This will:
- Assign a lesson number
- Create a review request
- Notify reviewers
- Track submission status

### Step 6: Address Review Feedback

Reviewers will check:
- Technical accuracy
- Completeness
- Clarity and readability
- Scientific rigor
- Practical applicability

Make requested changes and resubmit.

### Step 7: Publication

Once approved, your lesson will be:
- Added to AI University
- Indexed in the knowledge base
- Included in the bootstrap
- Credited to you

---

## Lesson Categories

- **Fundamentals:** Core concepts and principles
- **Methodologies:** Systematic approaches and frameworks
- **Tools:** Specific tool usage and optimization
- **Best Practices:** Proven patterns and techniques
- **Problem Solving:** Common issues and solutions
- **Advanced:** Complex topics requiring prerequisite knowledge

---

## Difficulty Levels

- **Beginner:** No prerequisites, foundational concepts
- **Intermediate:** Requires basic understanding
- **Advanced:** Requires multiple prerequisites
- **Expert:** Cutting-edge topics, extensive background needed

---

## Review Criteria

Lessons are evaluated on:

1. **Relevance (20%):** Addresses real needs
2. **Accuracy (25%):** Technically correct and current
3. **Clarity (20%):** Easy to understand and follow
4. **Completeness (15%):** All sections thoroughly covered
5. **Scientific Rigor (20%):** Properly cited and evidence-based

**Minimum Score:** 80/100 for approval

---

## Tips for Success

**Do:**
- Start with a clear outline
- Use real examples from your experience
- Cite authoritative sources
- Test all code examples
- Get feedback before submitting

**Don't:**
- Copy content without attribution
- Include unverified information
- Use overly complex language
- Skip the scientific basis section
- Submit without validation

---

## Questions?

Contact the AI University maintainers or check existing lessons for examples.

**Good Examples:**
- LESSON_001_Always_Study_First.md
- LESSON_009_Continuous_Learning_and_Adaptation.md
- LESSON_015_Scientific_Methodology_in_AI_Tasks.md
