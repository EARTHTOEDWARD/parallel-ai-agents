# Testing Guide for Non-Coders

This guide will help you test if the parallel-ai-agents framework actually works.

## The Simplest Test (What We Already Did)

Good news! We already ran one test and it passed:

```bash
cd /Users/edward/Coding\ Agents/parallel-ai-agents/tests
npm test unit/ingestor.spec.ts
```

This tested that the code can process text files and extract paper information. It worked!

## Testing the Whole System

Here's how to test if the research paper summarizer actually works:

### 1. Start the Backend (Paper Processor)

Open a terminal in VS Code and run:

```bash
cd /Users/edward/Coding\ Agents/parallel-ai-agents/backend
npm run dev
```

This watches for PDF/text files in the `papers/` folder.

### 2. Add a Test Paper

Create a simple text file to test with:

```bash
cd /Users/edward/Coding\ Agents/parallel-ai-agents
mkdir -p papers
echo "Test Paper About AI
by John Doe

This paper discusses artificial intelligence." > papers/test.txt
```

### 3. Check if It Worked

Look for a file called `research-insights.md` in the docs folder:

```bash
cat docs/research-insights.md
```

If you see your test paper summarized there, it's working!

### 4. Start the Frontend (Optional)

In another terminal:

```bash
cd /Users/edward/Coding\ Agents/parallel-ai-agents/frontend
npm run dev
```

Then open http://localhost:3000 in your browser.

## What Success Looks Like

- ✅ Backend processes your test.txt file
- ✅ Creates/updates docs/research-insights.md
- ✅ Frontend shows the paper summary at http://localhost:3000

## If Things Go Wrong

Common issues and fixes:

**"command not found: npm"**

- You need Node.js installed. Download from https://nodejs.org/

**"OPENAI_API_KEY not set"**

- The LLM features need an API key:
  ```bash
  export OPENAI_API_KEY="your-key-here"
  ```

**"Port 3000 already in use"**

- Something else is using that port. The frontend will suggest another port.

## The Docker Way (Advanced)

If the above doesn't work, try Docker:

```bash
cd /Users/edward/Coding\ Agents/parallel-ai-agents
docker-compose up
```

This starts everything in containers (whatever those are).

## Getting Help

If nothing works:

1. Copy any error messages
2. Ask Claude Code: "This error happened when I tried to test the parallel-ai-agents project: [paste error]"
3. Or create an issue on GitHub (Claude Code can help with that too!)

Remember: Not knowing how to test something is perfectly normal. Even experienced developers sometimes struggle with setup!
