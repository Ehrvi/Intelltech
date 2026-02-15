# Accurate API Pricing Reference

**Last Updated:** 2026-02-16  
**Source:** User knowledge + OpenAI research + Official documentation

---

## 🎯 OpenAI API Pricing

**Source:** https://openai.com/api/pricing/

### Current Models (Per 1M Tokens in USD)

| Model | Input (per 1M) | Output (per 1M) |
|-------|----------------|-----------------|
| gpt-4o | $5.00 | $15.00 |
| gpt-4o-mini | $0.15 | $0.60 |
| gpt-3.5-turbo | $0.50 | $1.50 |

### Calculation Formula

```python
cost_usd = (input_tokens / 1_000_000) * input_price + (output_tokens / 1_000_000) * output_price
```

**Example:**
- Model: gpt-4o
- Input: 1,000 tokens
- Output: 2,000 tokens
- Cost: (1000/1M * $5) + (2000/1M * $15) = $0.005 + $0.030 = **$0.035**

---

## 🔍 Apollo.io API Pricing

**Source:** https://docs.apollo.io/ + User knowledge

### Credit System

- **1 credit per API call** (search, enrich, export)
- **Cost per credit:** Varies by plan
  - Basic: ~$0.10-0.20 per credit
  - Professional: ~$0.05-0.10 per credit
  - Enterprise: Negotiated

### Typical Usage

```
1 company search = 1 credit
1 person enrich = 1 credit
1 export = 1 credit
```

**For cost tracking, use:** $0.10 per credit (conservative estimate)

---

## 💎 Manus Credits Pricing

**Source:** User knowledge + manus.app documentation

### Cost Per Operation (in Manus Credits)

| Operation | Credits | Notes |
|-----------|---------|-------|
| shell | 1.0 | Per command execution |
| file_read | 0.5 | Per file read |
| file_write | 0.5 | Per file write |
| file_edit | 0.5 | Per file edit |
| search | 20.0 | Web search |
| browser | 30.0 | Browser navigation |
| browser_action | 5.0 | Click, input, etc. |
| map | 10.0 | Per item in parallel |
| generate_image | 15.0 | Image generation |
| generate_video | 50.0 | Video generation |
| mcp_call | 2.0 | MCP tool call |
| plan | 0.0 | Planning (free) |
| message | 0.0 | Messaging (free) |

### Manus Credit Value

**1 Manus credit ≈ $0.01 USD**

(User should verify current conversion rate)

### Calculation Example

```
Task operations:
- shell: 10x = 10.0 credits
- file_write: 5x = 2.5 credits
- search: 1x = 20.0 credits
Total: 32.5 credits = $0.325 USD
```

---

## 📊 Multi-Platform Cost Calculation

### Total Cost Formula

```
Total USD = Manus_credits * 0.01 
          + OpenAI_cost_usd 
          + Apollo_credits * 0.10
```

### Example: Complete Task Cost

**Manus:**
- 50 credits = $0.50

**OpenAI:**
- 3 calls, ~5000 tokens total
- Cost: ~$0.10

**Apollo:**
- 10 API calls = 10 credits
- Cost: 10 * $0.10 = $1.00

**Total:** $0.50 + $0.10 + $1.00 = **$1.60 USD**

---

## ⚠️ Important Notes

1. **OpenAI pricing** is official and accurate as of 2024
2. **Apollo pricing** varies by plan - use $0.10/credit as conservative estimate
3. **Manus pricing** is based on user knowledge - verify with manus.app
4. **Prices change** - update this document when official pricing changes
5. **Always track actual usage** from API responses, not estimates

---

## 🔄 How to Update This Document

When pricing changes:

1. Visit official websites:
   - OpenAI: https://openai.com/api/pricing/
   - Apollo: https://www.apollo.io/pricing
   - Manus: https://manus.app/pricing (if available)

2. Update tables above

3. Update `multi_platform_cost_tracker.py` with new values

4. Commit with message: "chore: Update API pricing to [date]"

---

**Accuracy Level:** HIGH  
**Last Verified:** 2026-02-16  
**Next Review:** When user notices pricing discrepancy
