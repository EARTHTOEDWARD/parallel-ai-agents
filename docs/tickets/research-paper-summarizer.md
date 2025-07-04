# Research Paper Summarizer Feature

## Overview

Build a system that watches a folder for research papers (PDFs/text files), automatically summarizes them using an LLM, and provides a web interface to view the summaries.

## Technical Requirements

### Backend

- Watch folder: `~/Desktop/Research Papers/TEMP/`
- Support PDF and TXT file formats
- Extract metadata (title, authors)
- Generate 5 key insights per paper
- Append summaries to `docs/research-insights.md`
- CLI with --watch and --once modes

### Frontend

- Display list of summarized papers
- Show metadata and key insights
- Auto-refresh when new papers are processed
- Fallback to reading markdown directly if API unavailable

### Testing

- Unit tests for file processing
- Mock LLM calls for offline testing
- Integration tests for API endpoints
- 80% code coverage requirement

## Success Criteria

- ✅ Papers are automatically processed when added to watch folder
- ✅ Summaries are persisted in markdown format
- ✅ Web UI displays all summaries
- ✅ All tests pass with >80% coverage
- ✅ No linting errors
- ✅ CI pipeline is green
