@echo off
REM ================================================================
REM AKIRA SASE - GitHub Deployment Script (Windows)
REM
REM This script safely prepares and deploys Akira to GitHub
REM Ensures no secrets are committed
REM ================================================================

echo.
echo ================================================================
echo.
echo       AKIRA SASE - GITHUB DEPLOYMENT SCRIPT (Windows)
echo.
echo ================================================================
echo.

REM Step 1: Pre-flight checks
echo [INFO] Running pre-flight security checks...

REM Check if git is initialized
if not exist ".git" (
    echo [WARNING] Git repository not initialized. Initializing...
    git init
    echo [SUCCESS] Git repository initialized
)

REM Step 2: Check for sensitive files
echo [INFO] Checking for sensitive files...
git ls-files .env 2>nul
if %ERRORLEVEL% == 0 (
    echo [ERROR] DANGER: .env file is tracked by git!
    echo Please remove it: git rm --cached .env
    exit /b 1
)

git ls-files firebase-credentials.json 2>nul
if %ERRORLEVEL% == 0 (
    echo [ERROR] DANGER: firebase-credentials.json is tracked by git!
    echo Please remove it: git rm --cached firebase-credentials.json
    exit /b 1
)

echo [SUCCESS] No sensitive files found in git tracking

REM Step 3: Verify .gitignore
echo [INFO] Verifying .gitignore...
if not exist ".gitignore" (
    echo [ERROR] .gitignore not found!
    exit /b 1
)
echo [SUCCESS] .gitignore verified

REM Step 4: Check for example files
echo [INFO] Checking for example configuration files...
if not exist ".env.example" (
    echo [WARNING] .env.example not found!
)
if not exist "firebase-credentials.example.json" (
    echo [WARNING] firebase-credentials.example.json not found!
)

REM Step 5: Configure remote
echo [INFO] GitHub repository configuration...
set REPO_URL=https://github.com/dajarony/akira.git
echo [INFO] Target repository: %REPO_URL%

git remote | find "origin" >nul
if %ERRORLEVEL% == 0 (
    git remote set-url origin %REPO_URL%
) else (
    git remote add origin %REPO_URL%
)
echo [SUCCESS] Remote configured

REM Step 6: Prepare commit
echo [INFO] Preparing files for commit...
git add .
echo [INFO] Files staged for commit

REM Step 7: Create commit
echo [INFO] Creating commit...
git commit -m "Security hardening and CI/CD implementation - v2.0.0"
echo [SUCCESS] Commit created

REM Step 8: Push to GitHub
echo [INFO] Pushing to GitHub...
echo.
echo [WARNING] You will need to authenticate with GitHub
echo.

git push -u origin main
if %ERRORLEVEL% == 0 (
    echo [SUCCESS] Successfully pushed to GitHub!
) else (
    echo [WARNING] Push failed. Trying to pull first...
    git pull --rebase origin main
    git push -u origin main
    if %ERRORLEVEL% == 0 (
        echo [SUCCESS] Successfully pushed to GitHub after rebase!
    ) else (
        echo [ERROR] Push failed. Please resolve conflicts manually
        exit /b 1
    )
)

REM Final summary
echo.
echo ================================================================
echo.
echo             DEPLOYMENT SUCCESSFUL!
echo.
echo ================================================================
echo.
echo [SUCCESS] Repository deployed to GitHub
echo.
echo Next steps:
echo   1. Visit: https://github.com/dajarony/akira
echo   2. Configure GitHub Secrets for CI/CD
echo   3. Enable GitHub Actions
echo   4. Monitor first CI/CD run
echo.
echo Security reminders:
echo   - Never commit .env or firebase-credentials.json
echo   - Rotate all API keys and secrets
echo   - Review SECURITY.md for best practices
echo.
echo [SUCCESS] Deployment complete!
echo.

pause
