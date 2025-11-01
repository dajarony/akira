# 🚀 AKIRA SASE - DEPLOYMENT GUIDE

## 📋 Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+ recommended) or Docker
- **Python**: 3.11+
- **Memory**: 2GB minimum, 4GB recommended
- **Disk**: 10GB minimum
- **Network**: Outbound HTTPS (443) for APIs

### Required Services
- **OpenAI API** account with API key
- **Firebase** project with Firestore enabled
- **Domain** (for production deployment)
- **SSL Certificate** (Let's Encrypt recommended)

---

## 🔧 Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/dajarony/akira.git
cd akira
```

### 2. Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy example file
cp .env.example .env

# Edit with your actual values
nano .env
```

**Required values**:
```bash
# Generate secure keys
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(48))"
python -c "import secrets; print('API_SECRET_KEY=' + secrets.token_urlsafe(32))"

# Add your credentials
OPENAI_API_KEY=sk-proj-your-key-here
FIREBASE_PROJECT_ID=your-project-id
```

### 5. Firebase Credentials
```bash
# Copy example
cp firebase-credentials.example.json firebase-credentials.json

# Add your actual Firebase service account JSON
nano firebase-credentials.json
```

### 6. Run Development Server
```bash
python main.py
```

Access at: http://localhost:8000/docs

---

## 🐳 Docker Deployment

### 1. Build Image
```bash
docker build -t akira-sase:latest .
```

### 2. Run Container
```bash
docker run -d \
  --name akira \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/firebase-credentials.json:/app/firebase-credentials.json:ro \
  -v $(pwd)/logs:/app/logs \
  --read-only \
  --tmpfs /tmp \
  --security-opt=no-new-privileges \
  --cap-drop=ALL \
  --memory=2g \
  --cpus=2 \
  akira-sase:latest
```

### 3. Check Health
```bash
curl http://localhost:8000/ping
curl http://localhost:8000/status/health
```

---

## ☸️ Kubernetes Deployment

### 1. Create Namespace
```bash
kubectl create namespace akira-sase
```

### 2. Create Secrets
```bash
# Create secret for environment variables
kubectl create secret generic akira-env \
  --from-env-file=.env \
  -n akira-sase

# Create secret for Firebase credentials
kubectl create secret generic firebase-creds \
  --from-file=firebase-credentials.json \
  -n akira-sase
```

### 3. Apply Kubernetes Manifests
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: akira-sase
  namespace: akira-sase
spec:
  replicas: 3
  selector:
    matchLabels:
      app: akira-sase
  template:
    metadata:
      labels:
        app: akira-sase
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: akira
        image: ghcr.io/dajarony/akira:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          protocol: TCP
        envFrom:
        - secretRef:
            name: akira-env
        volumeMounts:
        - name: firebase-creds
          mountPath: /app/firebase-credentials.json
          subPath: firebase-credentials.json
          readOnly: true
        - name: logs
          mountPath: /app/logs
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /ping
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /status/health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          capabilities:
            drop:
            - ALL
      volumes:
      - name: firebase-creds
        secret:
          secretName: firebase-creds
      - name: logs
        emptyDir: {}

---
apiVersion: v1
kind: Service
metadata:
  name: akira-sase
  namespace: akira-sase
spec:
  selector:
    app: akira-sase
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  type: ClusterIP

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: akira-sase
  namespace: akira-sase
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - akira.yourdomain.com
    secretName: akira-tls
  rules:
  - host: akira.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: akira-sase
            port:
              number: 80
```

```bash
kubectl apply -f deployment.yaml
```

---

## 🔒 Production Security Checklist

### Before Going Live

#### 1. Environment Variables
- [ ] All secrets generated with cryptographically secure random
- [ ] `.env` file NOT in repository
- [ ] Secrets stored in secure secret manager (Kubernetes Secrets, AWS Secrets Manager, etc.)
- [ ] Different secrets for each environment (dev/staging/prod)

#### 2. Authentication & Authorization
- [ ] JWT secrets are 64+ characters
- [ ] API keys follow format `ak_[32-chars]`
- [ ] Default admin account disabled or password changed
- [ ] User permissions properly scoped

#### 3. Rate Limiting
- [ ] Rate limiting enabled (`RATE_LIMIT_ENABLED=true`)
- [ ] Scan limits appropriate for your use case
- [ ] Rate limit headers exposed to clients

#### 4. Target Authorization
- [ ] Whitelist configured with authorized targets only
- [ ] `REQUIRE_TARGET_AUTHORIZATION=true`
- [ ] `STRICT_SECURITY_MODE=true`
- [ ] Critical infrastructure blocks tested

#### 5. CORS Configuration
- [ ] `CORS_ORIGINS` set to your specific domains only
- [ ] NO wildcard (`*`) allowed
- [ ] HTTPS URLs only

#### 6. SSL/TLS
- [ ] Valid SSL certificate installed
- [ ] HTTPS enforced (HTTP redirects to HTTPS)
- [ ] TLS 1.2+ only
- [ ] Strong cipher suites configured

#### 7. Firewall & Network
- [ ] Only port 443 (HTTPS) exposed publicly
- [ ] Internal services on private network
- [ ] DDoS protection enabled (Cloudflare, AWS Shield, etc.)
- [ ] Fail2ban or equivalent configured

#### 8. Monitoring & Logging
- [ ] Centralized logging configured
- [ ] Log rotation enabled
- [ ] Security alerts configured
- [ ] Uptime monitoring (UptimeRobot, Pingdom, etc.)
- [ ] Error tracking (Sentry, etc.)

#### 9. Backup & Recovery
- [ ] Firebase data backed up regularly
- [ ] Configuration backed up
- [ ] Disaster recovery plan documented
- [ ] Recovery tested

#### 10. Compliance
- [ ] Terms of service displayed
- [ ] Privacy policy published
- [ ] Audit logs retained
- [ ] GDPR/compliance requirements met (if applicable)

---

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# Basic health
curl https://yourdomain.com/ping

# Detailed health
curl https://yourdomain.com/status/health

# System info (requires auth)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://yourdomain.com/status/system-info
```

### Log Monitoring
```bash
# Docker
docker logs -f akira --tail 100

# Kubernetes
kubectl logs -f deployment/akira-sase -n akira-sase

# File
tail -f logs/akira.log
```

### Metrics
- **Request rate**: Monitor via `/status/stats`
- **Error rate**: Check logs for ERROR/CRITICAL
- **Response time**: Monitor via middleware
- **Resource usage**: CPU, memory, disk

### Alerts
Set up alerts for:
- **High error rate** (>5% of requests)
- **Rate limit violations** (potential abuse)
- **Failed authentications** (potential brute force)
- **Critical infrastructure attempts** (serious violation)
- **Resource exhaustion** (CPU/memory >80%)

---

## 🔄 Updates & Rollback

### Update Process
```bash
# 1. Pull latest changes
git pull origin main

# 2. Review changes
git log --oneline -10

# 3. Backup current state
docker commit akira akira-backup:$(date +%Y%m%d)

# 4. Deploy new version
docker-compose down
docker-compose pull
docker-compose up -d

# 5. Verify health
curl http://localhost:8000/ping
```

### Rollback
```bash
# Docker
docker stop akira
docker run -d --name akira akira-backup:YYYYMMDD

# Kubernetes
kubectl rollout undo deployment/akira-sase -n akira-sase

# Verify
kubectl rollout status deployment/akira-sase -n akira-sase
```

---

## 🆘 Troubleshooting

### Common Issues

#### 1. Authentication Fails
```bash
# Check JWT secret is set
grep JWT_SECRET_KEY .env

# Verify token format
echo "YOUR_TOKEN" | base64 -d
```

#### 2. Rate Limit Errors
```bash
# Check current limits
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://yourdomain.com/status/rate-limit-info

# Increase limits in .env
RATE_LIMIT_PER_MINUTE=120
RATE_LIMIT_PER_HOUR=2000
```

#### 3. Firebase Connection Issues
```bash
# Verify credentials file exists
ls -la firebase-credentials.json

# Check Firebase project ID
grep FIREBASE_PROJECT_ID .env

# Test connection
python -c "import firebase_admin; print('OK')"
```

#### 4. OpenAI API Errors
```bash
# Verify API key format
grep OPENAI_API_KEY .env | cut -c1-20

# Test API connection
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_OPENAI_KEY"
```

---

## 📞 Support

- **Documentation**: https://docs.akira-cyber.com
- **Issues**: https://github.com/dajarony/akira/issues
- **Security**: security@akira-cyber.com
- **General**: support@akira-cyber.com

---

**Last Updated**: 2025-01-01
**Version**: 2.0.0
