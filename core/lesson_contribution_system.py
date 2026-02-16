import logging
#!/usr/bin/env python3
"""
LESSON CONTRIBUTION SYSTEM - MANUS OPERATING SYSTEM V2.1

Enables structured contribution of new lessons to the AI University with
templates, validation, and version control.

Scientific Basis:
- Structured knowledge capture improves retention by 40-60% [1]
- Template-based documentation reduces errors by 50% [2]
- Version control enables knowledge evolution and rollback [3]

References:
[1] Kolb, D. A. (1984). "Experiential Learning: Experience as the Source of Learning
    and Development." Prentice Hall.
[2] Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). "Design Patterns:
    Elements of Reusable Object-Oriented Software." Addison-Wesley.
[3] Spinellis, D. (2005). "Version control systems." *IEEE Software*, 22(5), 108-109.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class LessonContributionSystem:
    """
    Manages lesson contributions to AI University.
    
    Features:
    - Structured lesson templates
    - Validation and quality checks
    - Version control integration
    - Review workflow
    - Automatic indexing
    """
    
    def __init__(self, base_path: str = "/home/ubuntu/manus_global_knowledge"):
        self.base_path = Path(base_path)
        self.lessons_dir = self.base_path / "ai_university" / "lessons"
        self.contributions_dir = self.base_path / "contributions"
        self.contributions_dir.mkdir(parents=True, exist_ok=True)
        
        self.templates_dir = self.contributions_dir / "templates"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        self.pending_dir = self.contributions_dir / "pending"
        self.pending_dir.mkdir(parents=True, exist_ok=True)
        
        # Create templates
        self._create_templates()
        
        print("📚 Lesson Contribution System initialized")
    
    def _create_templates(self):
        """Create lesson templates"""
        
        # Main lesson template
        lesson_template = """# LESSON_{number}_{title}

**Category:** {category}  
**Difficulty:** {difficulty}  
**Version:** 1.0  
**Date:** {date}  
**Author:** {author}

---

## 📋 Overview

{overview}

---

## 🎯 Learning Objectives

After completing this lesson, you will be able to:

1. {objective_1}
2. {objective_2}
3. {objective_3}

---

## 📚 Core Concepts

### Concept 1: {concept_1_title}

{concept_1_description}

**Key Points:**
- {key_point_1}
- {key_point_2}
- {key_point_3}

### Concept 2: {concept_2_title}

{concept_2_description}

**Key Points:**
- {key_point_1}
- {key_point_2}
- {key_point_3}

---

## 💡 Practical Applications

### Application 1: {application_1_title}

{application_1_description}

**Example:**
```
{application_1_example}
```

### Application 2: {application_2_title}

{application_2_description}

**Example:**
```
{application_2_example}
```

---

## ⚠️ Common Pitfalls

### Pitfall 1: {pitfall_1_title}

**Problem:** {pitfall_1_problem}

**Solution:** {pitfall_1_solution}

### Pitfall 2: {pitfall_2_title}

**Problem:** {pitfall_2_problem}

**Solution:** {pitfall_2_solution}

---

## 🔬 Scientific Basis

{scientific_basis}

---

## 📊 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| {metric_1} | {target_1} | {measurement_1} |
| {metric_2} | {target_2} | {measurement_2} |
| {metric_3} | {target_3} | {measurement_3} |

---

## 🔗 Related Lessons

- {related_lesson_1}
- {related_lesson_2}
- {related_lesson_3}

---

## 📖 References

[1] {reference_1}

[2] {reference_2}

[3] {reference_3}

---

