# Agent instructions (Codex, Cursor, Gemini CLI, Claude Code, any agent)

This repo is an AI job-search workflow. When asked to search for jobs, apply, prefill applications,
or run the nightly job search:

1. Read `skills/job-apply/SKILL.md` — the rules — and `skills/job-apply/profile.md` — the candidate's facts.
   The skill is authoritative on what may be claimed, screening and form answers.
2. For a nightly search, follow `prompts/nightly-job-search.md`. For filling forms, follow
   `prompts/prefill-applications.md`.
3. If you don't have Google Drive or the Claude Apply Board: save resumes to `./out/` and use
   `tracker/applications.csv` (append rows only; never edit rows marked `applied`/`skipped`).
4. Scripts: `python3 -I scripts/india-roles-filter.py [--new]` for leads; `python3 scripts/resume-builder.py`
   for one-page PDFs (needs `pdflatex`, `pdfinfo`).

Non-negotiable: never fabricate anything not in `profile.md`; never click Submit; never attach a
placeholder file; never automate LinkedIn or send messages/emails on the user's behalf; check for a
prior application before filling a form.
