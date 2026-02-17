# OpenAI API Setup Guide

## Why Use OpenAI API

**Cost Efficiency**: OpenAI API costs ~$0.15 per 1M tokens vs Manus credits

**Use Cases**: Bulk processing, simple classification, data extraction, template generation

**Savings**: 90%+ on high-volume tasks while maintaining quality

## Setup Steps

### 1. Create OpenAI Account

Visit https://platform.openai.com/signup

Use existing ChatGPT credentials or create new account

### 2. Add Billing

Navigate to Settings → Billing

Add credit card

Set spending limit (recommended: $10-20/month to start)

### 3. Create API Key

Go to API Keys section

Click "Create new secret key"

Name it (e.g., "Manus Integration")

**Copy the key immediately** (only shown once)

Format: `sk-proj-...` or `sk-...`

### 4. Configure in Manus

Store API key securely

System will automatically use OpenAI for eligible tasks

Fallback to Manus if OpenAI unavailable

## Cost Estimates

### GPT-4o-mini (Recommended)

**Input**: $0.15 per 1M tokens  
**Output**: $0.60 per 1M tokens

### Typical Usage

**100 leads/day qualification**:
- ~20,000 tokens/day
- ~$0.02/day
- ~$0.60/month

**Daily market research**:
- ~50,000 tokens/day
- ~$0.05/day
- ~$1.50/month

**Content drafts (10/week)**:
- ~30,000 tokens/week
- ~$0.03/week
- ~$0.12/month

**Total typical usage**: $5-15/month

## Monitoring Costs

**Daily**: Check usage at platform.openai.com/usage

**Set Alerts**: Configure at 80% of spending limit

**Monthly Review**: Analyze cost vs Manus savings

## Troubleshooting

**"Quota exceeded"**: Add billing or increase limit

**"Invalid API key"**: Regenerate key at platform.openai.com

**"Rate limit"**: Batch requests or upgrade tier

## Security

**Never share API key** publicly or in code repositories

**Rotate keys** periodically (every 90 days recommended)

**Use environment variables** for key storage

**Monitor usage** for unauthorized access
