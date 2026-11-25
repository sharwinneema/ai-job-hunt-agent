# Contributing

Contributions are very welcome — especially:

- **ATS quirks** (new form-filling gotchas like the Ashby React-input one) → add to `skills/job-apply/SKILL.md` under "Filling forms".
- **Sources** that render from the cloud, or careers pages that don't → "When searching rather than applying".
- **Filters for other countries** → `scripts/<country>-roles-filter.py` (copy `india-roles-filter.py`, change the `IN` regex).
- **Adapters** for other agents (Codex, Cursor, Gemini CLI), trackers (Notion, Airtable, Sheets), or browsers (Playwright MCP).
- **Resume templates** — keep them one page, ATS-readable, and driven by the same `V` dict.

## Ground rules
1. **Never commit personal data.** No real phone numbers, emails, salaries, Drive IDs, artifact URLs or resumes. Use `{{PLACEHOLDERS}}` or the fictional "Jane Doe" example.
2. Keep the safety rules intact: no auto-submit, no fabricated claims, no LinkedIn automation, no sending messages on the user's behalf.
3. Test scripts before opening a PR (`python3 scripts/resume-builder.py` should produce a 1-page PDF).

## How
Fork → branch → change → PR with a one-paragraph "why". Issues for ideas and bug reports are great too.
