# Developer Quick Reference - Parallel AI Agents

## 🚀 Quick Start

### Prerequisites Checklist
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] Git installed (`git --version`)
- [ ] Claude Code CLI installed
- [ ] OpenAI API key (for paper summarizer demo)
- [ ] GitHub CLI (optional, for PRs) (`gh --version`)

### Initial Setup (One Time)
```bash
# Clone the repository
git clone https://github.com/EARTHTOEDWARD/parallel-ai-agents.git
cd parallel-ai-agents

# Install dependencies
npm install

# Setup Git branches for agents
npm run setup

# Set environment variables
export OPENAI_API_KEY="your-key-here"
export DAILY_TOKEN_BUDGET=200000
```

## 🤖 Agent Commands

### Launch Individual Agents
```bash
# Backend Agent (Terminal 1)
npm run agent:backend
# Or manually:
claude-code --role backend --watch backend/ docs/mission-briefs/backend.md

# Frontend Agent (Terminal 2)  
npm run agent:frontend
# Or manually:
claude-code --role frontend --watch frontend/ docs/mission-briefs/frontend.md

# Test Agent (Terminal 3)
npm run agent:test
# Or manually:
claude-code --role tests --watch tests/ docs/mission-briefs/tests.md
```

### Launch All Agents Simultaneously
```bash
# Requires: npm install -g concurrently
npm run agents:all
```

### VS Code Integration
1. Open workspace: `code .vscode/parallel-agents.code-workspace`
2. Use Command Palette: `Cmd+Shift+P` → "Tasks: Run Task"
3. Select "Launch All Agents"

## 📊 Supervisor Commands

### Monitor Agent Status
```bash
# Basic monitoring
npm run supervisor

# With Python directly
python scripts/supervisor.py --monitor

# Monitor and create PRs for ready branches
npm run supervisor:prs
```

### Merge Agent Work
```bash
# Merge specific branch
npm run supervisor:merge backend-opus

# Merge with squash
python scripts/supervisor.py --merge backend-opus --squash
```

### View Reports
```bash
# List all reports
ls supervisor-reports/

# View latest report
cat supervisor-reports/report_*.md | tail -50
```

## 🧪 Testing Commands

### Run All Tests
```bash
npm test
```

### Run Tests by Type
```bash
# Unit tests only
npm test -- tests/unit

# Integration tests only
npm test -- tests/integration

# Single test file
npm test -- tests/unit/ingestor.spec.ts

# Watch mode
npm run test:watch

# With coverage
npm run test:coverage
```

### Backend-Specific Tests
```bash
cd backend
npm test
npm run test:coverage
```

### Frontend-Specific Tests
```bash
cd frontend
npm test
npm run test:e2e  # If E2E tests exist
```

## 🔧 Development Commands

### Code Quality
```bash
# Run linter
npm run lint

# Fix linting issues
npm run lint:fix

# Type checking
npm run typecheck

# Format code
npm run format

# Check formatting
npm run format:check

# Full validation
npm run validate
```

### Backend Development
```bash
cd backend

# Build TypeScript
npm run build

# Run in development mode
npm run dev

# Run CLI directly
npm run cli -- --input ~/Documents/Papers --once

# Watch specific directory
npm run cli -- --watch --input ./papers --output ./summaries.md
```

### Frontend Development
```bash
cd frontend

# Start development server
npm run dev
# Access at: http://localhost:3000

# Build for production
npm run build

# Start production server
npm run start

# Analyze bundle size
npm run analyze  # If configured
```

## 🌿 Git Workflow

### Agent Branching
```bash
# Check current branch
git branch --show-current

# Switch to agent branch
git checkout backend-opus
git checkout frontend-opus
git checkout test-opus

# Return to main
git checkout main
```

### View Agent Work
```bash
# See all branches
git branch -a

# View branch differences
git diff main..backend-opus

# View branch commits
git log main..frontend-opus --oneline

# Visualize branch structure
git log --graph --oneline --all --decorate
```

### Commit Message Format
```bash
# Backend agent commits
git commit -m "[backend-opus] feat: add user authentication"
git commit -m "[backend-opus] fix: handle null in PDF parser"

# Frontend agent commits
git commit -m "[frontend-opus] feat: create insight cards"
git commit -m "[frontend-opus] style: update dark mode theme"

# Test agent commits
git commit -m "[test-opus] test: add auth integration tests"
git commit -m "[test-opus] fix: stabilize flaky test"
```

## 📁 Project Structure

