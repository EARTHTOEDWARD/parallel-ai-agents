### Mission Brief – QA & CI Guard-Rails (Tests)

ROLE & OWNERSHIP

- Owns `/tests/**`, CI config under `.github/workflows/**`, and `scripts/supervisor.py`.
- May stub functions but must never alter production source outside `tests/`.

DEFINITION OF DONE

1. **Unit tests**:
   - Drop `fixtures/sample.pdf` into a temp folder, run `npm run ingest -- --once`, assert that
     `docs/research-insights.md` contains a new block whose title matches the sample's title.
   - Mock `summariseLLM` so tests run offline.
2. **Integration tests** (optional but stretched goal):
   - Spin up the frontend dev server and assert that `GET /api/insights` returns ≥ 1 item.
3. Coverage ≥ 80 %, red CI fails the branch.

TEST STACK

- Jest + ts-jest.
- `supertest` for API endpoints.

COMPACT ERROR FORMAT

```json
{
  "error": "<short slug>",
  "detail": "<stack or reason>"
}
```

GIT COMMIT PREFIX
`[test-opus] test|infra: …`

First task: scaffold `tests/ingestor.spec.ts` with the unit test skeleton and install dev-deps.
