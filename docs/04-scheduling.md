# 4. Scheduling the two tasks

## On Claude (what the original setup uses)

Create two **scheduled tasks** (claude.ai / desktop app → Scheduled tasks → New, or just ask Claude:
*"Create a scheduled task from prompts/nightly-job-search.md"*).

| Task | Schedule | Require this computer | Folder | Connectors | Model |
|---|---|---|---|---|---|
| **Nightly job search** | Daily, e.g. 01:42 local (`CRON_TZ=Asia/Calcutta 42 1 * * *`) | **Off** — cloud only, your laptop can sleep | none | Gmail, Google Drive | a strong model (Opus-class) |
| **Prefill my applications** | None — press **Run now** when you're at your desk | **On** | your resumes folder | Gmail, Google Drive, Claude in Chrome | any capable model |

Tips
- Set approvals to **Automatically approve** (task settings) so the nightly run doesn't stop for a click.
- Turn on **push notifications** so the morning report reaches your phone.
- Add the `job-apply` skill first: claude.ai → Settings → Capabilities → Skills → Upload
  (zip the `skills/job-apply/` folder — it must contain `SKILL.md` and your filled `profile.md`).

## The daily loop

```
01:42  Nightly (cloud)  Gmail alerts + dataset + ATS boards → verify → tailor PDFs → Drive
                        → Apply Board rows → referral kits → queue file → report
08:00  You              Open Apply Board, read report, send referral messages yourself
any    Prefill (local)  Gmail "already applied?" → copy PDFs Drive→~/Documents/resumes
                        → open each form in Chrome → fill all fields → leave tabs open
       You              Attach PDF, review, Submit, press "Mark applied"
```

## Without Claude scheduled tasks
- **Codex / other CLI agents:** run the prompt with cron, e.g.
  `42 1 * * * cd ~/ai-job-hunt-agent && codex exec "$(cat prompts/nightly-job-search.md)"`
  (or your agent's non-interactive mode). See `05-other-agents.md`.
- **GitHub Actions:** possible for the search half (scripts + an API-driven agent), but Gmail/Drive
  access needs your own OAuth credentials stored as repo secrets — never commit them.
