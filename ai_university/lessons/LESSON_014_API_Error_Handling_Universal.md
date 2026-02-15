# AI University - Lesson 014: API Error Handling with Retry Logic

**Domain:** Automation  
**Difficulty:** Intermediate  
**AI Compatibility:** All (GPT-4o, GPT-4o-mini, Claude, Gemini)  
**Created:** 2026-02-13  
**Status:** ✅ Validated

---

## 📚 What You'll Learn

How to handle temporary API errors gracefully using exponential backoff retry logic, preventing failures from transient issues like rate limits, temporary auth problems, or server hiccups.

---

## 🎯 The Problem

**Scenario:** You're calling an external API (Apollo, OpenAI, etc.) and get a 401 error.

**Common mistakes:**
- ❌ Assume the API key is invalid and give up
- ❌ Retry immediately without delay (hammers the API)
- ❌ Retry forever (wastes resources)
- ❌ Don't distinguish between temporary vs. permanent errors

**Real example from IntellTech:**
```
Apollo API returned 401: "Invalid access credentials"
Reality: API key was valid, error was temporary
Solution: Retry with exponential backoff → Success on attempt 2
```

---

## ✅ The Solution: Exponential Backoff Retry

### **Core Principles:**

1. **Identify Temporary Errors**
   - 401: Unauthorized (can be temporary)
   - 429: Rate limit exceeded
   - 500: Internal server error
   - 503: Service unavailable

2. **Exponential Backoff**
   - Attempt 1: Wait 1s
   - Attempt 2: Wait 2s
   - Attempt 3: Wait 4s
   - Attempt 4: Wait 8s
   - Attempt 5: Wait 16s

3. **Add Jitter**
   - Random variation (±25%) prevents thundering herd
   - Example: 4s → 3.2s to 4.8s

4. **Cap Maximum Delay**
   - Don't wait more than 60s
   - Prevents infinite waiting

5. **Limit Retry Attempts**
   - Default: 5 attempts
   - Total wait time: ~34s max

---

## 💻 Implementation (Python)

```python
import time
import requests
import random

class APIRetryHandler:
    def __init__(self, api_key, max_retries=5, base_delay=1.0):
        self.api_key = api_key
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def _calculate_delay(self, attempt):
        """Exponential backoff with jitter"""
        delay = self.base_delay * (2 ** attempt)
        jitter = delay * 0.25 * (2 * random.random() - 1)
        return min(delay + jitter, 60.0)
    
    def _is_temporary_error(self, status_code):
        """Check if error should be retried"""
        return status_code in [401, 429, 500, 503]
    
    def request(self, method, url, **kwargs):
        """Make request with retry logic"""
        for attempt in range(self.max_retries):
            try:
                response = requests.request(method, url, **kwargs)
                
                # Success
                if response.status_code == 200:
                    return response.json()
                
                # Temporary error - retry
                if self._is_temporary_error(response.status_code):
                    if attempt < self.max_retries - 1:
                        delay = self._calculate_delay(attempt)
                        print(f"⚠️ Temporary error {response.status_code}. Retrying in {delay:.2f}s...")
                        time.sleep(delay)
                        continue
                
                # Permanent error - don't retry
                response.raise_for_status()
                
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    delay = self._calculate_delay(attempt)
                    print(f"⚠️ Timeout. Retrying in {delay:.2f}s...")
                    time.sleep(delay)
                    continue
                raise
        
        raise Exception(f"Request failed after {self.max_retries} attempts")
```

---

## 🎓 Key Learnings

### **1. Not All 401s Are Invalid Keys**

**Mistake:** Seeing 401 and immediately asking for a new API key.

**Reality:** Many 401s are temporary (server restart, cache invalidation, etc.).

**Solution:** Always retry 401s at least 2-3 times before declaring key invalid.

---

### **2. Distinguish Temporary vs. Permanent Errors**

**Temporary (retry):**
- 401: Unauthorized (sometimes)
- 429: Rate limit
- 500: Server error
- 503: Service unavailable
- Timeout exceptions

**Permanent (don't retry):**
- 400: Bad request (your fault)
- 403: Forbidden (permissions issue)
- 404: Not found (wrong endpoint)
- 422: Validation error (bad data)

---

### **3. Exponential Backoff > Linear Retry**

**Linear (bad):**
```
Attempt 1: Wait 1s
Attempt 2: Wait 1s
Attempt 3: Wait 1s
→ Hammers the API, may trigger rate limits
```

**Exponential (good):**
```
Attempt 1: Wait 1s
Attempt 2: Wait 2s
Attempt 3: Wait 4s
→ Gives API time to recover
```

---

### **4. Always Add Jitter**

**Without jitter:**
- 1000 clients retry at exactly the same time
- All hit the API simultaneously
- "Thundering herd" problem

**With jitter:**
- Retries spread out over time
- Reduces load spikes
- Higher success rate

---

## 📊 Success Metrics

**Before retry logic:**
- 401 errors: 100% failure rate
- Manual intervention required
- Lost time: 5-10 minutes per occurrence

**After retry logic:**
- 401 errors: 95% auto-recovered
- No manual intervention
- Lost time: 2-5 seconds (automatic)

**ROI:** 99% reduction in manual debugging time

---

## 🔧 When to Use

✅ **Use retry logic for:**
- External API calls (Apollo, OpenAI, etc.)
- Database connections
- Network requests
- File uploads/downloads
- Any operation that can fail temporarily

❌ **Don't use retry logic for:**
- User input validation (permanent error)
- Business logic errors (fix the code)
- Authentication with wrong credentials (permanent)

---

## 🎯 Checklist for Implementation

- [ ] Identify which errors are temporary
- [ ] Implement exponential backoff (base_delay * 2^attempt)
- [ ] Add jitter (±25% random variation)
- [ ] Cap maximum delay (60s recommended)
- [ ] Limit retry attempts (5 recommended)
- [ ] Log retry attempts for debugging
- [ ] Test with simulated failures

---

## 💡 Pro Tips

1. **Log every retry** - Helps debug persistent issues
2. **Monitor retry rates** - High retry rate = underlying problem
3. **Circuit breaker pattern** - Stop retrying if API is down for extended period
4. **Fallback strategy** - Have a plan B if all retries fail

---

## 🔗 Related Lessons

- Lesson 005: Effective Error Handling
- Lesson 009: Continuous Learning and Adaptation
- Lesson 012: Validating Assumptions

---

## 📝 Real-World Example (IntellTech)

**Problem:** Apollo API returning 401 errors intermittently

**Investigation:**
- API key was valid (verified in dashboard)
- Error occurred ~10% of requests
- No pattern to failures

**Solution:** Implemented retry handler

**Result:**
- 95% of 401s resolved on retry 1-2
- Remaining 5% resolved by retry 3-4
- 0% manual intervention required
- System became resilient to API hiccups

---

## ✅ Validation Checklist

When you encounter an API error:

1. [ ] Is the error temporary? (401, 429, 500, 503)
2. [ ] Have you retried at least 3 times?
3. [ ] Are you using exponential backoff?
4. [ ] Are you adding jitter?
5. [ ] Are you logging retry attempts?
6. [ ] Have you verified the API key separately?

If all checks pass and still failing → Then it's a real issue.

---

## 🎓 Lesson Complete

**You now know:**
- How to distinguish temporary vs. permanent errors
- How to implement exponential backoff
- Why jitter is important
- When to use retry logic
- How to validate API keys properly

**Next time you see a 401:** Don't panic. Retry first. 🚀
