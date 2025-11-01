# 🔧 Akira SASE - Scripts

This directory contains automation and utility scripts.

## 📜 Scripts

### Setup & Configuration
- **setup.py** - Interactive setup wizard
  - Generates secure keys
  - Creates configuration files
  - Checks dependencies
  - Initializes project structure

  ```bash
  python scripts/setup.py
  ```

### Deployment
- **deploy_to_github.sh** - Automated GitHub deployment (Linux/Mac)
  ```bash
  chmod +x scripts/deploy_to_github.sh
  ./scripts/deploy_to_github.sh
  ```

- **deploy_to_github.bat** - Automated GitHub deployment (Windows)
  ```cmd
  scripts\deploy_to_github.bat
  ```

- **deploy.py** - General deployment script
  ```bash
  python scripts/deploy.py
  ```

### Execution
- **run_akira.py** - Standard run script
  ```bash
  python scripts/run_akira.py
  ```

- **start_akira.py** - Alternative start script
  ```bash
  python scripts/start_akira.py
  ```

### Installation
- **install.sh** - System dependencies installation (Linux)
  ```bash
  chmod +x scripts/install.sh
  ./scripts/install.sh
  ```

## 🎯 Quick Start

```bash
# 1. Setup project
python scripts/setup.py

# 2. Run application
python main.py

# Or use run script
python scripts/run_akira.py
```

## 🔐 Security Notes

- Never commit generated secrets
- Review scripts before execution
- Run setup.py in trusted environments only
- Deployment scripts check for exposed secrets

---

**Last Updated**: 2025-01-01
