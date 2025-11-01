# 🛡️⚔️ Akira SASE Cyberwar Platform

**Professional-Grade Hybrid Cybersecurity Platform** | **SUME + STDG Architecture** | **v2.0.0**

[![Security Rating](https://img.shields.io/badge/security-A+-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)]()
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)]()
[![Code Quality](https://img.shields.io/badge/code%20quality-A-brightgreen)]()

> **⚠️ ETHICAL USE ONLY**: This platform is designed exclusively for authorized penetration testing, security auditing, and research. Unauthorized use is strictly prohibited and illegal.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Security First](#-security-first)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Documentation](#-documentation)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**Akira SASE** is a next-generation cybersecurity platform that combines offensive and defensive security capabilities in a unified, API-driven system. Built with enterprise-grade security and modern architecture, it provides security teams with powerful tools for:

- 🔴 **Offensive Security**: Authorized reconnaissance, vulnerability scanning, and security testing
- 🔵 **Defensive Security**: Active defense, threat detection, and automated response
- 🤖 **Security Operations**: Automated workflows and intelligent analysis

### Built For

- Security Operations Centers (SOCs)
- Penetration Testing Teams
- Red Team/Blue Team Exercises
- Security Researchers
- Bug Bounty Hunters
- Cybersecurity Education

---

## ✨ Key Features

### 🔴 Offensive Capabilities

#### Network Reconnaissance
- **Nmap Integration**: Professional-grade network scanning
- **Service Detection**: Identify services, versions, and OS
- **Vulnerability Mapping**: Automated CVE correlation
- **Custom Scan Profiles**: Stealth, aggressive, and custom modes

#### OSINT Collection
- **Domain Intelligence**: DNS, WHOIS, subdomain enumeration
- **Threat Intelligence**: Integration with threat feeds
- **Data Aggregation**: Automated intelligence gathering
- **Report Generation**: Comprehensive OSINT reports

#### Vulnerability Verification
- **Ethical Exploit Framework**: Safe verification without damage
- **CVE Database**: Up-to-date vulnerability information
- **Proof of Concept**: Evidence generation for reporting
- **Remediation Guidance**: Fix recommendations

### 🔵 Defensive Capabilities

#### Firewall Management
- **Dynamic Rules**: Automated firewall rule creation
- **IP Blocking**: Instant malicious IP blocking
- **Platform Support**: Linux (iptables) and Windows firewall
- **Rule Templates**: Pre-configured security policies

#### Honeypot Deployment
- **Service Emulation**: SSH, HTTP, FTP honeypots
- **Attacker Tracking**: Log and analyze attacker behavior
- **Automated Response**: Auto-block attacking IPs
- **Forensic Data**: Capture attack artifacts

#### Threat Detection
- **Log Analysis**: Automated security log parsing
- **Pattern Recognition**: Identify attack signatures
- **Anomaly Detection**: ML-based threat identification
- **Alert Generation**: Real-time security notifications

### 🔐 Security & Compliance

#### Authentication & Authorization
- **JWT Tokens**: Industry-standard authentication
- **API Keys**: Alternative auth method
- **Role-Based Access**: Granular permissions (admin, operator, viewer)
- **Session Management**: Secure token lifecycle

#### Rate Limiting
- **Request Throttling**: Prevent abuse
- **Scan Limits**: 10 scans/hour default
- **Customizable**: Per-user and per-endpoint limits
- **Graceful Degradation**: Informative error responses

#### Target Authorization
- **Whitelist System**: Only scan authorized targets
- **CIDR Support**: Network range authorization
- **Critical Infrastructure Protection**: Auto-block government, emergency services
- **Public Service Protection**: Block major platforms (Google, AWS, etc.)

#### Audit & Compliance
- **Comprehensive Logging**: All actions logged
- **Firebase Integration**: Persistent audit trail
- **Export Capabilities**: Reports for compliance
- **Forensic Ready**: Immutable log storage

---

## 🔒 Security First

Akira SASE is built with security as the foundation:

### Secure by Default
- ✅ All secrets in environment variables
- ✅ JWT with strong encryption (HS256+)
- ✅ Rate limiting enabled
- ✅ Target whitelisting required
- ✅ HTTPS enforced in production
- ✅ No hardcoded credentials

### Protection Mechanisms
- 🛡️ **Input Validation**: Pydantic schemas for all inputs
- 🛡️ **SQL Injection Prevention**: Parameterized queries
- 🛡️ **XSS Protection**: Output sanitization
- 🛡️ **CSRF Protection**: Token-based protection
- 🛡️ **DDoS Mitigation**: Rate limiting and throttling

### Compliance
- 📋 **OWASP Top 10**: Protection against all major threats
- 📋 **GDPR Ready**: Data protection and privacy
- 📋 **SOC 2**: Logging and monitoring
- 📋 **PCI DSS**: Secure credential handling

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)
- OpenAI API key
- Firebase project

### 1. Clone & Setup
```bash
git clone https://github.com/dajarony/akira.git
cd akira
python scripts/setup.py  # Interactive setup wizard
```

### 2. Configure
```bash
# Edit .env with your credentials
nano .env

# Add Firebase credentials
# Download from Firebase Console → Project Settings → Service Accounts
cp your-firebase-credentials.json firebase-credentials.json
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run
```bash
# Development
python main.py

# Production (Docker)
docker-compose up -d
```

### 5. Access API
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/ping
- **OpenAPI Spec**: http://localhost:8000/openapi.json

---

## 🏗️ Architecture

```
akira/
├── core/                           # Core system components
│   ├── config.py                   # Configuration management
│   ├── logger.py                   # Structured logging
│   ├── auth.py                     # JWT authentication
│   ├── rate_limiter.py             # Rate limiting
│   ├── target_authorization.py     # Target whitelisting
│   ├── services.py                 # External service integration
│   └── exceptions.py               # Error handling
│
├── models/                         # Pydantic data models
│   ├── common_models.py            # Shared models
│   ├── scan_models.py              # Scan request/response models
│   └── defense_models.py           # Defense models
│
├── modules/                        # Functional modules
│   ├── offense/                    # Offensive tools
│   │   ├── nmap_scanner.py         # Network scanning
│   │   ├── osint_collector.py      # OSINT gathering
│   │   └── exploit_launcher.py     # Exploit framework
│   │
│   ├── defense/                    # Defensive tools
│   │   ├── firewall_manager.py     # Firewall automation
│   │   ├── honeypot_deployer.py    # Honeypot management
│   │   └── ai_threat_detector.py   # Threat detection
│   │
│   └── shared/                     # Shared utilities
│       ├── utils.py                # General utilities
│       └── validators.py           # Input validation
│
├── api/                            # REST API endpoints
│   ├── offense.py                  # Offensive endpoints
│   ├── defense.py                  # Defensive endpoints
│   └── status.py                   # System status
│
├── tests/                          # Test suite
│   ├── test_api.py                 # API tests
│   ├── test_offense.py             # Offensive module tests
│   └── test_defense.py             # Defensive module tests
│
├── docs/                           # 📚 Documentation
│   ├── SECURITY.md                 # Security policies
│   ├── DEPLOYMENT.md               # Deployment guide
│   ├── DEPLOYMENT_INSTRUCTIONS.md  # Step-by-step deployment
│   ├── CHANGELOG.md                # Version history
│   ├── ROADMAP.md                  # Future plans
│   └── README.md                   # Documentation index
│
├── scripts/                        # 🔧 Automation scripts
│   ├── setup.py                    # Interactive setup wizard
│   ├── deploy_to_github.sh         # GitHub deployment (Linux/Mac)
│   ├── deploy_to_github.bat        # GitHub deployment (Windows)
│   ├── run_akira.py                # Run script
│   └── README.md                   # Scripts documentation
│
├── config/                         # ⚙️ Configuration files
│   ├── .env.example                # Environment template
│   ├── firebase-credentials.example.json  # Firebase template
│   ├── Dockerfile                  # Container definition
│   └── README.md                   # Config documentation
│
├── .github/                        # GitHub Actions CI/CD
│   └── workflows/
│       └── ci-cd.yml               # Automated testing & deployment
│
├── main.py                         # Application entry point
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

### Design Principles

#### SUME (Sistema Universal de Modularización Estratégica)
- **Modular Architecture**: Independent, reusable components
- **Clear Interfaces**: Well-defined APIs between modules
- **Single Responsibility**: Each module has one purpose
- **Extensibility**: Easy to add new capabilities

#### STDG (Sistema de Trazabilidad Dinámica Global)
- **Complete Traceability**: All actions logged
- **Dynamic Tracking**: Real-time activity monitoring
- **Global Visibility**: Centralized logging and metrics
- **Audit Trail**: Forensic-ready logging

---

## 📚 Documentation

### Core Documents
- [SECURITY.md](docs/SECURITY.md) - Security policies and best practices
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Production deployment guide
- [DEPLOYMENT_INSTRUCTIONS.md](docs/DEPLOYMENT_INSTRUCTIONS.md) - Step-by-step setup
- [CHANGELOG.md](docs/CHANGELOG.md) - Version history and release notes
- [ROADMAP.md](docs/ROADMAP.md) - Future features and plans
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (Swagger UI)

### Quick References
- [Authentication Guide](#authentication)
- [Rate Limiting](#rate-limiting)
- [Target Authorization](#target-authorization)
- [Examples & Tutorials](#examples)
- [Documentation Index](docs/README.md) - Full documentation directory

---

## 📊 API Reference

### Authentication

#### Login (Get JWT Token)
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your-password"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Using Token
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/offense/nmap
```

### Offensive Operations

#### Nmap Scan
```bash
POST /offense/nmap
Authorization: Bearer YOUR_TOKEN

{
  "target": {
    "ip": "192.168.1.100"
  },
  "scan_type": "tcp_syn",
  "port_range": "1-1000"
}
```

#### OSINT Collection
```bash
POST /offense/osint
Authorization: Bearer YOUR_TOKEN

{
  "target_domain": "example.com",
  "sources": ["dns_records", "whois", "subdomain_enum"],
  "depth_level": 2
}
```

### Defensive Operations

#### Create Firewall Rule
```bash
POST /defense/firewall/rule
Authorization: Bearer YOUR_TOKEN

{
  "rule_name": "Block_Suspicious_IP",
  "action": "deny",
  "source_ip": "192.168.1.100",
  "protocol": "tcp",
  "destination_port": "22"
}
```

#### Deploy Honeypot
```bash
POST /defense/honeypot
Authorization: Bearer YOUR_TOKEN

{
  "honeypot_name": "SSH_Trap",
  "honeypot_type": "ssh",
  "port": 2222,
  "auto_block_attackers": true
}
```

### System Status

#### Health Check
```bash
GET /status/health
```

#### System Information
```bash
GET /status/system-info
Authorization: Bearer YOUR_TOKEN
```

---

## 🧪 Examples

### Example 1: Authorized Network Scan
```python
import requests

# Login
response = requests.post('http://localhost:8000/auth/login', json={
    'username': 'admin',
    'password': 'your-password'
})
token = response.json()['access_token']

# Scan authorized target
headers = {'Authorization': f'Bearer {token}'}
scan_request = {
    'target': {'ip': '192.168.1.0/24'},
    'scan_type': 'tcp_syn',
    'port_range': '1-1000'
}
response = requests.post(
    'http://localhost:8000/offense/nmap',
    json=scan_request,
    headers=headers
)
print(response.json())
```

### Example 2: Auto-Block Malicious IP
```python
# Block an attacking IP automatically
block_request = {
    'ip_address': '203.0.113.42',
    'threat_level': 'HIGH',
    'duration_hours': 24
}
response = requests.post(
    'http://localhost:8000/defense/firewall/block',
    json=block_request,
    headers=headers
)
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone repo
git clone https://github.com/dajarony/akira.git
cd akira

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 .
black --check .
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Legal Disclaimer

**IMPORTANT**: Akira SASE is a powerful cybersecurity tool that must be used responsibly and legally.

### Authorized Use Only
- ✅ You **MUST** have explicit written permission to test any system
- ✅ Use only on systems you own or have authorization to test
- ✅ Comply with all applicable laws and regulations
- ✅ Respect bug bounty program rules and scopes

### Prohibited Activities
- ❌ Unauthorized network scanning or penetration testing
- ❌ Attacking critical infrastructure
- ❌ Violating computer fraud and abuse laws
- ❌ Using for malicious purposes

### Liability
The developers and contributors of Akira SASE:
- Are NOT responsible for misuse of this software
- Provide this tool "AS IS" without warranty
- Encourage responsible disclosure and ethical hacking
- Support only legal and authorized security research

**By using Akira SASE, you agree to use it only for lawful purposes and in accordance with all applicable laws.**

---

## 🌟 Acknowledgments

- **FastAPI** - Modern web framework
- **OpenAI** - Intelligence capabilities
- **Firebase** - Real-time database
- **Nmap** - Network scanning
- **OWASP** - Security best practices
- **Python Community** - Amazing ecosystem

---

## 📞 Contact & Support

- **Website**: https://akira-cyber.com
- **Documentation**: https://docs.akira-cyber.com
- **Issues**: https://github.com/dajarony/akira/issues
- **Security**: security@akira-cyber.com
- **General**: support@akira-cyber.com
- **Twitter**: @AkiraSASE

---

<div align="center">

**Akira SASE v2.0.0** | Built with ❤️ and ☕ by the Security Community

[⬆ Back to Top](#-akira-sase-cyberwar-platform)

</div>
