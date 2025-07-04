# Minimal Mission Example

This demonstrates the parallel agent workflow with a simple chain:
1. `poem.ts` - Returns a hardcoded limerick
2. `sentiment.ts` - Analyzes sentiment (mocked)
3. `summary.ts` - Chains both and outputs JSON

## Running the Example

```bash
# Install ts-node if not present
npm install -g ts-node

# Run the summary
ts-node summary.ts
```

## Expected Output

```json
{
  "summary": {
    "poem": "There once was a coder named Ray...",
    "analysis": {
      "sentimentScore": 0.8,
      "sentimentLabel": "positive",
      "wordCount": 28,
      "lineCount": 5
    },
    "metadata": {
      "timestamp": "2024-01-04T...",
      "version": "1.0.0"
    }
  }
}
```

This minimal example shows how agents can create modular, testable components that chain together.