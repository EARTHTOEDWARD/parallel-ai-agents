# Quick Start Guide - Parallel AI Agents

## Prerequisites

- Claude Code CLI installed
- Node.js 18+ and npm
- Python 3.8+ (for supervisor)
- Git
- GitHub CLI (optional, for PR creation)

## Initial Setup

1. **Clone and setup the project:**

   ```bash
   cd parallel-ai-agents
   npm install
   npm run setup
   ```

2. **Open VS Code workspace:**
   ```bash
   code .vscode/parallel-agents.code-workspace
   ```

## Running the Agents

### Option 1: Individual Terminals

Open 3 terminals and run:

```bash
# Terminal 1 - Backend Agent
npm run agent:backend

# Terminal 2 - Frontend Agent
npm run agent:frontend

# Terminal 3 - Test Agent
npm run agent:test
```

### Option 2: All at Once (requires concurrently)

```bash
npm install -g concurrently
npm run agents:all
```

### Option 3: VS Code Tasks

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Tasks: Run Task"
3. Select "Launch All Agents"

## Monitoring Progress

In a separate terminal:

```bash
# Monitor agent status
npm run supervisor

# Monitor and create PRs for ready branches
npm run supervisor:prs

# Merge a specific branch
npm run supervisor:merge backend-opus
```

## Workflow Example

1. **Create a feature ticket:**

   ```bash
   echo "# Feature: User Authentication

   ## Acceptance Criteria
   - [ ] POST /api/auth/login endpoint
   - [ ] JWT token generation
   - [ ] Password hashing with bcrypt
   - [ ] Login form component
   - [ ] Auth context for React
   - [ ] Unit tests for auth logic
   - [ ] Integration tests for API
   - [ ] E2E test for login flow
   " > docs/tickets/auth-feature.md
   ```

2. **Feed ticket to agents:**
   - Paste ticket content to each agent with their specific tasks
   - Agents work in parallel on their branches

3. **Monitor progress:**

   ```bash
   npm run supervisor
   ```

4. **Review and merge:**
   - Check supervisor report
   - When tests pass, merge to main
   - Or create PRs for review

## Tips for Non-Coders

### Understanding Agent Status

- ✅ Green checks = Good to go
- ❌ Red X = Needs attention
- Look for "Ready to merge" in supervisor reports

### Common Commands

```bash
# See what changed
git status

# Switch branches
git checkout backend-opus
git checkout main

# View agent work visually
git log --graph --oneline --all
```

### When Things Break

1. Check the supervisor report for specific errors
2. Paste error to the relevant agent
3. Tell agent: "Fix this error: [error message]"

### Best Practices

- Start with small features
- One feature at a time
- Let tests guide quality
- Trust the supervisor reports
- Merge only when all tests pass

## Troubleshooting

**"Command not found: claude-code"**

- Install Claude Code CLI first

**"npm: command not found"**

- Install Node.js from nodejs.org

**"Permission denied"**

- Run: `chmod +x scripts/*.sh`

**Merge conflicts**

- Let supervisor detect them
- Ask the conflicting agent to resolve

## Next Steps

1. Read mission briefs to understand agent roles
2. Create your first ticket
3. Watch agents collaborate
4. Celebrate automated development! 🎉