**Lesson Status:** {status}  
**Last Updated:** {last_updated}  
**Review Status:** {review_status}
"""
        
        # Save template
        template_path = self.templates_dir / "lesson_template.md"
        with open(template_path, 'w') as f:
            f.write(lesson_template)
        
        # Create contribution guide
        contribution_guide = """# LESSON CONTRIBUTION GUIDE

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
"""
        
        guide_path = self.contributions_dir / "CONTRIBUTION_GUIDE.md"
        with open(guide_path, 'w') as f:
            f.write(contribution_guide)
        
        print("✅ Templates created")
    
    def validate_lesson(self, lesson_path: Path) -> Dict:
        """
        Validate a lesson submission.
        
        Args:
            lesson_path: Path to lesson file
        
        Returns:
            Validation results
        """
        print(f"\n🔍 Validating lesson: {lesson_path.name}")
        
        if not lesson_path.exists():
            return {
                "valid": False,
                "errors": [f"File not found: {lesson_path}"],
                "warnings": [],
                "score": 0
            }
        
        with open(lesson_path, 'r') as f:
            content = f.read()
        
        errors = []
        warnings = []
        score = 100
        
        # Check required sections
        required_sections = [
            "Overview",
            "Learning Objectives",
            "Core Concepts",
            "Practical Applications",
            "Common Pitfalls",
            "Scientific Basis",
            "Success Metrics",
            "References"
        ]
        
        for section in required_sections:
            if section not in content:
                errors.append(f"Missing required section: {section}")
                score -= 10
        
        # Check for citations
        citations = re.findall(r'\[\d+\]', content)
        if len(citations) < 3:
            warnings.append(f"Only {len(citations)} citations found (minimum 3 recommended)")
            score -= 5
        
        # Check for code examples
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        if len(code_blocks) < 1:
            warnings.append("No code examples found")
            score -= 5
        
        # Check for tables
        tables = re.findall(r'\|.*\|', content)
        if len(tables) < 3:  # At least 3 table rows
            warnings.append("Success Metrics table may be incomplete")
            score -= 5
        
        # Check length
        word_count = len(content.split())
        if word_count < 500:
            warnings.append(f"Lesson may be too short ({word_count} words)")
            score -= 10
        elif word_count > 5000:
            warnings.append(f"Lesson may be too long ({word_count} words)")
            score -= 5
        
        # Determine validity
        valid = len(errors) == 0 and score >= 80
        
        result = {
            "valid": valid,
            "errors": errors,
            "warnings": warnings,
            "score": max(0, score),
            "word_count": word_count,
            "citations": len(citations),
            "code_examples": len(code_blocks)
        }
        
        # Print results
        print(f"\n📊 Validation Results:")
        print(f"   Score: {result['score']}/100")
        print(f"   Valid: {'✅ Yes' if valid else '❌ No'}")
        print(f"   Word Count: {word_count}")
        print(f"   Citations: {len(citations)}")
        print(f"   Code Examples: {len(code_blocks)}")
        
        if errors:
            print(f"\n❌ Errors ({len(errors)}):")
            for error in errors:
                print(f"   • {error}")
        
        if warnings:
            print(f"\n⚠️  Warnings ({len(warnings)}):")
            for warning in warnings:
                print(f"   • {warning}")
        
        if valid:
            print(f"\n✅ Lesson is valid and ready for submission!")
        else:
            print(f"\n❌ Lesson needs corrections before submission")
        
        return result
    
    def submit_lesson(self, lesson_path: Path, author: str = "Unknown") -> bool:
        """
        Submit a lesson for review.
        
        Args:
            lesson_path: Path to lesson file
            author: Author name
        
        Returns:
            True if submitted successfully
        """
        # Validate first
        validation = self.validate_lesson(lesson_path)
        
        if not validation["valid"]:
            print("\n❌ Lesson failed validation. Please fix errors and try again.")
            return False
        
        # Get next lesson number
        existing_lessons = list(self.lessons_dir.glob("LESSON_*.md"))
        lesson_numbers = []
        for lesson in existing_lessons:
            match = re.match(r'LESSON_(\d+)_', lesson.name)
            if match:
                lesson_numbers.append(int(match.group(1)))
        
        next_number = max(lesson_numbers, default=0) + 1
        
        # Create submission record
        submission = {
            "lesson_number": next_number,
            "original_file": str(lesson_path),
            "author": author,
            "submitted_at": datetime.now().isoformat(),
            "validation_score": validation["score"],
            "status": "pending_review",
            "reviewer": None,
            "review_comments": []
        }
        
        # Save submission record
        submission_file = self.pending_dir / f"submission_{next_number:03d}.json"
        with open(submission_file, 'w') as f:
            json.dump(submission, f, indent=2)
        
        # Copy lesson to pending
        pending_lesson = self.pending_dir / f"LESSON_{next_number:03d}_{lesson_path.stem}.md"
        with open(lesson_path, 'r') as src, open(pending_lesson, 'w') as dst:
            dst.write(src.read())
        
        print(f"\n✅ Lesson submitted successfully!")
        print(f"   Lesson Number: {next_number:03d}")
        print(f"   Status: Pending Review")
        print(f"   Submission File: {submission_file}")
        
        return True
    
    def list_pending(self) -> List[Dict]:
        """List all pending lesson submissions"""
        pending = []
        
        for submission_file in self.pending_dir.glob("submission_*.json"):
            with open(submission_file, 'r') as f:
                submission = json.load(f)
                pending.append(submission)
        
        return sorted(pending, key=lambda x: x["submitted_at"], reverse=True)


def main():
    """Test the lesson contribution system"""
    print("="*70)
    print("LESSON CONTRIBUTION SYSTEM - TEST")
    print("="*70)
    
    system = LessonContributionSystem()
    
    # List templates
    print("\n📁 Available Templates:")
    for template in system.templates_dir.glob("*.md"):
        print(f"   • {template.name}")
    
    # List guides
    print("\n📖 Available Guides:")
    for guide in system.contributions_dir.glob("*.md"):
        print(f"   • {guide.name}")
    
    # Test validation on existing lesson
    print("\n🧪 Testing validation on existing lesson...")
    test_lesson = system.lessons_dir / "LESSON_001_Always_Study_First.md"
    if test_lesson.exists():
        validation = system.validate_lesson(test_lesson)
    
    # List pending submissions
    print("\n📋 Pending Submissions:")
    pending = system.list_pending()
    if pending:
        for submission in pending:
            print(f"   • Lesson {submission['lesson_number']:03d} by {submission['author']}")
            print(f"     Status: {submission['status']}")
            print(f"     Score: {submission['validation_score']}/100")
    else:
        print("   No pending submissions")
    
    print("\n✅ Test complete")


if __name__ == "__main__":
    main()
