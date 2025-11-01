# 📁 Akira SASE - Project Structure

This document provides a complete overview of the project organization.

## 🗂️ Directory Structure

```
akira/
│
├── 📁 api/                         # REST API Endpoints
│   ├── __init__.py                 # API router exports
│   ├── offense.py                  # Offensive security endpoints
│   ├── defense.py                  # Defensive security endpoints
│   ├── defense_endpoints.py        # Additional defense endpoints
│   └── status.py                   # System status and health checks
│
├── 📁 core/                        # Core System Components
│   ├── __init__.py                 # Core exports
│   ├── config.py                   # Configuration management
│   ├── logger.py                   # Structured logging system
│   ├── services.py                 # External services (OpenAI, Firebase)
│   ├── exceptions.py               # Custom exception classes
│   ├── auth.py                     # JWT authentication system
│   ├── rate_limiter.py             # Rate limiting middleware
│   └── target_authorization.py     # Target whitelisting system
│
├── 📁 models/                      # Data Models (Pydantic)
│   ├── __init__.py                 # Model exports
│   ├── base_models.py              # Base model classes
│   ├── common_models.py            # Common shared models
│   ├── scan_models.py              # Scan-related models
│   ├── defense_models.py           # Defense-related models
│   ├── exploit_models.py           # Exploit-related models
│   ├── osint_models.py             # OSINT-related models
│   ├── requests.py                 # Request models
│   ├── responses.py                # Response models
│   └── additional_models.py        # Additional models
│
├── 📁 modules/                     # Functional Modules
│   ├── __init__.py
│   │
│   ├── 📁 offense/                 # Offensive Tools
│   │   ├── __init__.py
│   │   ├── nmap_scanner.py         # Nmap integration
│   │   ├── osint_collector.py      # OSINT data collection
│   │   └── exploit_launcher.py     # Ethical exploit framework
│   │
│   ├── 📁 defense/                 # Defensive Tools
│   │   ├── __init__.py
│   │   ├── firewall_manager.py     # Firewall automation
│   │   ├── honeypot_deployer.py    # Honeypot deployment
│   │   └── ai_threat_detector.py   # AI-powered threat detection
│   │
│   └── 📁 shared/                  # Shared Utilities
│       ├── __init__.py
│       ├── utils.py                # General utilities
│       └── validators.py           # Input validation
│
├── 📁 tests/                       # Test Suite
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration
│   ├── .env.test                   # Test environment config
│   ├── firebase-credentials-test.json  # Test Firebase credentials
│   │
│   ├── test_api.py                 # API endpoint tests
│   ├── test_offense.py             # Offensive module tests
│   ├── test_defense.py             # Defensive module tests
│   ├── test_nmap_scanner.py        # Nmap scanner tests
│   ├── test_osint_collector.py     # OSINT collector tests
│   ├── test_exploit_launcher.py    # Exploit launcher tests
│   ├── test_firewall_manager.py    # Firewall manager tests
│   ├── test_honeypot_deployer.py   # Honeypot deployer tests
│   ├── test_ai_threat_detector.py  # AI threat detector tests
│   │
│   └── comprehensive_test_suite.py # Complete test suite
│
├── 📁 docs/                        # Documentation
│   ├── README.md                   # Documentation index
│   ├── SECURITY.md                 # Security policies (5,000+ words)
│   ├── DEPLOYMENT.md               # Deployment guide (7,000+ words)
│   ├── DEPLOYMENT_INSTRUCTIONS.md  # Step-by-step setup
│   ├── DEPLOYMENT_SUCCESS.md       # Deployment verification
│   ├── CHANGELOG.md                # Version history
│   ├── ROADMAP.md                  # Future development
│   ├── INTEGRATION_GUIDE.md        # Integration guide
│   ├── FRONTEND_IMPROVEMENTS.md    # Frontend documentation
│   └── README_COMPLETE.md          # Extended README
│
├── 📁 scripts/                     # Automation Scripts
│   ├── README.md                   # Scripts documentation
│   ├── setup.py                    # Interactive setup wizard
│   ├── deploy_to_github.sh         # GitHub deployment (Linux/Mac)
│   ├── deploy_to_github.bat        # GitHub deployment (Windows)
│   ├── deploy.py                   # General deployment script
│   ├── run_akira.py                # Standard run script
│   ├── start_akira.py              # Alternative start script
│   └── install.sh                  # System dependencies installer
│
├── 📁 config/                      # Configuration Files
│   ├── README.md                   # Configuration documentation
│   ├── .env.example                # Environment variables template
│   ├── firebase-credentials.example.json  # Firebase template
│   └── Dockerfile                  # Container image definition
│
├── 📁 frontend/                    # Frontend (Optional)
│   ├── README.md                   # Frontend documentation
│   ├── index.html                  # Main HTML
│   ├── script.js                   # JavaScript
│   └── styles.css                  # Styles
│
├── 📁 tools/                       # Additional Tools
│   └── installation_guide.md       # Installation guide
│
├── 📁 backups/                     # Backup Files
│   ├── main.py.backup              # Main backup
│   ├── README.md.old               # Old README
│   └── models_backup/              # Old models
│
├── 📁 .archive/                    # Archived Files
│   ├── endpoint_discovery.py       # Old discovery script
│   ├── fix_attribute_errors.py     # Fix script
│   ├── fix_missing_models.py       # Model fix script
│   ├── make_akira_real.py          # Old realization script
│   ├── test_frontend.py            # Old frontend test
│   ├── test_integration.py         # Old integration test
│   ├── akira_realization_report.json      # Old report
│   ├── akira_test_report_20250618_211129.json  # Old test report
│   └── info.txt                    # Old info file
│
├── 📁 .github/workflows/           # CI/CD
│   └── ci-cd.yml                   # GitHub Actions pipeline
│
├── 📁 .vscode/                     # VSCode Configuration
│   └── settings.json               # Editor settings
│
├── 📄 main.py                      # Application Entry Point
├── 📄 requirements.txt             # Python Dependencies
├── 📄 .gitignore                   # Git ignore patterns
├── 📄 README.md                    # Main Documentation
├── 📄 PROJECT_STRUCTURE.md         # This file
│
└── 📄 .env                         # Environment Variables (NOT in git)
└── 📄 firebase-credentials.json    # Firebase Credentials (NOT in git)
```

