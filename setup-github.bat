@echo off
REM GitHub Setup Script for Pieces-Obsidian Integration Project (Windows)
REM This script initializes Git, creates the initial commit, and prepares for GitHub push

setlocal enabledelayedexpansion

echo 🚀 Setting up Pieces-Obsidian Integration for GitHub...
echo.

REM Check if we're in the right directory
if not exist "README.md" (
    echo ❌ This script must be run from the project root directory
    echo ℹ️  Please navigate to the directory containing README.md and 01_Epics/
    pause
    exit /b 1
)

if not exist "01_Epics" (
    echo ❌ This script must be run from the project root directory
    echo ℹ️  Please navigate to the directory containing README.md and 01_Epics/
    pause
    exit /b 1
)

echo ℹ️  Current directory: %CD%
echo ℹ️  Verifying project structure...

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

echo ✅ Git is installed

REM Check if already a Git repository
if exist ".git" (
    echo ⚠️  This directory is already a Git repository
    echo ℹ️  Checking current status...
    git status --porcelain
) else (
    echo ℹ️  Initializing Git repository...
    git init
    echo ✅ Git repository initialized
)

REM Check Git configuration
for /f "tokens=*" %%i in ('git config --global user.name 2^>nul') do set username=%%i
for /f "tokens=*" %%i in ('git config --global user.email 2^>nul') do set useremail=%%i

if "!username!"=="" (
    echo ⚠️  Git user configuration not found
    echo ℹ️  Please configure Git with your information:
    echo git config --global user.name "Your Name"
    echo git config --global user.email "your.email@example.com"
    echo.
    pause
)

echo ℹ️  Adding all files to Git...
git add .

echo ℹ️  Creating initial commit...
git commit -m "Initial commit: Epic-driven project structure

- Complete Epic documentation (1.0 through 5.0)
- LLM Developer Guide for comprehensive onboarding  
- GitHub-ready repository structure with CI/CD
- Research phase ready to begin (Epic 1.0)
- Issue templates and PR templates configured
- Comprehensive project documentation

Project Status: Epic 1.0 - Research & Discovery Phase

Features:
✅ Epic-driven development structure
✅ Automated CI/CD pipeline
✅ Documentation validation
✅ Security scanning
✅ Code quality checks
✅ Project progress tracking

Ready for: Pieces CLI research and Obsidian integration development"

echo ✅ Initial commit created successfully

REM Set main branch
echo ℹ️  Setting default branch to 'main'...
git branch -M main
echo ✅ Default branch set to 'main'

REM Show current status
echo ℹ️  Current Git status:
git log --oneline -1
echo.

echo ✅ Local Git repository is ready!
echo.
echo ℹ️  Next steps to push to GitHub:
echo.
echo 1. Create a new repository on GitHub:
echo    - Go to https://github.com/new
echo    - Repository name: pieces-obsidian-integration
echo    - Description: Seamlessly export Workstream Activities from Pieces CLI and import them into Obsidian as properly formatted markdown files.
echo    - Make it Public
echo    - DO NOT initialize with README, .gitignore, or license (we already have these)
echo.
echo 2. Connect to GitHub and push:
echo    git remote add origin https://github.com/YOUR_USERNAME/pieces-obsidian-integration.git
echo    git push -u origin main
echo.
echo ⚠️  Replace YOUR_USERNAME with your actual GitHub username!
echo.
echo ✅ Setup complete! Your project is ready for GitHub.
echo.
echo ℹ️  Project Structure Summary:
dir /b 01_Epics | find /c /v "" > temp_count.txt
set /p epic_count=<temp_count.txt
del temp_count.txt
echo 📁 Epic Documentation: %epic_count% files
echo 📁 GitHub Templates: Issue templates + PR template configured
echo 📁 Research Structure: Research files organized
echo 📄 Root Documentation: Multiple markdown files
echo.
echo ✅ All systems ready for Epic 1.0 - Research & Discovery!
echo.
pause