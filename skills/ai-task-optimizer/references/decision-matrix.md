# Decision Matrix for Task Routing

## Scoring System

Each task receives a score from 4 to 12 based on four dimensions:

### 1. Complexity (1 to 3)

**Simple (1)**: Binary classification, data extraction, template responses, simple calculations

**Moderate (2)**: Multi-category classification, pattern recognition, basic analysis, summarization

**Complex (3)**: Strategic decisions, creative problem solving, multi-step reasoning, custom solutions

### 2. Volume (1 to 3)

**Low (1)**: 1 to 10 items, one-off tasks, ad-hoc requests

**Medium (2)**: 11 to 100 items, daily/weekly batches, recurring workflows

**High (3)**: 100+ items, continuous processing, large-scale operations

### 3. Quality Sensitivity (1 to 3)

**Low (1)**: Internal use, preliminary screening, quick validation

**Medium (2)**: Team collaboration, decision support, client-facing (reviewed)

**High (3)**: Direct client delivery, strategic decisions, legal/compliance, brand reputation

### 4. Time Sensitivity (1 to 3)

**Low (1)**: Days to weeks, background processing, scheduled tasks

**Medium (2)**: Hours to days, business day response, standard workflows

**High (3)**: Minutes to hours, real-time processing, urgent requests

## Routing Rules

**Total Score = Complexity + Volume + Quality Sensitivity + Time Sensitivity**

### OpenAI Territory (Score 4 to 7)

High volume with low to medium complexity. Low to medium quality sensitivity.

**Examples:**
- Lead qualification (hundreds of leads)
- Email template generation
- Data extraction from lists
- Simple translations
- Meeting notes summarization

**Cost:** ~$0.15 per 1M input tokens  
**Savings:** 90%+ vs Manus

### Borderline Zone (Score 8)

Medium complexity, medium volume. Consider hybrid approach or OpenAI with review.

**Examples:**
- Company research reports (batch)
- Market analysis (routine)
- Content drafts
- Competitive intelligence

**Strategy:** OpenAI for bulk work, Manus for review if needed  
**Savings:** 60-70%

### Manus Territory (Score 9 to 12)

High complexity OR high quality sensitivity. Strategic value.

**Examples:**
- Client proposals
- Strategic plans
- Executive presentations
- Technical specifications
- Custom solutions

**Cost:** Manus credits (appropriate for value)  
**Savings:** None, but quality maximized

## Override Rules

These rules override score-based routing:

**Always Manus:**
- Quality sensitivity = 3 (client-facing, high stakes)
- Complexity = 3 (strategic, creative)

**Prefer OpenAI:**
- Volume = 3 AND complexity = 1 (bulk simple tasks)
- Explicit "draft" or "quick" in request

## Common Task Mappings

| Task Type | Typical Score | Provider | Rationale |
|-----------|--------------|----------|-----------|
| Lead qualification | 7 | OpenAI | High volume, simple logic |
| Lead search | 6 | OpenAI | Data extraction, bulk |
| Company research | 8 | OpenAI/Hybrid | Medium complexity, batch |
| Pitch writing | 9 | Manus | High quality, strategic |
| Email templates | 8 | OpenAI | Medium complexity, volume |
| Data extraction | 6 | OpenAI | Simple, high volume |
| Strategic analysis | 11 | Manus | Complex, high quality |
| Report generation | 9 | Manus | High quality output |

## Cost Optimization Tactics

**Batch Processing**: Combine similar tasks to reduce API overhead (40% savings)

**Prompt Engineering**: Concise prompts save 20-30% tokens

**Caching**: Cache common responses (company research, industry analysis) for 30-50% savings

**Progressive Enhancement**: Start with OpenAI classification, escalate only top 10-20% to Manus (80% savings)

## Quality Assurance

**OpenAI Tasks**: 95%+ accuracy target, 10% sample review by Manus

**Manus Tasks**: 98%+ accuracy target, full strategic review

**Hybrid Tasks**: OpenAI speed + Manus quality, cost-effective excellence
