# Apply Board (the tracker)

The Apply Board is the page you open every morning: one card per verified role, best fit first,
with the resume filename to attach, an "Open application" button, and **Mark applied / Skip**
buttons. The nightly task writes rows; you mark them.

## Option A — Claude artifact with a database (what the original setup uses)

1. In a Claude chat, say: *"Publish `apply-board/index.html` from this repo as an artifact and give
   it a database with a collection `roles` and a document `profile/answers`."* (Upload the file or
   paste it.)
2. Copy the artifact's URL (looks like `https://claude.ai/artifact/XXXX`) into both prompts where it
   says `{{APPLY_BOARD_URL}}`.
3. Optional: ask Claude to write your standard answers to `profile/answers` as
   `{ "items": [ {"k": "Current CTC", "v": "..."}, {"k": "Notice period", "v": "..."} ] }` — they
   show as a copy-paste sheet at the bottom of the board.

The tasks read/write it with Claude's artifact-data tool (`list`, `set`, `update`, `batch`).

## Option B — any other agent (Codex, Cursor, Gemini CLI, a plain script)

Use `tracker/applications.csv` (same fields, one row per role). Rules are identical: append rows,
never delete, never change a row whose status is `applied` or `skipped`. You could also use a Google
Sheet, Notion database or Airtable — just keep the field names.

## Row schema — collection `roles`

doc id: `<YYYY-MM-DD>-<company>-<role>` (lowercase, hyphens)

| field | type | example |
|---|---|---|
| company | string | `Acme AI` |
| role | string | `Software Engineer II, Agents` |
| location | string | `Bengaluru` |
| mode | string | `Hybrid` |
| ats | string | `Ashby` |
| applyUrl | https URL | employer's application page |
| jdUrl | https URL | job description |
| years | string | `2-4 years` |
| comp | string | `Not stated` or the stated band |
| compStated | bool | `false` |
| payCut | bool | `false` |
| resumeFile | string | `Jane_Doe_AcmeAI_SDE2_Agents.pdf` |
| resumeUrl | https URL | Drive view link |
| fit | string | 1–2 sentences on why it fits |
| flags | string[] | `["Comp not stated — ask in recruiter screen"]` |
| queuedOn | `YYYY-MM-DD` | `2026-11-25` |
| rank | int | `1` = best tonight |
| status | `queued` \| `applied` \| `skipped` | `queued` |
| linkedinJobUrl | https URL (optional) | |
| answers | `[{q, a}]` (optional) | custom screening Q&A |
| statusOn | `YYYY-MM-DD` (set by the buttons) | |
