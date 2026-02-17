# API Key Management Best Practices

## Security Principles

### 1. Never Hardcode Keys
- Store keys in environment variables or secure config files
- Use `.env` files with `.gitignore`
- Never commit keys to version control

### 2. Rotate Keys Regularly
- Change keys every 90 days minimum
- Immediately rotate if compromised
- Keep backup of old keys during transition

### 3. Limit Key Permissions
- Use minimum required permissions
- Create separate keys for different purposes
- Prefer service-specific keys over master keys when possible

### 4. Monitor Key Usage
- Track all API calls
- Set up alerts for unusual activity
- Log all validation attempts

## Supported Services

### OpenAI
- **Endpoint**: https://api.openai.com/v1
- **Auth**: Bearer token
- **Validation**: GET /v1/models
- **Key format**: sk-proj-... or sk-...
- **Expiration**: Keys don't expire but can be revoked

### Apollo
- **Endpoint**: https://api.apollo.io/v1
- **Auth**: X-Api-Key header
- **Validation**: GET /v1/auth/health
- **Key format**: alphanumeric string
- **Master Key**: Only available in Organization plan ($119/month)
- **Expiration**: Keys don't expire unless manually regenerated

## Common Issues

### OpenAI Key Invalid
**Symptoms**: 401 Unauthorized
**Causes**:
- Key was revoked
- Billing not active
- Wrong key format

**Solution**:
1. Verify billing is active
2. Create new key at platform.openai.com/api-keys
3. Test immediately after creation

### Apollo Key Not Master
**Symptoms**: Some endpoints return 401
**Causes**:
- Professional plan doesn't support Master Keys
- Toggle not activated during creation
- Wrong account permissions

**Solution**:
- Upgrade to Organization plan for Master Keys
- OR accept limited access with Professional plan
- Verify account owner status

## Backup Strategy

### Automatic Backups
- Backup created on every key update
- Stored at `~/.api_keys/backup.json`
- Includes all keys and metadata

### Manual Backup
```bash
python key_manager.py backup
```

### Restore from Backup
```bash
python key_manager.py restore
```

## Monitoring Schedule

### Daily
- Automatic health check
- Alert on any failures
- Log all validations

### Weekly
- Review validation logs
- Check for unusual patterns
- Verify backup integrity

### Monthly
- Rotate keys if needed
- Review access permissions
- Update documentation