## 📋 File Categories

### 🔐 Critical Files (Never Commit)
- `.env` - Environment variables with secrets
- `firebase-credentials.json` - Firebase service account credentials
- `*.log` - Log files
- `__pycache__/` - Python cache
- `.venv/`, `venv/` - Virtual environments

### 📝 Configuration Templates (Safe to Commit)
- `config/.env.example` - Environment template
- `config/firebase-credentials.example.json` - Firebase template

### 🚀 Entry Points
- `main.py` - Main application (FastAPI server)
- `scripts/run_akira.py` - Run script
- `scripts/setup.py` - Interactive setup

### 📚 Documentation
- `README.md` - Main project documentation
- `docs/` - All detailed documentation
- `*/README.md` - Directory-specific docs

### 🧪 Tests
- `tests/` - Complete test suite
- `pytest` compatible
- Coverage reports enabled

## 🎯 Quick Navigation

### For Users
1. Start here: [`README.md`](README.md)
2. Security: [`docs/SECURITY.md`](docs/SECURITY.md)
3. Setup: [`scripts/setup.py`](scripts/setup.py)
4. Deploy: [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)

### For Developers
1. Architecture: See [`README.md#architecture`](README.md#architecture)
2. API Endpoints: [`api/`](api/)
3. Core Systems: [`core/`](core/)
4. Tests: [`tests/`](tests/)
5. Contributing: Add new features to [`modules/`](modules/)

### For DevOps
1. CI/CD: [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml)
2. Docker: [`config/Dockerfile`](config/Dockerfile)
3. Deployment: [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)
4. Scripts: [`scripts/`](scripts/)

## 📊 Project Statistics

- **Total Files**: ~91 files
- **Lines of Code**: ~24,000+
- **Documentation**: ~15,000 words
- **Test Files**: 15+ test modules
- **API Endpoints**: 20+ endpoints
- **Security Modules**: 3 core modules (auth, rate limit, authorization)

## 🔄 Workflow

### Development Workflow
```
1. Clone repo
2. Run setup: python scripts/setup.py
3. Configure: Edit .env with your credentials
4. Install deps: pip install -r requirements.txt
5. Run tests: pytest tests/
6. Start server: python main.py
7. Access docs: http://localhost:8000/docs
```

### Deployment Workflow
```
1. Commit changes: git add . && git commit -m "message"
2. Run tests: pytest tests/
3. Push to GitHub: git push origin main
4. CI/CD runs automatically
5. Deploy to production (manual approval)
```

## 🏷️ Version Control

### Branches
- `main` - Production-ready code
- `develop` - Development branch (if using)
- `feature/*` - Feature branches
- `hotfix/*` - Hot fixes

### Tags
- `v2.0.0` - Current stable version
- `v1.0.0-MVP` - Original MVP version

---

**Last Updated**: 2025-01-01
**Version**: 2.0.0
**Maintained By**: Akira Security Team