```bash
# Key directories
backend/          # Backend service code
frontend/         # Next.js frontend
tests/            # All test files
docs/             # Documentation
  mission-briefs/ # Agent instructions
  tickets/        # Feature requests
  schema/         # JSON schemas
scripts/          # Utility scripts
  supervisor.py   # Agent coordinator

# Configuration files
.eslintrc.json    # Linting rules
.prettierrc       # Code formatting
jest.config.js    # Test configuration
tsconfig.json     # TypeScript config
docker-compose.yml # Docker setup
```

## 🎯 Common Workflows

### Adding a New Feature
```bash
# 1. Create feature ticket
echo "# Feature: User Authentication
## Acceptance Criteria
- [ ] Login endpoint
- [ ] JWT tokens
- [ ] React login form
- [ ] Unit tests
" > docs/tickets/auth-feature.md

# 2. Share with agents (paste to each agent terminal)

# 3. Monitor progress
npm run supervisor

# 4. Merge when ready
npm run supervisor:merge backend-opus
npm run supervisor:merge frontend-opus
npm run supervisor:merge test-opus
```

### Debugging Failed Tests
```bash
# 1. Check which tests fail
npm test

# 2. Run specific failing test
npm test -- --testNamePattern="should process PDF"

# 3. Debug with more output
npm test -- --verbose --no-coverage

# 4. Check test logs
cat test-results.log  # If configured
```

### Updating Dependencies
```bash
# Check for outdated packages
npm outdated

# Update dependencies
npm update

# Audit for vulnerabilities
npm audit

# Fix vulnerabilities
npm audit fix
```

## 🐛 Troubleshooting

### Common Issues

#### "Command not found: claude-code"
```bash
# Install Claude Code CLI first
# See: https://claude.ai/code
```

#### "npm: command not found"
```bash
# Install Node.js from nodejs.org
# Or use nvm: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

#### Permission Denied Errors
```bash
# Fix script permissions
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

#### Merge Conflicts
```bash
# Let supervisor detect them
npm run supervisor

# Ask conflicting agent to resolve
# Paste conflict details to agent terminal
```

#### Test Failures
```bash
# Clean test environment
rm -rf tests/temp/*
npm test -- --clearCache

# Run with fresh install
rm -rf node_modules package-lock.json
npm install
npm test
```

## 📊 Environment Variables

### Required
```bash
OPENAI_API_KEY=sk-...          # For LLM summarization
```

### Optional
```bash
DAILY_TOKEN_BUDGET=200000       # LLM token limit
REACT_APP_API_URL=http://localhost:3001  # API endpoint
NODE_ENV=production             # Environment mode
LOG_LEVEL=debug                 # Logging verbosity
```

### Setting Variables
```bash
# Temporary (current session)
export OPENAI_API_KEY="your-key"

# Permanent (.bashrc/.zshrc)
echo 'export OPENAI_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc

# Using .env file
echo "OPENAI_API_KEY=your-key" > .env
```

## 🚢 Docker Commands

### Build and Run
```bash
# Build image
docker build -t parallel-ai-agents .

# Run container
docker run -p 3000:3000 parallel-ai-agents

# Using docker-compose
docker-compose up

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📈 Performance Monitoring

### Check Token Usage
```bash
# View today's usage
cat /tmp/llm_usage.json

# In supervisor report
npm run supervisor | grep "LLM tokens"
```

### Test Performance
```bash
# Measure test execution time
time npm test

# Profile backend performance
cd backend
npm run profile  # If configured

# Check bundle size
cd frontend
npm run build
ls -la .next/static/chunks
```

## 🔑 Quick Tips

1. **Always run tests before merging**
   ```bash
   npm test && npm run supervisor:merge branch-name
   ```

2. **Keep agents informed**
   - Share error messages
   - Provide context from other agents
   - Use clear, specific requests

3. **Monitor regularly**
   ```bash
   watch -n 30 npm run supervisor  # Auto-refresh every 30s
   ```

4. **Clean working directory**
   ```bash
   git clean -fd  # Remove untracked files
   git checkout .  # Reset changes
   ```

5. **Quick validation**
   ```bash
   npm run validate  # Lint + Type check + Tests
   ```

## 🆘 Getting Help

### Documentation
- Project: `README.md`, `QUICKSTART.md`
- Architecture: `TECHNICAL_DEEP_DIVE.md`
- Testing: `TESTING_GUIDE.md`
- Agent guides: `docs/mission-briefs/*.md`

### Debug Information
```bash
# System info
node --version
npm --version
python3 --version
git --version

# Project status
npm ls  # Check dependencies
git status  # Check Git state
npm test  # Verify tests
```

### Support
- GitHub Issues: [Report problems](https://github.com/EARTHTOEDWARD/parallel-ai-agents/issues)
- Review docs in `docs/` directory
- Check supervisor reports for agent status