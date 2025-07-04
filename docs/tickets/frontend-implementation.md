### Mission Brief – Insights Viewer (Frontend)

ROLE & OWNERSHIP

- Owns `/frontend/**`; must **not** touch backend code.
- Provides a minimal UI to view `docs/research-insights.md`.

DEFINITION OF DONE

1. Run `npm run dev` → localhost:3000 shows a list of papers and their bullet-point insights.
2. UI auto-reloads when the markdown file is updated (poll every 30 s or subscribe to websocket if available).
3. All lint + unit tests pass.

CONTRACT WITH BACKEND

- Reads `http://localhost:3000/api/insights` which returns

```json
InsightSummary[]
```

- If the API 404s, fall back to parsing the markdown file directly (SSR).

IMPLEMENTATION NOTES

- Use the existing Next.js scaffold (if present). Otherwise, create `vite + React`.
- Styling: plain CSS modules.
- No auth, routing, or edit functionality.

GIT COMMIT PREFIX
`[frontend-opus] feat|fix|refactor: …`

First task: create the read-only `/api/insights` route that reads `docs/research-insights.md` and returns JSON.
