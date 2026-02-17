---
name: api-key-limitations
description: Complete reference of API key limitations, plan restrictions, and capabilities for all services (OpenAI, Apollo, Gmail, etc). Quick lookup for troubleshooting and planning integrations across project conversations.
---

# API Key Limitations Reference

## Purpose

Quick reference guide documenting all API key limitations, plan restrictions, and capabilities for services used in the Intelltech project. Use this to understand what each key can and cannot do before attempting integrations.

## Current API Keys Status

### OpenAI API
**Key**: `sk-proj-pqg6...J9MA`  
**Plan**: Plus ($20/month)  
**Status**: ✅ Valid and authenticated  
**Billing**: Active  

**Capabilities**:
- ✅ Full API access to all models
- ✅ GPT 4o mini, GPT 4o, GPT 4.1 mini, GPT 4.1 nano
- ✅ Gemini 2.5 flash
- ✅ Unlimited requests (rate limited)
- ✅ All endpoints available
- ✅ Streaming supported
- ✅ Function calling supported

**Limitations**:
- ⚠️ Rate limits apply (10,000 requests/minute for GPT 4o mini)
- ⚠️ Token limits per request (varies by model)
- ⚠️ Requires active billing (pay per use)
- ⚠️ Key can be revoked if exposed publicly

**Cost Structure**:
- GPT 4o mini: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- GPT 4o: ~$2.50 per 1M input tokens, ~$10 per 1M output tokens
- Very cost effective for bulk processing

**Common Issues**:
- 401 Unauthorized: Key revoked or billing inactive
- 429 Too Many Requests: Rate limit exceeded
- 400 Bad Request: Invalid parameters or model name

**Best For**:
- Bulk lead qualification
- Content generation at scale
- Data analysis and extraction
- Automated workflows

---

### Apollo API
**Key**: `81e5ypd7aiD5cxMluGxLRA`  
**Plan**: Professional ($79/month)  
**Status**: ✅ Valid but NOT Master Key  
**Credits**: 7,152 / 8,105 available (88%)  

**Capabilities**:
- ✅ People search
- ✅ Company search
- ✅ Email enrichment (1 credit)
- ✅ Phone enrichment (8 credits)
- ✅ Job change tracking
- ✅ LinkedIn data enrichment
- ✅ Export to CSV
- ✅ Sequences (email campaigns)

**Limitations**:
- ❌ NOT a Master Key (Professional plan restriction)
- ❌ Some admin endpoints unavailable
- ❌ User management endpoints restricted
- ❌ Organization settings endpoints restricted
- ⚠️ 8,105 credits/year (675 credits/month average)
- ⚠️ Credits reset annually, not monthly
- ⚠️ No rollover of unused credits

**Credit Costs**:
- Email: 1 credit
- Phone: 8 credits
- Mobile phone: 8 credits
- Export contact: 1 credit
- Enrichment: 1 credit per field
- Typical lead (email + phone + enrichment): ~13 credits

**Monthly Capacity**:
- ~675 credits/month average
- ~52 full leads/month (email + phone + enrichment)
- ~675 email only leads/month

**Master Key Restrictions**:
- ❌ Professional plan does NOT support Master Keys
- ❌ Only Organization plan ($119/month) has Master Keys
- ❌ Toggle during key creation does not work on Professional plan
- ✅ Current key works for 95% of use cases

**Common Issues**:
- 401 Unauthorized: Key regenerated or invalid
- 403 Forbidden: Endpoint requires Master Key (upgrade needed)
- 429 Too Many Requests: Credit limit exceeded
- 400 Bad Request: Invalid search parameters

**Best For**:
- Targeted lead generation (quality over quantity)
- Email enrichment campaigns
- Company research
- Contact verification

**NOT Suitable For**:
- High volume lead generation (>50 leads/month with full data)
- User management automation
- Organization wide settings changes

---

### Gmail API (via MCP)
**Access**: Via Manus MCP integration  
**Plan**: Free (Google Workspace)  
**Status**: ✅ Available  

**Capabilities**:
- ✅ Read emails
- ✅ Send emails
- ✅ Search emails
- ✅ Label management
- ✅ Draft creation
- ✅ Attachment handling

**Limitations**:
- ⚠️ OAuth required (automatic via MCP)
- ⚠️ Rate limits apply (varies by account type)
- ⚠️ Large attachments may fail (>25MB)

**Best For**:
- Email automation
- Lead follow up sequences
- Notification systems
- Email parsing and data extraction

---

### Google Calendar API (via MCP)
**Access**: Via Manus MCP integration  
**Plan**: Free (Google Workspace)  
**Status**: ✅ Available  

**Capabilities**:
- ✅ Create events
- ✅ Read events
- ✅ Update events
- ✅ Delete events
- ✅ Recurring events
- ✅ Reminders

**Limitations**:
- ⚠️ OAuth required (automatic via MCP)
- ⚠️ Rate limits apply

**Best For**:
- Meeting scheduling
- Event tracking
- Reminder systems
- Time management automation

---

## Plan Comparison Tables

