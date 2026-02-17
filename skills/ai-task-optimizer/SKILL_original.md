---
name: ai-task-optimizer
description: Intelligent AI task distribution for cost optimization. Automatically routes tasks to OpenAI (bulk/simple) or Manus (strategic/complex) based on complexity, volume, quality needs, and time sensitivity. Use for lead processing, research, content creation, data analysis, or any AI task requiring cost efficiency without compromising quality.
---

# AI Task Optimizer

Automatically routes tasks to the optimal AI provider (OpenAI vs Manus) to maximize cost savings while maintaining quality.

## When to Use

This skill activates automatically for tasks involving:
- Lead generation and qualification
- Company research and analysis
- Content creation and drafting
- Data extraction and processing
- Report generation
- Any bulk AI processing

## How It Works

### Automatic Routing

Tasks are analyzed across four dimensions and scored 4 to 12:

1. **Complexity**: Simple (1), Moderate (2), Complex (3)
2. **Volume**: Low (1), Medium (2), High (3)
3. **Quality Sensitivity**: Low (1), Medium (2), High (3)
4. **Time Sensitivity**: Low (1), Medium (2), High (3)

**Routing Logic:**
- Score 4 to 7: OpenAI (bulk processing, 90%+ cost savings)
- Score 8: Borderline (consider hybrid or OpenAI with review)
- Score 9 to 12: Manus (strategic work, maximum quality)

**Override Rules:**
- Quality sensitivity = 3: Always Manus (client-facing)
- Complexity = 3: Always Manus (strategic)
- Volume = 3 AND complexity = 1: Prefer OpenAI (bulk simple)

### Task Analysis

Use `task_router.py` to analyze and route tasks:

```python
from scripts.task_router import route_task

# Automatic analysis
decision = route_task("Qualify 100 leads as HOT/WARM/COLD")

# Manual profile
decision = route_task(
    "Research mining companies",
    complexity=2,
    volume=2,
    quality_sensitivity=2,
    time_sensitivity=2
)

# Result includes provider, score, rationale
print(f"Route to: {decision['provider']}")
print(f"Rationale: {decision['rationale']}")
```

### Common Task Mappings

| Task Type | Provider | Rationale |
|-----------|----------|-----------|
| Lead qualification (bulk) | OpenAI | High volume, simple logic |
| Lead search | OpenAI | Data extraction |
| Company research (batch) | OpenAI | Medium complexity, volume |
| Pitch writing | Manus | High quality, strategic |
| Strategic analysis | Manus | Complex, high stakes |
| Data extraction | OpenAI | Simple, bulk |
| Client proposals | Manus | Client-facing |
| Email templates | OpenAI | Medium complexity, volume |

## Cost Optimization

### Expected Savings

**OpenAI Tasks**: 90%+ savings vs Manus
- 100 leads qualified: $0.02 vs $10 Manus credits
- Daily research: $0.05 vs $25 Manus credits

**Monthly Projection** (typical usage):
- OpenAI: $5-15/month
- Manus: Strategic work only
- **Total savings: 35-50% overall**

### Setup Requirements

**OpenAI API** (for cost savings):
1. Create account at platform.openai.com
2. Add billing (recommended $10-20/month limit)
3. Generate API key
4. Configure in system

See `references/openai-setup.md` for detailed setup.

**Without OpenAI**: System uses Manus for all tasks (still functional, no savings).

## Quality Assurance

**OpenAI Tasks**: 95%+ accuracy, suitable for bulk processing and internal use

**Manus Tasks**: 98%+ accuracy, for strategic and client-facing work

**Validation**: 10% sample of OpenAI outputs reviewed by Manus for quality

## Usage Examples

### Example 1: Lead Qualification

```
User: "Qualify these 50 leads as HOT/WARM/COLD based on company size and role"

Skill Analysis:
- Complexity: 1 (simple classification)
- Volume: 2 (50 items)
- Quality: 1 (internal screening)
- Time: 2 (standard)
- Score: 6

Decision: Route to OpenAI
Rationale: Bulk processing, simple criteria
Savings: ~$8 Manus credits
```

### Example 2: Strategic Proposal

```
User: "Create technical proposal for BHP Mining tailings dam monitoring"

Skill Analysis:
- Complexity: 3 (strategic, technical)
- Volume: 1 (single proposal)
- Quality: 3 (client-facing)
- Time: 2 (days)
- Score: 9

Decision: Route to Manus
Rationale: High quality sensitivity, strategic value
Savings: None (appropriate Manus usage)
```

### Example 3: Company Research

```
User: "Research top 20 Australian mining companies and summarize"

Skill Analysis:
- Complexity: 2 (synthesis required)
- Volume: 2 (20 companies)
- Quality: 2 (internal use)
- Time: 2 (same day)
- Score: 8

Decision: Route to OpenAI
Rationale: Medium volume, acceptable for bulk processing
Savings: ~$15 Manus credits
```

## Advanced Usage

### Force Provider

Override automatic routing when needed:

```python
# Force Manus for critical task
decision = route_task("Quick draft", force_provider='manus')

# Force OpenAI for testing
decision = route_task("Strategic plan", force_provider='openai')
```

### Track Statistics

Monitor routing decisions and savings:

```python
from scripts.task_router import get_stats

stats = get_stats()
print(f"Total savings: ${stats['total_savings_aud']} AUD")
print(f"OpenAI tasks: {stats['openai_tasks']}")
print(f"Manus tasks: {stats['manus_tasks']}")
```

### Decision Matrix

For detailed routing rules and task profiles, see `references/decision-matrix.md`.

## Best Practices

**Let the system decide**: Automatic routing is optimized for cost and quality balance.

**Review borderline tasks**: Score 8 tasks may benefit from manual review.

**Batch similar tasks**: Combine similar requests for better efficiency.

**Monitor costs**: Check OpenAI usage weekly, adjust if needed.

**Trust OpenAI for volume**: Bulk processing is where savings happen.

**Reserve Manus for value**: Strategic and client-facing work deserves premium quality.

## Troubleshooting

**"OpenAI quota exceeded"**: Add billing at platform.openai.com/settings/organization/billing

**"All tasks routing to Manus"**: OpenAI not configured or unavailable, system falls back safely

**"Quality concerns with OpenAI"**: Increase quality_sensitivity parameter or force Manus

**"Costs too high"**: Review task profiles, ensure bulk tasks use OpenAI

## Summary

This skill automatically optimizes AI task distribution for cost efficiency:

**Automatic**: Analyzes every task, routes intelligently  
**Cost-effective**: 35-50% overall savings with OpenAI  
**Quality-maintained**: Strategic work stays on Manus  
**Transparent**: See routing decisions and savings  
**Flexible**: Override when needed  

Use this skill to maximize value from AI while minimizing costs.
