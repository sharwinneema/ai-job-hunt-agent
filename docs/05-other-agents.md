# 5. Using this with Codex, Cursor, Gemini CLI or any agent

The workflow is plain markdown + two Python scripts, so any agent that can read files, run a shell,
search the web and (optionally) drive a browser can run it.

| Piece | Claude | Codex / other agents |
|---|---|---|
| Instructions | `skills/job-apply/SKILL.md` (uploaded as a skill) | `AGENTS.md` at repo root points the agent to the same files |
| Profile | `skills/job-apply/profile.md` | same file |
| Gmail / Drive | built-in connectors | an MCP server for Gmail/Drive, or export alert emails manually; save resumes to a local `out/` folder instead of Drive |
| Tracker | Apply Board artifact | `tracker/applications.csv` |
| Browser form fill | Claude in Chrome | Playwright MCP / Chrome DevTools MCP / your agent's browser tool — same rules: never submit, never attach files, read fields back |
| Schedule | Claude scheduled tasks | cron / launchd / Task Scheduler running the agent's headless mode |

## Codex quick start
```bash
git clone https://github.com/sharwinneema/ai-job-hunt-agent && cd ai-job-hunt-agent
# fill skills/job-apply/profile.md and the data blocks in scripts/resume-builder.py
codex   # then: "Run prompts/nightly-job-search.md, using tracker/applications.csv
        #        as the tracker and ./out for resumes instead of Drive"
```

## Claude Code quick start
```bash
mkdir -p ~/.claude/skills && cp -r skills/job-apply ~/.claude/skills/
claude   # then: "use the job-apply skill to run prompts/nightly-job-search.md"
```

Adapting a prompt: replace the Drive and Apply Board steps with "write to ./out" and "append to
tracker/applications.csv". Everything else (sourcing, screening, tailoring rules, referral kit,
no-submit) stays the same.
