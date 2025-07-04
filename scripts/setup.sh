#!/usr/bin/env bash
set -euo pipefail

# Setup script for Parallel AI Agents project
# Idempotent - safe to run multiple times

echo "🚀 Setting up Parallel AI Agents project..."

# Check if setup was already completed
if [ -f .setup-complete ]; then
  echo "✅ Setup already run – skipping."
  exit 0
fi

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Error: Not a git repository. Please run 'git init' first."
    exit 1
fi

# Create agent branches
echo "📌 Creating agent branches..."

# Backend agent branch
git checkout -b backend-opus 2>/dev/null || git checkout backend-opus
echo "✅ backend-opus branch ready"

# Frontend agent branch  
git checkout -b frontend-opus 2>/dev/null || git checkout frontend-opus
echo "✅ frontend-opus branch ready"

# Test agent branch
git checkout -b test-opus 2>/dev/null || git checkout test-opus
echo "✅ test-opus branch ready"

# Return to main
git checkout main
echo "✅ Returned to main branch"

# Create initial directory structure on each branch
echo "📁 Creating directory structures..."

# Backend directories
git checkout backend-opus
mkdir -p backend/{src,tests,config}
mkdir -p docs/api
touch backend/package.json
git add .
git commit -m "[backend-opus] chore: initialize backend structure" 2>/dev/null || true

# Frontend directories
git checkout frontend-opus
mkdir -p frontend/{src,public,tests}
mkdir -p docs/ui
touch frontend/package.json
git add .
git commit -m "[frontend-opus] chore: initialize frontend structure" 2>/dev/null || true

# Test directories
git checkout test-opus
mkdir -p tests/{unit,integration,e2e,performance}
mkdir -p docs/testing
touch tests/jest.config.js
git add .
git commit -m "[test-opus] chore: initialize test structure" 2>/dev/null || true

# Return to main
git checkout main

# Install dependencies
echo "📦 Installing dependencies..."
if command -v pnpm &> /dev/null; then
    corepack enable
    pnpm install
else
    npm install
fi

# Install husky hooks
npx husky install

# Mark setup as complete
touch .setup-complete

echo ""
echo "✨ Setup complete! Next steps:"
echo ""
echo "1. Open VS Code with the workspace:"
echo "   code .vscode/parallel-agents.code-workspace"
echo ""
echo "2. Launch agents in separate terminals:"
echo "   Terminal 1: npm run agent:backend"
echo "   Terminal 2: npm run agent:frontend"
echo "   Terminal 3: npm run agent:test"
echo ""
echo "3. Run supervisor to monitor progress:"
echo "   python scripts/supervisor.py --monitor"
echo ""
echo "Happy coding with your AI agent team! 🤖🤖🤖"