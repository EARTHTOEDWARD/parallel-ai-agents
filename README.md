# Parallel AI Agent Development Framework

![CI](https://github.com/EARTHTOEDWARD/parallel-ai-agents/actions/workflows/ci.yml/badge.svg)
![Schema Validation](https://github.com/EARTHTOEDWARD/parallel-ai-agents/actions/workflows/validate-schema.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A hybrid workflow combining Parallel AI Agent architecture with 12-Factor Agent principles for reliable, scalable AI-assisted development.

> 📖 **Read the story behind this project**: [How I Built a Multi-Agent Development Framework in Two Hours (As a Non-Coder)](./STORY.md) - Learn how this framework was created by a non-coder using AI agents to coordinate development.
>
> 🧪 **New to testing?** Check out the [Testing Guide for Non-Coders](./TESTING_GUIDE.md) for simple steps to verify everything works.

🔗 **GitHub Repository**: [github.com/EARTHTOEDWARD/parallel-ai-agents](https://github.com/EARTHTOEDWARD/parallel-ai-agents)

## What Was Built: Research Paper Summarizer

The three AI agents successfully implemented a **Research Paper Summarizer** as a demonstration:

- **Backend**: Watches a folder for PDF/text papers, extracts content, and uses OpenAI to generate key insights
- **Frontend**: Next.js web interface that displays paper summaries with auto-refresh
- **Tests**: Unit and integration tests to ensure everything works correctly

This serves as a working example of how the parallel agent framework operates in practice.

## Architecture Overview

This project uses three specialized Claude Opus 4 agents working in parallel:

- **Backend Agent**: Owns `/backend` directory and API development
- **Frontend Agent**: Owns `/frontend` directory and UI development
- **Test Agent**: Owns `/tests` directory and quality assurance

Each agent operates on its own Git branch to prevent conflicts, with automated CI/CD ensuring code quality.

## Project Structure

```
parallel-ai-agents/
├── .git
├── .github/workflows/    # CI/CD pipelines
├── docs/                 # Architecture & agent briefs
│   ├── mission-briefs/   # Agent-specific instructions
│   └── tickets/          # Feature requests
├── backend/              # Backend API (backend-opus branch)
├── frontend/             # Frontend UI (frontend-opus branch)
├── tests/                # Test suites (test-opus branch)
└── infra/                # Infrastructure config
```

## Quick Start

1. **Setup branches for each agent:**

   ```bash
   git checkout -b backend-opus
   git checkout -b frontend-opus
   git checkout -b test-opus
   git checkout main
   ```

2. **Launch agents in separate VS Code terminals:**

   ```bash
   # Terminal 1
   claude-code --role backend --watch backend/ docs/mission-briefs/backend.md

   # Terminal 2
   claude-code --role frontend --watch frontend/ docs/mission-briefs/frontend.md

   # Terminal 3
   claude-code --role tests --watch tests/ docs/mission-briefs/tests.md
   ```

3. **Run the supervisor to manage outputs:**
   ```bash
   python scripts/supervisor.py
   ```

## Key Principles (12-Factor Agents)

1. **Small, focused agents**: Each agent owns specific paths
2. **Structured outputs**: All communication via JSON schemas
3. **Test-driven**: Definition of Done = passing tests
4. **Compact errors**: Errors condensed for supervisor handling
5. **Git as shared memory**: Branches prevent conflicts

## Development Workflow

1. Write mission briefs defining agent responsibilities
2. Create tickets with acceptance criteria
3. Launch agents to work in parallel
4. Supervisor collates results and manages merges
5. CI/CD ensures quality gates are met

## Configuration

- Pre-commit hooks: `.husky/` and `.lintstagedrc`
- CI pipeline: `.github/workflows/ci.yml`
- Agent prompts: `docs/prompts/`
- VS Code workspace: `.vscode/parallel-agents.code-workspace`
