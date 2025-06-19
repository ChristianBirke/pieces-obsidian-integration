#!/bin/bash

# GitHub Setup Script for Pieces-Obsidian Integration Project
# This script initializes Git, creates the initial commit, and prepares for GitHub push

set -e  # Exit on any error

echo "🚀 Setting up Pieces-Obsidian Integration for GitHub..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [[ ! -f "README.md" ]] || [[ ! -d "01_Epics" ]]; then
    print_error "This script must be run from the project root directory"
    print_info "Please navigate to the directory containing README.md and 01_Epics/"
    exit 1
fi

print_info "Current directory: $(pwd)"
print_info "Verifying project structure..."

# Verify all required files exist
required_files=(
    "README.md"
    "README-LLM-Developer-Guide.md"
    "01_Epics/00_ProjectOverview.md"
    "01_Epics/Epic1.0-ResearchAndDiscovery.md"
    "01_Epics/Epic2.0-TechnicalArchitecture.md"
    "01_Epics/Epic3.0-CoreIntegrationImplementation.md"
    "01_Epics/Epic4.0-UserExperienceAndAutomation.md"
    "01_Epics/Epic5.0-TestingAndDocumentation.md"
    "01_Epics/TechnicalRoadmap.md"
    "01_Epics/DevelopmentQuickStart.md"
    ".github/workflows/ci.yml"
    ".gitignore"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        missing_files+=("$file")
    fi
done

if [[ ${#missing_files[@]} -eq 0 ]]; then
    print_status "All required project files are present"
else
    print_error "Missing required files:"
    printf '%s\n' "${missing_files[@]}"
    exit 1
fi

# Check if Git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

print_status "Git is installed"

# Check if already a Git repository
if [[ -d ".git" ]]; then
    print_warning "This directory is already a Git repository"
    print_info "Checking current status..."
    git status --porcelain
else
    print_info "Initializing Git repository..."
    git init
    print_status "Git repository initialized"
fi

# Configure Git if not already configured
if [[ -z "$(git config --global user.name)" ]] || [[ -z "$(git config --global user.email)" ]]; then
    print_warning "Git user configuration not found"
    print_info "Please configure Git with your information:"
    echo "git config --global user.name 'Your Name'"
    echo "git config --global user.email 'your.email@example.com'"
    echo ""
    read -p "Press Enter after configuring Git to continue..."
fi

print_info "Adding all files to Git..."
git add .

print_info "Creating initial commit..."
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

print_status "Initial commit created successfully"

# Set main branch
print_info "Setting default branch to 'main'..."
git branch -M main
print_status "Default branch set to 'main'"

# Show current status
print_info "Current Git status:"
git log --oneline -1
echo ""

print_status "Local Git repository is ready!"
echo ""
print_info "Next steps to push to GitHub:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: pieces-obsidian-integration"
echo "   - Description: Seamlessly export Workstream Activities from Pieces CLI and import them into Obsidian as properly formatted markdown files."
echo "   - Make it Public"
echo "   - DO NOT initialize with README, .gitignore, or license (we already have these)"
echo ""
echo "2. Connect to GitHub and push:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/pieces-obsidian-integration.git"
echo "   git push -u origin main"
echo ""
print_warning "Replace YOUR_USERNAME with your actual GitHub username!"
echo ""
print_status "Setup complete! Your project is ready for GitHub."

# Show project structure summary
echo ""
print_info "Project Structure Summary:"
echo "📁 Epic Documentation: $(ls -1 01_Epics/ | wc -l | tr -d ' ') files"
echo "📁 GitHub Templates: $(ls -1 .github/ISSUE_TEMPLATE/ | wc -l | tr -d ' ') issue templates + PR template"
echo "📁 Research Structure: $(find research/ -name "*.md" | wc -l | tr -d ' ') research files"
echo "📄 Root Documentation: $(ls -1 *.md | wc -l | tr -d ' ') markdown files"
echo ""
print_status "All systems ready for Epic 1.0 - Research & Discovery!"