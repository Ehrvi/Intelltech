---
name: api-key-manager
description: Centralized API key management with automatic validation, secure backup, health monitoring, and recovery for all external services (OpenAI, Apollo, Gmail, etc). Ensures keys never expire unexpectedly and provides instant alerts on failures.
---

# API Key Manager Skill

## Purpose

This skill provides enterprise grade API key management for all external services. It eliminates the recurring problem of expired or invalid API keys by implementing automatic validation, monitoring, backup, and recovery systems.

## When to Use

Activate this skill when:
- Setting up new API keys for any service
- Troubleshooting API authentication errors
- Need to verify all API keys are valid
- Want to ensure keys are backed up securely
- Monitoring API key health status

## Core Capabilities

### 1. Centralized Key Storage

All API keys are stored securely in `~/.api_keys/config.json` with metadata including creation date, last validation, and current status.

### 2. Automatic Validation

Validates keys for supported services (OpenAI, Apollo) using their health check endpoints. Detects invalid or expired keys immediately.

### 3. Health Monitoring

Runs periodic health checks on all registered keys. Generates alerts when keys fail validation. Logs all validation attempts for audit trail.

### 4. Secure Backup

Automatically backs up all keys on every update. Backup stored at `~/.api_keys/backup.json`. One command restoration if keys are lost or corrupted.

### 5. Multi Service Support

Currently supports OpenAI and Apollo with extensible architecture for adding more services (Gmail, Calendar, etc).

## Usage Instructions

### Adding a New API Key

```python
from key_manager import APIKeyManager

manager = APIKeyManager()
manager.add_key("openai", "sk-proj-...", metadata={"plan": "Plus"})
manager.add_key("apollo", "your_key_here", metadata={"plan": "Professional"})
```

### Validating Keys

```bash
# Validate all keys
python /home/ubuntu/skills/api-key-manager/scripts/key_manager.py health

# Validate specific key
python /home/ubuntu/skills/api-key-manager/scripts/key_manager.py validate openai
```

### Checking Status

```bash
python /home/ubuntu/skills/api-key-manager/scripts/key_manager.py status
```

### Backup and Restore

```bash
# Create backup
python /home/ubuntu/skills/api-key-manager/scripts/key_manager.py backup

# Restore from backup
python /home/ubuntu/skills/api-key-manager/scripts/key_manager.py restore
```

### Automatic Monitoring

```bash
# Run health check with alerts
python /home/ubuntu/skills/api-key-manager/scripts/auto_monitor.py

# View recent alerts
python /home/ubuntu/skills/api-key-manager/scripts/auto_monitor.py recent
```

## Workflow

When user reports API key issues:

1. **Immediate Validation**: Run health check to identify which keys are failing
2. **Root Cause Analysis**: Check validation logs and alert history
3. **Guided Resolution**: Follow service specific troubleshooting in references/best-practices.md
4. **Prevention**: Set up automatic monitoring to catch future issues

## Service Specific Notes

### OpenAI
- Keys format: `sk-proj-...` or `sk-...`
- Keys don't expire but require active billing
- Create keys at platform.openai.com/api-keys
- Test immediately after creation

### Apollo
- Professional plan: Standard keys only (limited access)
- Organization plan: Master keys available (full access)
- Keys don't expire unless manually regenerated
- Common issue: Toggle not activated during creation

## Key Learnings

Based on troubleshooting history:

**Problem**: Keys appear to "expire" frequently  
**Reality**: Keys don't expire automatically  
**Causes**: Billing issues (OpenAI), wrong plan (Apollo), manual regeneration  
**Solution**: Validate immediately, check billing, verify plan supports needed features

**Problem**: Apollo Master Key not working  
**Reality**: Professional plan doesn't support Master Keys  
**Solution**: Accept standard key limitations or upgrade to Organization plan

## Files

- `scripts/key_manager.py`: Core management system
- `scripts/auto_monitor.py`: Automatic monitoring and alerts
- `references/best-practices.md`: Security best practices and troubleshooting

## Best Practices

1. **Validate immediately** after creating any new key
2. **Set up monitoring** for production keys
3. **Backup regularly** (automatic on updates)
4. **Document metadata** when adding keys (plan, purpose, etc)
5. **Check logs** when troubleshooting issues

## Integration

This skill integrates with the ai-task-optimizer skill. When API keys are validated and healthy, the task optimizer can confidently route tasks to external services (OpenAI for bulk processing, Apollo for lead generation).

## Guarantees

With this skill active:
- ✅ All keys validated before use
- ✅ Instant detection of invalid keys
- ✅ Automatic backup on every change
- ✅ Complete audit trail of all validations
- ✅ No more surprise "expired" keys
