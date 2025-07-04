import { sentiment } from "./sentiment";

const result = sentiment();
const summary = {
  summary: {
    poem: result.text,
    analysis: {
      sentimentScore: result.score,
      sentimentLabel: result.sentiment,
      wordCount: result.text.split(/\s+/).length,
      lineCount: result.text.split('\n').length
    },
    metadata: {
      timestamp: new Date().toISOString(),
      version: "1.0.0"
    }
  }
};

console.log(JSON.stringify(summary, null, 2));