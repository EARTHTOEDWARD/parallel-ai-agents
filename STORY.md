# **How I Built a Multi-Agent Development Framework in Two Hours (As a Non-Coder)**

I'm not a coder, let alone a developer. I can't read bash scripts, and dependency management sounds like an addiction problem, not a coding thing. And even more important, I don't want to learn. But as a non coder, a few days ago I found the promised land which is to have a really smart agent work within an IDE; I got Claude Code (which uses Opus 4) to work inside VScode. This was transformative. It felt like moving from the stone age to the modern world. Now finally projects I've been working and failing at for months have begun to take shape properly. But there were still serious failures and it could take CC hours of work to maybe make them worse. I needed a better way. Enter youtube. This morning I watched a couple of YouTube videos. The first explained "12-Factor Agents"—a structured approach to building reliable LLM systems with clear ownership, focused responsibilities, and proper guardrails. The second was a demo by Zen van Riel showing three different AI coding assistants working simultaneously in VS Code terminals. This was the first example of multiple agent architecture that I sort of could distantly get a feel for. But I didn't like that it mixed agents. I don't want lesser models involved at all. Ideally i'd have ChatGPT o3 Pro doing all the coding, with a few calls to o3 and maybe checks by Opus 4. But I heard that Gemini command line wasn't so good, so just for the sake of sanity, I just want to use Opus 4 for all three agents instead of mixing different models.

## **The Process**

I started by transcribing the 3 Agent video and feeding the text to ChatGPT o3 Pro along with documentation from the 12-Factor GitHub repository. ButI asked for a hybrid plan that combined the best ideas from both approaches while upgrading to Claude Opus 4 throughout.

The result was surprisingly comprehensive: three dedicated Git branches (backend-opus, frontend-opus, test-opus), each with clear mission statements and responsibilities. o3 Pro also suggested a supervisor script, CI pipeline integration, and structured Git commit formatting.

I copied this plan into Claude Code and watched it start building the basic structure—creating directories, installing dependencies, and writing initial tests. While that was running, I opened another ChatGPT tab (regular o3 this time) and asked what was missing from a production standpoint.

The response highlighted several critical gaps: Docker containerization, JSON schema validation, token budget monitoring, and better CI integration. I took these suggestions back to o3 Pro for implementation details, (asking it to implement what it thinks makes sense) then distributed the resulting code to my original CC agent, who made the changes.

## **What Got Built**

Over the course of about two hours, this back-and-forth process produced:

- **Docker containerization**: Multi-stage Dockerfile and compose stack for consistent environments
- **Schema validation**: GitHub Actions that validate all JSON artifacts against defined schemas
- **Budget controls**: Token monitoring wrapper that prevents runaway costs
- **Comprehensive supervision**: Daily usage reporting alongside test results
- **Idempotent setup**: Scripts that work reliably on repeated runs
- **Working demo**: End-to-end pipeline with Jupyter notebook examples
- **CI badges**: Automated testing and validation indicators

The only manual Git work I had to do was merging the branches, but I don't understand that either, so I showed CC a screenshot of the github page and it handled the mechanics the GitHub's merge.

## **Key Insights**

What surprised me wasn't just that this worked, but how natural the process felt. I never had to learn Docker syntax or figure out GitHub Actions configuration. Instead, I focused on understanding what needed to be built and coordinating between different AI systems to get it done.

The 12-Factor principles proved essential—not just for the final architecture, but for managing the development process itself. Having clear ownership boundaries meant I could assign different pieces to different agents without conflicts or confusion.

## **For Other Non-Coders**

If you're in a similar position—curious about building things but intimidated by the technical complexity—this approach might work for you too. The key elements were:

1. **Clear requirements**: Taking time to understand what I actually wanted to build.
2. **Good examples**: Starting with proven architectural patterns rather than inventing from scratch
3. **Iterative improvement**: Building something basic first, then identifying and fixing gaps
4. **Tool coordination**: Using each AI system for what it does best rather than trying to do everything in one place

The result is a production-ready framework _(whatever that means, this story is written by an AI, not me!)_ that I genuinely understand at a systems level _(not true, the actual human doesn't understand this at system level or even what system level means),_ even though I didn't write the implementation details myself. Sometimes the most valuable skill isn't coding—it's knowing what questions to ask and how to coordinate the answers _(you can tell this was written by Claude Opus 4 because of the sermonising wrap up last sentence!)_.
