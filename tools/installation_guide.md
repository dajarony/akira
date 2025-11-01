# Security Tools Installation Guide

## Core Tools (Install manually)

### 1. Nikto (Web Scanner)
```bash
# Ubuntu/Debian
sudo apt install nikto

# Windows
# Download from https://github.com/sullo/nikto
```

### 2. SQLMap (SQL Injection)
```bash
# Python package
pip install sqlmap-python

# Or download from https://github.com/sqlmapproject/sqlmap
```

### 3. Dirb (Directory Brute Force)
```bash
# Ubuntu/Debian
sudo apt install dirb

# Windows/macOS
# Download from http://dirb.sourceforge.net/
```

### 4. Metasploit (Advanced - Optional)
```bash
# Ubuntu/Debian
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
sudo ./msfinstall

# Windows
# Download installer from https://www.metasploit.com/download
```

## API Keys Needed

### Free APIs:
- Shodan: https://developer.shodan.io/api/requirements
- VirusTotal: https://developers.virustotal.com/reference
- HaveIBeenPwned: https://haveibeenpwned.com/API/v3

### Paid APIs (Optional):
- SecurityTrails: https://securitytrails.com/corp/apidocs
- Censys: https://search.censys.io/api

## Notes:
- Start with free APIs for basic functionality
- Install tools one by one and test
- Always get permission before scanning external targets
- Use in isolated environments for safety