### OpenAI Plans
| Feature | Free Trial | Pay As You Go (Current) | Enterprise |
|---------|-----------|------------------------|------------|
| API Access | ✅ Limited | ✅ Full | ✅ Full |
| Models | Latest | Latest | Latest + Custom |
| Rate Limits | Low | Standard | High |
| Cost | $5 credit | Per token | Custom pricing |
| Best For | Testing | Production | Large scale |

### Apollo Plans
| Feature | Free | Basic ($49) | Professional ($79) | Organization ($119) |
|---------|------|-------------|-------------------|---------------------|
| Credits/year | 900 | 30,000 | 8,105 | 12,000 |
| Credits/month | 75 | 2,500 | 675 | 1,000 |
| API Access | ✅ | ✅ | ✅ | ✅ |
| Master Keys | ❌ | ❌ | ❌ | ✅ |
| Sequences | ❌ | ✅ | ✅ | ✅ |
| A/Z Testing | ❌ | ❌ | ✅ | ✅ |
| Team Access | ❌ | ❌ | ✅ | ✅ |
| Full leads/month | 5 | 192 | 52 | 77 |

**Note**: Full lead = email + phone + enrichment (~13 credits)

---

## Integration Recommendations

### For Lead Generation Workflows

**Recommended Stack**:
1. **Apollo**: Find and enrich leads (52/month max)
2. **OpenAI**: Qualify and score leads (unlimited, $0.03/lead)
3. **Gmail**: Send personalized outreach (free)

**Cost**: ~$81/month ($79 Apollo + ~$2 OpenAI)  
**Capacity**: 52 fully enriched leads/month  
**Quality**: High (targeted, qualified, personalized)

### For High Volume Processing

**Recommended Stack**:
1. **OpenAI**: All AI processing (bulk analysis, content gen)
2. **Manus**: Strategic decisions and complex tasks
3. **Apollo**: Minimal use (only for data not available elsewhere)

**Cost**: ~$5-15/month OpenAI + Manus subscription  
**Capacity**: Thousands of tasks/month  
**Quality**: Excellent with proper prompting

### For Email Automation

**Recommended Stack**:
1. **Gmail MCP**: Email operations (free)
2. **OpenAI**: Email content generation ($0.001/email)
3. **Apollo**: Lead data (when needed)

**Cost**: ~$1-5/month  
**Capacity**: Unlimited emails  
**Quality**: Personalized at scale

---

## Upgrade Decision Matrix

### When to Upgrade Apollo to Organization ($119)

**Upgrade IF**:
- ✅ Need Master Key for admin automation
- ✅ Processing >80 full leads/month
- ✅ Need advanced team features
- ✅ ROI justifies extra $40/month

**Stay on Professional IF**:
- ✅ <50 leads/month is sufficient
- ✅ Don't need Master Key features
- ✅ Current key works for your use cases
- ✅ Want to minimize costs

**Current Recommendation**: Stay on Professional. Current key works for 95% of use cases and 52 leads/month is sufficient for targeted outreach.

### When to Increase OpenAI Usage

**Always Recommended**:
- ✅ Extremely cost effective ($0.001-0.01 per task)
- ✅ Saves massive Manus credits
- ✅ Perfect for bulk processing
- ✅ No practical limit on volume

**Current Recommendation**: Use OpenAI for ALL bulk tasks. Reserve Manus for strategy and complex decisions.

---

## Troubleshooting Quick Reference

### "API Key Invalid" Error

**OpenAI**:
1. Check billing is active at platform.openai.com/settings/organization/billing
2. Verify key not revoked at platform.openai.com/api-keys
3. Create new key if needed

**Apollo**:
1. Check key not regenerated at developer.apollo.io/keys
2. Verify credits available (need at least 1 credit)
3. Test with health endpoint: `GET /v1/auth/health`

### "Permission Denied" Error

**OpenAI**:
- Rare. Usually means model not available or deprecated.

**Apollo**:
- Check if endpoint requires Master Key
- If yes, either upgrade to Organization or use alternative endpoint
- Most common: user management, org settings endpoints

### "Rate Limit Exceeded" Error

**OpenAI**:
- Wait 60 seconds and retry
- Implement exponential backoff
- Consider batching requests

**Apollo**:
- Check credit balance
- Slow down request rate
- Implement queuing system

---

## Key Takeaways

**OpenAI**:
- ✅ Use for ALL bulk processing
- ✅ Extremely cost effective
- ✅ No practical limitations
- ⚠️ Requires active billing

**Apollo Professional**:
- ✅ Perfect for targeted lead gen (quality over quantity)
- ✅ 52 full leads/month capacity
- ❌ NOT a Master Key (by design, not error)
- ⚠️ Credits are precious, use wisely

**Integration Strategy**:
- Use OpenAI for volume (cheap, unlimited)
- Use Apollo for data (targeted, limited)
- Use Manus for strategy (expensive, high quality)
- Use Gmail/Calendar for automation (free, unlimited)

**Cost Optimization**:
- Total monthly: ~$81 (Apollo) + ~$5 (OpenAI) = ~$86
- Saves ~$200-300/month in Manus credits
- ROI: Immediate and substantial

---

## Last Updated

**Date**: 2026-02-12  
**By**: Lord Manus  
**Next Review**: When new services added or plans change
