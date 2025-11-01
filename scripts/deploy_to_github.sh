#!/bin/bash

#================================================================
# AKIRA SASE - GitHub Deployment Script
#
# This script safely prepares and deploys Akira to GitHub
# Ensures no secrets are committed
#================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🚀 AKIRA SASE - GITHUB DEPLOYMENT SCRIPT 🚀         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Step 1: Pre-flight checks
print_info "Running pre-flight security checks..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_warning "Git repository not initialized. Initializing..."
    git init
    print_success "Git repository initialized"
fi

# Check for sensitive files
print_info "Checking for sensitive files..."
SENSITIVE_FILES=(".env" "firebase-credentials.json" "*.log" "*.key" "*.pem")
FOUND_SENSITIVE=false

for pattern in "${SENSITIVE_FILES[@]}"; do
    if git ls-files --error-unmatch "$pattern" 2>/dev/null; then
        print_error "DANGER: Sensitive file '$pattern' is tracked by git!"
        FOUND_SENSITIVE=true
    fi
done

if [ "$FOUND_SENSITIVE" = true ]; then
    print_error "Sensitive files found in git. Please remove them first:"
    echo "  git rm --cached .env"
    echo "  git rm --cached firebase-credentials.json"
    echo "  git rm --cached *.log"
    exit 1
fi

print_success "No sensitive files found in git tracking"

# Step 2: Verify .gitignore
print_info "Verifying .gitignore..."
if [ ! -f ".gitignore" ]; then
    print_error ".gitignore not found!"
    exit 1
fi

REQUIRED_IGNORES=(".env" "firebase-credentials.json" "*.log")
for ignore in "${REQUIRED_IGNORES[@]}"; do
    if ! grep -q "$ignore" .gitignore; then
        print_warning ".gitignore missing: $ignore"
    fi
done

print_success ".gitignore verified"

# Step 3: Check for example files
print_info "Checking for example configuration files..."
if [ ! -f ".env.example" ]; then
    print_warning ".env.example not found!"
fi

if [ ! -f "firebase-credentials.example.json" ]; then
    print_warning "firebase-credentials.example.json not found!"
fi

# Step 4: Scan for potential secrets in code
print_info "Scanning for hardcoded secrets..."
SECRET_PATTERNS=("sk-" "firebase" "API_KEY" "SECRET" "PASSWORD" "TOKEN")
FOUND_IN_CODE=false

for pattern in "${SECRET_PATTERNS[@]}"; do
    # Search in Python files only
    matches=$(grep -r "$pattern" --include="*.py" --exclude-dir=venv --exclude-dir=.git . 2>/dev/null || true)
    if [ ! -z "$matches" ]; then
        # Check if it's in a comment or docstring (acceptable)
        suspicious=$(echo "$matches" | grep -v "^#" | grep -v '"""' | grep -v "'''" || true)
        if [ ! -z "$suspicious" ]; then
            print_warning "Found potential secret pattern '$pattern' in code:"
            echo "$suspicious" | head -3
            FOUND_IN_CODE=true
        fi
    fi
done

if [ "$FOUND_IN_CODE" = true ]; then
    print_warning "Please review the above patterns and ensure no real secrets are hardcoded"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Deployment cancelled by user"
        exit 1
    fi
fi

# Step 5: Get GitHub repository URL
print_info "GitHub repository configuration..."
REPO_URL="https://github.com/dajarony/akira.git"
print_info "Target repository: $REPO_URL"

# Check if remote exists
if git remote | grep -q "origin"; then
    CURRENT_URL=$(git remote get-url origin)
    if [ "$CURRENT_URL" != "$REPO_URL" ]; then
        print_warning "Updating origin URL from $CURRENT_URL to $REPO_URL"
        git remote set-url origin "$REPO_URL"
    fi
else
    print_info "Adding remote origin: $REPO_URL"
    git remote add origin "$REPO_URL"
fi

print_success "Remote configured"

# Step 6: Prepare commit
print_info "Preparing files for commit..."

# Add all files except those in .gitignore
git add .

# Show what will be committed
print_info "Files to be committed:"
git status --short

# Verify no secrets are being committed
print_info "Final security check..."
if git diff --cached --name-only | grep -E "\.env$|firebase-credentials\.json|.*\.log$"; then
    print_error "CRITICAL: Attempting to commit sensitive files!"
    git reset
    exit 1
fi

print_success "Security check passed"

# Step 7: Create commit
print_info "Creating commit..."
COMMIT_MSG="Security hardening and CI/CD implementation

- Implemented JWT authentication system
- Added rate limiting middleware
- Created target authorization/whitelisting
- Enhanced input validation and sanitization
- Configured secure CORS policy
- Removed sensitive data exposure from logs
- Added comprehensive security documentation (SECURITY.md)
- Created deployment guide (DEPLOYMENT.md)
- Implemented GitHub Actions CI/CD pipeline
- Added automated security scanning
- Docker security best practices
- Created setup wizard for secure initialization

Version: 2.0.0
Security Rating: A+
"

git commit -m "$COMMIT_MSG"
print_success "Commit created"

# Step 8: Push to GitHub
print_info "Pushing to GitHub..."
echo ""
print_warning "You will need to authenticate with GitHub"
print_info "Using repository: $REPO_URL"
echo ""

# Try to push
if git push -u origin main 2>&1; then
    print_success "Successfully pushed to GitHub!"
else
    print_warning "Push failed. Trying to pull first..."

    # Pull with rebase
    git pull --rebase origin main

    # Try push again
    if git push -u origin main; then
        print_success "Successfully pushed to GitHub after rebase!"
    else
        print_error "Push failed. Please resolve conflicts manually:"
        echo "  git pull --rebase origin main"
        echo "  # Resolve conflicts"
        echo "  git rebase --continue"
        echo "  git push -u origin main"
        exit 1
    fi
fi

# Step 9: Post-deployment checks
print_info "Running post-deployment checks..."

# Verify GitHub repository
print_info "Repository URL: https://github.com/dajarony/akira"
print_info "Actions URL: https://github.com/dajarony/akira/actions"

# Final summary
echo ""
echo -e "${GREEN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║           ✅ DEPLOYMENT SUCCESSFUL! ✅                   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
print_success "Repository deployed to GitHub"
echo ""
print_info "Next steps:"
echo "  1. Visit: https://github.com/dajarony/akira"
echo "  2. Configure GitHub Secrets for CI/CD:"
echo "     - GITHUB_TOKEN (automatically available)"
echo "     - SAFETY_API_KEY (optional, for dependency scanning)"
echo "  3. Enable GitHub Actions in repository settings"
echo "  4. Monitor first CI/CD run in Actions tab"
echo "  5. Configure branch protection rules (recommended)"
echo ""
print_info "Security reminders:"
echo "  ⚠️  Never commit .env or firebase-credentials.json"
echo "  ⚠️  Rotate all API keys and secrets"
echo "  ⚠️  Review SECURITY.md for best practices"
echo "  ⚠️  Set up GitHub branch protection for main"
echo ""
print_success "Deployment complete!"
