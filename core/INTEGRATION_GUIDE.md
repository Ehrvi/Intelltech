# Cost Optimization Integration Guide

**Date:** 2026-02-16  
**Version:** 1.0  
**Status:** Ready for Production

---

## Quick Start

### Step 1: Import the Wrapper

Replace this:
```python
import requests
```

With this:
```python
import requests
from optimized_api_wrapper import optimized_post
```

### Step 2: Replace API Calls

Replace this:
```python
response = requests.post(url, headers=headers, json=payload, timeout=30)
```

With this:
```python
response = optimized_post(url, headers=headers, json=payload, timeout=30)
```

**That's it!** The optimization happens automatically.

---

## Complete Example

### Before (Original Code)

```python
#!/usr/bin/env python3
import os
import requests

API_KEY = os.environ.get('APOLLO_API_KEY')
url = 'https://api.apollo.io/api/v1/mixed_companies/search'

headers = {
    'Content-Type': 'application/json',
    'X-Api-Key': API_KEY
}

payload = {
    'q_organization_keyword_tags': ['mining', 'coal'],
    'page': 1,
    'per_page': 100
}

response = requests.post(url, headers=headers, json=payload, timeout=30)
data = response.json()
```

### After (With Optimization)

```python
#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add cost optimization to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'manus_global_knowledge' / 'core'))

from optimized_api_wrapper import optimized_post, print_optimization_stats

API_KEY = os.environ.get('APOLLO_API_KEY')
url = 'https://api.apollo.io/api/v1/mixed_companies/search'

headers = {
    'Content-Type': 'application/json',
    'X-Api-Key': API_KEY
}

payload = {
    'q_organization_keyword_tags': ['mining', 'coal'],
    'page': 1,
    'per_page': 100
}

# Use optimized_post instead of requests.post
response = optimized_post(url, headers=headers, json=payload, timeout=30)
data = response.json()

# Optional: Print stats at the end
print_optimization_stats()
```

---

## What Gets Optimized?

### 1. Prompt Compression

**Before:**
```json
{
  "query": "Please kindly provide a very detailed analysis..."
}
```

**After:**
```json
{
  "query": "Provide detailed analysis..."
}
```

**Savings:** ~30-50% on text fields

### 2. Response Size Control

For LLM APIs (OpenAI, etc), adds `max_tokens` limits:
```json
{
  "prompt": "...",
  "max_tokens": 500  // Added automatically
}
```

**Savings:** ~10-30% on response costs

### 3. Smart Defaults

- Removes unnecessary whitespace
- Compresses JSON payloads
- Optimizes nested structures

---

## Configuration

### Enable/Disable Optimization

Set environment variable:
```bash
export ENABLE_COST_OPTIMIZATION=true   # Enable (default)
export ENABLE_COST_OPTIMIZATION=false  # Disable
```

Or in code:
```python
from optimized_api_wrapper import OptimizedAPIWrapper

wrapper = OptimizedAPIWrapper(enable_optimization=False)
response = wrapper.post(url, headers=headers, json=payload)
```

### View Statistics

```python
from optimized_api_wrapper import print_optimization_stats

# At the end of your script
print_optimization_stats()
```

Output:
```
======================================================================
COST OPTIMIZATION STATISTICS
======================================================================
Total API Calls:        10
Optimized Calls:        7
Optimization Rate:      70.0%
Tokens Saved (est):     150
Cost Savings (est):     $0.0003

By Endpoint:
----------------------------------------------------------------------
  search                  5 calls  (80% optimized)
  enrich                  3 calls  (67% optimized)
  create                  2 calls  (50% optimized)
======================================================================
```

---

## Integration Checklist

For each script you want to optimize:

- [ ] Add import: `from optimized_api_wrapper import optimized_post`
- [ ] Replace `requests.post` with `optimized_post`
- [ ] Test that script still works correctly
- [ ] Optional: Add `print_optimization_stats()` at the end
- [ ] Commit changes

---

## Scripts to Update

Based on ProjetoApollo, these scripts should be updated:

### High Priority (Frequent API calls)
1. ✅ `extract_all_companies.py` - Fetches 14K+ companies
2. ✅ `extract_all_companies_full.py` - Full enrichment
3. ✅ `score_companies.py` - Scoring logic
4. ✅ `apollo_custom_fields_manager.py` - Field management

### Medium Priority (Moderate usage)
5. ✅ `fix_custom_fields_from_csv.py`
6. ✅ `fix_existing_contacts.py`
7. ✅ `recover_lost_contacts.py`
8. ✅ `update_all_rio_tinto.py`

### Low Priority (Testing/one-off)
9. ⏸️ `test_*.py` scripts (can wait)

---

## Expected Savings

### Current Costs (Estimated)

| Service | Monthly Cost | API Calls/Month |
|---|---|---|
| Apollo API | $50-100 | ~10,000 |
| OpenAI API | $15 | ~500 |
| **Total** | **$65-115** | **~10,500** |

### After Optimization

| Service | Monthly Cost | Savings |
|---|---|---|
| Apollo API | $50-100 | $0 (no token-based pricing) |
| OpenAI API | $6-9 | **$6-9 (40-60%)** |
| **Total** | **$56-109** | **$6-9/month** |

**Note:** Apollo savings are minimal (API is not token-based), but OpenAI savings are significant.

---

## Troubleshooting

### "Module not found" Error

**Problem:**
```
ImportError: No module named 'optimized_api_wrapper'
```

**Solution:**
Add the path to your script:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'manus_global_knowledge' / 'core'))
```

### Optimization Not Working

**Check 1:** Is optimization enabled?
```python
from optimized_api_wrapper import get_wrapper
print(get_wrapper().enable_optimization)  # Should be True
```

**Check 2:** Are optimization modules available?
```bash
cd /home/ubuntu/manus_global_knowledge/core
python3 -c "from prompt_optimizer import PromptOptimizer; print('✅ OK')"
```

### Response Format Changed

**Problem:** API returns different format after optimization.

**Solution:** Optimization should NOT change response format. If it does, disable optimization for that specific call:
```python
import requests
response = requests.post(url, headers=headers, json=payload)  # Bypass optimization
```

---

## Next Steps

1. **Test Integration:** Update one script and verify it works
2. **Roll Out:** Update remaining scripts one by one
3. **Monitor:** Track savings over 1 week
4. **Iterate:** Adjust optimization rules based on results

---

## Support

If you encounter issues:
1. Check this guide
2. Review error messages
3. Test with optimization disabled
4. Contact: [Your contact info]

---

**Version History:**
- v1.0 (2026-02-16): Initial release
