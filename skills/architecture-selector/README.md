# Architecture Selector Skill

**Automatically selects the optimal AI execution architecture for any task.**

---

## Quick Start

```bash
# Test the selector
python3 /home/ubuntu/skills/architecture-selector/scripts/selector.py --test

# Analyze a specific task
python3 /home/ubuntu/skills/architecture-selector/scripts/selector.py "Your task description here"
```

---

## What It Does

This skill analyzes any task and recommends the best execution architecture:

- **Guardian** - GPT workers for bulk tasks (90% cost savings)
- **Direct Manus** - Full capabilities for strategic work
- **Parallel Map** - True parallelism for homogeneous tasks
- **Hybrid** - Combined approach for complex multi-stage work

---

## Example Results

```
Task: "Expand Apollo database with 3000 mining companies"

Recommended: guardian
Confidence: 92%
Reasoning: High volume (3000 items) with moderate complexity (5/10) suits Guardian GPT workers
Cost Estimate: $0.30 USD
```

---

## Integration

Use in Python:

```python
from architecture_selector import select_architecture

task = "Collect 500 companies from Australia"
arch = select_architecture(task, detailed=True)

print(f"Use: {arch['recommended']}")
print(f"Cost: {arch['cost_estimate']}")
```

---

## Files

- `SKILL.md` - Complete documentation
- `scripts/selector.py` - Core selection engine
- `README.md` - This file

---

## Created

2026-02-13 by Manus AI for IntellTech Project
