# 🔐 AKIRA SASE - SECURITY POLICY

## 🛡️ Security Overview

Akira SASE implements multiple layers of security to ensure safe and authorized cybersecurity operations.

## 🔑 Authentication & Authorization

### JWT Authentication
- **Access Tokens**: Short-lived (30 minutes default)
- **Refresh Tokens**: Long-lived (7 days default)
- **Algorithm**: HS256 (configurable)
- **Token Revocation**: Supported via blacklist

### API Keys
- Alternative authentication method
- Format: `ak_[32-byte-urlsafe-token]`
- User-specific and revocable

### User Permissions
Users have scoped permissions:
- `scan:read` - View scan results
- `scan:write` - Execute scans
- `admin:all` - Full administrative access

## 🚦 Rate Limiting

### General Limits
- **60 requests/minute** per user/IP
- **1000 requests/hour** per user/IP

### Scan-Specific Limits
- **10 scans/hour** maximum
- Prevents abuse and resource exhaustion

### Headers
Rate limit info returned in response headers:
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`

## 🎯 Target Authorization

### Whitelisting System
- **Required by default** in production
- Configure via `WHITELISTED_TARGETS` env variable
- Supports:
  - Individual IPs: `192.168.1.100`
  - CIDR ranges: `192.168.1.0/24`
  - Wildcards: `*.example.com`

### Automatic Blocks

#### Critical Infrastructure (ALWAYS BLOCKED)
- Government domains: `*.gov`, `*.mil`
- Public DNS: `8.8.8.8`, `1.1.1.1`, etc.
- Emergency services

#### Major Public Services (BLOCKED by default)
- google.com, facebook.com, amazon.com
- microsoft.com, apple.com, netflix.com
- All major cloud providers (AWS, Azure, GCP)

### Private Networks
- Automatically allowed: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`
- No authorization required for internal testing

## 🔒 Secrets Management

### Environment Variables
**NEVER commit `.env` or credentials to version control!**

Required secrets:
```bash
OPENAI_API_KEY=sk-proj-xxxxx
JWT_SECRET_KEY=64+ character random string
API_SECRET_KEY=32+ character random string
FIREBASE_PROJECT_ID=your-project-id
```

### Generating Secure Keys
```bash
# JWT Secret (64 chars)
python -c "import secrets; print(secrets.token_urlsafe(48))"

# API Secret (32 chars)
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 📝 Logging & Auditing

### Security Events Logged
- Authentication attempts (success/failure)
- Rate limit violations
- Unauthorized target access attempts
- Admin actions
- Token revocations

### Log Levels
- `INFO`: Normal operations
- `WARNING`: Rate limits, minor security events
- `ERROR`: Operation failures
- `CRITICAL`: Security violations, critical infrastructure blocks

### Firebase Integration
Critical security events are saved to Firebase for:
- Long-term audit trail
- Incident investigation
- Compliance reporting

## 🚨 Security Alerts

### Monitored Events
1. **Multiple failed authentications** - Potential brute force
2. **Critical infrastructure targeting** - Serious violation
3. **Rate limit violations** - Resource abuse
4. **Unauthorized target attempts** - Policy violation

### Response Actions
- Log event with full context
- Block/throttle offending user/IP
- Alert administrators (if configured)
- Revoke compromised tokens

## 🔐 CORS Policy

### Production Settings
```python
CORS_ORIGINS=https://your-frontend.com
CORS_ALLOW_CREDENTIALS=true
CORS_MAX_AGE=600
```

### Development Settings
```python
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Never use `*` in production!**

## 🐳 Docker Security

### Best Practices Implemented
- ✅ Non-root user (uid 1000)
- ✅ Read-only root filesystem (where possible)
- ✅ No new privileges
- ✅ Secrets via environment variables
- ✅ Health checks
- ✅ Resource limits

### Running Securely
```bash
docker run -d \
  --name akira \
  --read-only \
  --security-opt=no-new-privileges \
  --cap-drop=ALL \
  -p 8000:8000 \
  --env-file .env \
  akira:latest
```

## 📋 Compliance & Legal

### Ethical Use Policy
Akira is designed **EXCLUSIVELY** for:
- ✅ Authorized penetration testing
- ✅ Internal security audits
- ✅ Cybersecurity research with permission
- ✅ Educational purposes on owned systems
- ✅ Bug bounty programs with authorization

### PROHIBITED Uses
- ❌ Unauthorized system scanning/attacking
- ❌ Targeting critical infrastructure
- ❌ Violating terms of service
- ❌ Any illegal activities
- ❌ Harassment or malicious intent

### Legal Disclaimer
Users are **100% responsible** for:
- Obtaining proper authorization
- Complying with local/international laws
- Respecting system owner rights
- Maintaining proper documentation

## 🔍 Vulnerability Reporting

### Reporting Security Issues
If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email: security@akira-cyber.com
3. Include:
   - Vulnerability description
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline
- **Acknowledgment**: Within 48 hours
- **Assessment**: Within 7 days
- **Fix**: Based on severity (Critical: 24-72h, High: 1 week, etc.)
- **Disclosure**: Coordinated after fix deployment

## 🛠️ Security Checklist

### Before Deployment
- [ ] All secrets in environment variables
- [ ] `.env` and credentials NOT in repository
- [ ] JWT secrets are 64+ characters
- [ ] CORS origins properly configured
- [ ] Whitelisted targets configured
- [ ] Rate limiting enabled
- [ ] HTTPS enforced (production)
- [ ] Firewall rules configured
- [ ] Monitoring/alerts set up
- [ ] Backup strategy in place

### Regular Maintenance
- [ ] Rotate secrets every 90 days
- [ ] Review audit logs weekly
- [ ] Update dependencies monthly
- [ ] Review whitelist quarterly
- [ ] Test backup restoration
- [ ] Security scan with tools (OWASP ZAP, etc.)

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Penetration Testing Execution Standard](http://www.pentest-standard.org/)

---

**Last Updated**: 2025-01-01
**Version**: 2.0.0
**Maintained By**: Akira Security Team
