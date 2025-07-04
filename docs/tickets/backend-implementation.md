### Mission Brief – Research Paper Ingestor (Backend)

ROLE & OWNERSHIP

- Owns `/backend/**` and database/migration files.
- Sole authority to read from the local file system and write to the data store.

DEFINITION OF DONE

1. Running `npm run ingest -- --once` ingests every PDF/TXT under `~/Desktop/Research Papers/TEMP/`.
2. Running `npm run ingest -- --watch` keeps watching the folder and ingests new files in < 60 s.
3. For each paper it appends a _front-matter block_ to `docs/research-insights.md`:

```md
## <paper-title> <!-- slug -->

- **Authors:** <comma-sep>
- **Source:** <file name or DOI>
- **Key insights:** <bulleted list of ≤ 5 items>
```

4. All side-effects are wrapped in `try/compactError()` so that test agent can assert failures (Factor 9).
5. Passing unit tests (`npm test`) and lint (`npm run lint`).

EXTERNAL CONTRACTS

```ts
type PaperMeta = {
  title: string;
  authors: string[];
  source: string; // file path or DOI
};
type InsightSummary = {
  meta: PaperMeta;
  insights: string[]; // ≤ 5 bullet strings
};
```

IMPLEMENTATION NOTES

- Use **Node 18 + TypeScript**.
- PDF parsing: `pdf-parse` or `pdfjs-dist`.
- Summarisation: call `summariseLLM(text, meta): Promise<InsightSummary>`; the test agent will stub this.
- File watching: `chokidar`.
- State: append to `docs/research-insights.md`; no database needed for v0.

GIT COMMIT PREFIX
`[backend-opus] feat|fix|refactor: …`

Begin with:

1. `npm init -y && npm add pdf-parse chokidar` (if absent)
2. Scaffold `/backend/ingestor.ts`, CLI wrapper in `/backend/cli.ts`, and update package.json scripts.
