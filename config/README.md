# ⚙️ Akira SASE - Configuration

This directory contains configuration files and templates.

## 📋 Configuration Files

### Environment Configuration
- **.env.example** - Environment variables template
  ```bash
  # Copy to project root and configure
  cp config/.env.example ../.env
  nano ../.env
  ```

  Required variables:
  - `OPENAI_API_KEY` - OpenAI API key
  - `FIREBASE_PROJECT_ID` - Firebase project ID
  - `JWT_SECRET_KEY` - JWT signing key (64+ chars)
  - `API_SECRET_KEY` - API secret key (32+ chars)

### Firebase Configuration
- **firebase-credentials.example.json** - Firebase credentials template
  ```bash
  # Download actual credentials from Firebase Console
  # Save as ../firebase-credentials.json (project root)
  ```

### Docker Configuration
- **Dockerfile** - Container image definition
- **docker-compose.yml** - Multi-container orchestration (if exists)

## 🔐 Security Best Practices

### DO:
✅ Copy `.env.example` to `.env` in project root
✅ Fill in actual values in `.env`
✅ Generate secure random keys
✅ Use different secrets for each environment
✅ Keep credentials out of version control

### DON'T:
❌ Commit `.env` file to git
❌ Share credentials in chat/email
❌ Use default/example values in production
❌ Commit `firebase-credentials.json`

## 🔑 Generating Secure Keys

```bash
# JWT Secret (64+ characters)
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(48))"

# API Secret (32+ characters)
python -c "import secrets; print('API_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

## 📦 Docker Usage

```bash
# Build image
docker build -f config/Dockerfile -t akira:latest .

# Run container
docker run -d \
  --name akira \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/firebase-credentials.json:/app/firebase-credentials.json:ro \
  akira:latest
```

## 🔗 References

- Environment variables: [`docs/DEPLOYMENT.md`](../docs/DEPLOYMENT.md)
- Security policies: [`docs/SECURITY.md`](../docs/SECURITY.md)
- Setup guide: [`scripts/setup.py`](../scripts/setup.py)

---

**Last Updated**: 2025-01-01
**⚠️ NEVER commit actual credentials to version control!**
