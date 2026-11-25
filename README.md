# 🤖 AI Job Hunt Agent

**An AI agent that searches for jobs while you sleep, checks each one is real, tailors a one-page
resume for every role, and fills in the application forms in your browser. You attach the resume
and click Submit.**

It was built and used day to day with Claude (scheduled tasks + skills + the Claude in Chrome
extension), and it is plain markdown + Python, so **Codex, Claude Code, Cursor or any agent** can run it.

---

## Contents
1. [How it works](#1-how-it-works)
2. [What's in this repo](#2-whats-in-this-repo)
3. [What you need](#3-what-you-need)
4. [Setup, step by step](#4-setup-step-by-step)
   - [4.1 Fill in your profile](#41-fill-in-your-profile)
   - [4.2 Set up the resume builder](#42-set-up-the-resume-builder)
   - [4.3 Connect Gmail and Google Drive](#43-connect-gmail-and-google-drive)
   - [4.4 Create the Drive folder](#44-create-the-job-queue-drive-folder)
   - [4.5 LinkedIn job alerts → Gmail](#45-linkedin-job-alerts--gmail)
   - [4.6 Install the Claude in Chrome extension](#46-install-the-claude-in-chrome-extension)
   - [4.7 Publish the Apply Board](#47-publish-the-apply-board)
   - [4.8 Add the skill](#48-add-the-skill)
   - [4.9 Create the two scheduled tasks](#49-create-the-two-scheduled-tasks)
5. [Your daily routine](#5-your-daily-routine)
6. [Using Codex or another agent](#6-using-codex-or-another-agent)
7. [Safety rules](#7-safety-rules)
8. [Privacy](#8-privacy)
9. [Troubleshooting](#9-troubleshooting)
10. [Contributing](#10-contributing) · [License](#license)

---

## 1. How it works

```
 01:42  NIGHTLY SEARCH  (cloud — your laptop can sleep)
        LinkedIn alert emails ─┐
        open-jobs dataset ─────┼─► open each role on the employer's OWN page ─► screen it
        Ashby/Greenhouse/Lever ┤      (still open? right location? years? stack? pay floor?)
        YC Work at a Startup ──┘
                     ▼
        tailored 1-page resume PDF per role ─► Google Drive (job-queue folder)
        row per role on the Apply Board ─► referral kit per role ─► queue file ─► report (push)

 Morning  YOU  read the report, send the referral messages yourself

 Any time PREFILL  (your computer — press "Run now")
        Gmail "already applied?" check ─► copy PDFs to ~/Documents/resumes
        ─► open every form in its own Chrome tab ─► fill every field ─► STOP

 YOU  attach the resume ─► review ─► Submit ─► press "Mark applied"
```

Two automated runs:

| | **Nightly job search** | **Prefill my applications** |
|---|---|---|
| When | Every night (e.g. 01:42) | Whenever you're at your computer ("Run now") |
| Where | Cloud only | Your computer + real Chrome |
| Does | Finds, verifies, ranks roles; builds resumes; fills the Apply Board; writes referral kits; checks inbox; drafts follow-ups | Checks Gmail for duplicates; copies resumes to your computer; fills every form field except the resume |
| Never | Submits, sends messages, logs in to LinkedIn | Clicks Submit, attaches files |

---

## 2. What's in this repo

| Path | What it is |
|---|---|
| `skills/job-apply/SKILL.md` | **The rules**: decide-alone answers, verification, screening, tailoring, "already applied" Gmail check, Ashby form fix, referral kit, safety rules |
| `skills/job-apply/profile.md` | **Your facts** (template). The only file you *must* fill in |
| `prompts/nightly-job-search.md` | Prompt for the nightly scheduled task |
| `prompts/prefill-applications.md` | Prompt for the run-when-free prefill task |
| `scripts/india-roles-filter.py` | Pulls ~38k jobs/day from the public [open-jobs-data](https://github.com/ConorsCode/open-jobs-data) set, keeps non-senior software roles in India. `--new` = only new since yesterday |
| `scripts/resume-builder.py` | LaTeX one-page resume builder; one `V` entry per tailored variant; auto-fits to 1 page |
| `apply-board/index.html` | The morning dashboard page (Claude artifact) |
| `apply-board/README.md` | Apply Board setup + row schema |
| `tracker/applications.csv` | Tracker for agents without the Apply Board |
| `docs/` | The same setup steps split into separate pages |
| `AGENTS.md`, `CLAUDE.md` | Entry points Codex / Claude Code / other agents load automatically |

---

## 3. What you need

- A **paid Claude plan** (Pro, Max, Team or Enterprise) — for scheduled tasks, skills and Claude in Chrome.
  *(Or another agent — see [section 6](#6-using-codex-or-another-agent).)*
- The **Claude desktop app** (Mac or Windows) — for the prefill run on your computer.
- **Google Chrome** on desktop.
- A **Google account** (Gmail + Drive) — the same one that gets your LinkedIn and job emails.
- A **LinkedIn** account (for job-alert emails only).
- About **30–45 minutes** for setup.

---

## 4. Setup, step by step

### 4.1 Fill in your profile
1. Fork or clone this repo:
   ```bash
   git clone https://github.com/sharwinneema/ai-job-hunt-agent && cd ai-job-hunt-agent
   ```
2. Copy the template so your real details stay out of git:
   ```bash
   cp skills/job-apply/profile.md skills/job-apply/profile.private.md
   ```
3. Fill **every** `{{...}}` in `profile.private.md`: contact details, education, experience (real
   bullets with real numbers), projects, skills, search preferences (years, locations, current pay,
   pay floor, target band, best-fit roles, stacks you lack), standard form answers.
4. When you upload the skill (4.8), rename it to `profile.md` inside the uploaded copy.

> **Rule:** the agent will only ever claim what is in this file. If it's missing here, it won't
> appear on a resume or a form.

### 4.2 Set up the resume builder
1. Install LaTeX + poppler to test locally (the cloud run already has them):
   - Mac: `brew install --cask mactex-no-gui && brew install poppler`
   - Ubuntu: `sudo apt install texlive-latex-extra poppler-utils`
2. Open `scripts/resume-builder.py` and replace the "Jane Doe" sample data at the top: `CONTACT`,
   `JOB`, `PREV`, `EDU`, the bullet bank `B`, projects `P`, skills `S`. Use your real facts only.
3. Test it: `python3 scripts/resume-builder.py` → a one-page PDF. The agent adds one `V` entry per job.
4. In LaTeX, write `\%` for %, `\&` for &, `---` for an em dash.

### 4.3 Connect Gmail and Google Drive
1. claude.ai or the desktop app → **Settings → Connectors**.
2. Connect **Gmail** and **Google Drive** with the Google account that gets your job emails.

Only these connectors are needed:

| Connector | Used for |
|---|---|
| Gmail | Read LinkedIn alerts, detect "already applied" emails, spot recruiter replies, save follow-up **drafts** |
| Google Drive | Scripts, resume PDFs, nightly queue file |
| Claude artifacts (built in) | The Apply Board |
| Claude in Chrome | Filling forms (prefill only) |

### 4.4 Create the `job-queue` Drive folder
1. In Google Drive, create a folder named **`job-queue`**.
2. Upload `scripts/india-roles-filter.py` and your edited `scripts/resume-builder.py`.
3. Create an empty text file **`company-slugs.md`**. The nightly run keeps it updated with the job
   boards it has checked and the companies to try next.
4. Copy the IDs:
   - Folder ID: open the folder; the URL ends in `/folders/<FOLDER_ID>`.
   - File ID: right-click the file → *Share → Copy link*; the ID sits between `/d/` and `/view`.

### 4.5 LinkedIn job alerts → Gmail
The agent **reads alert emails only**. It never logs in to LinkedIn and never automates it.
1. linkedin.com → **Jobs** → search a role + location (e.g. `Software Engineer II` · `Bengaluru`).
2. Filters: **Date posted → Past 24 hours**, **Experience level**, Remote/Hybrid if you want.
3. Turn on the **job alert toggle** on the results page.
4. **Manage alerts** → **Daily**, notify by **Email**.
5. Repeat for each search (up to 20 alerts): Software / Backend / AI / Full-stack engineer × your cities.
   For a target company: its LinkedIn page → **Jobs → Create job alert**.
6. Make sure LinkedIn emails go to the Gmail you connected (LinkedIn → Settings → Sign in & security
   → Email addresses → set it as primary). Don't auto-delete these emails.
7. Test: ask Claude *"Search my Gmail for LinkedIn job alert emails from the last 2 days and list
   company, title and link."*

### 4.6 Install the Claude in Chrome extension
1. Chrome Web Store → **Claude** by Anthropic →
   https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn → **Add to Chrome**.
2. Sign in with your Claude account. Pin it (puzzle icon → thumbtack).
3. Desktop app → your initials → **Settings → Connectors → Claude in Chrome → Configure → On**.
4. Settings → **Preferred browser → Claude in Chrome**.
5. The first time it fills a job site, allow it: `jobs.ashbyhq.com`, `job-boards.greenhouse.io`,
   `jobs.lever.co`, `*.myworkdayjobs.com`, etc.
6. Read Anthropic's "Use Claude in Chrome safely" guide in the Claude Help Center.

Without the extension, the prefill run uses the desktop app's built-in browser. **Closing that
panel loses the filled form**, so attach and submit right away.

### 4.7 Publish the Apply Board
1. In a Claude chat, upload `apply-board/index.html` and say:
   *"Publish this as an artifact with a database: collection `roles`, and document `profile/answers`."*
2. Copy the artifact link (`https://claude.ai/artifact/XXXX`).
3. Optional: *"Write my standard form answers to `profile/answers`"* → a copy-paste sheet at the bottom.
4. The row fields are listed in [`apply-board/README.md`](apply-board/README.md).

### 4.8 Add the skill
- **claude.ai / desktop:** zip the `skills/job-apply/` folder (with your filled `profile.md`) →
  **Settings → Capabilities → Skills → Upload**.
- **Claude Code:** `cp -r skills/job-apply ~/.claude/skills/`
- **Codex / others:** nothing to install. `AGENTS.md` points them to the skill.

### 4.9 Create the two scheduled tasks
1. Open `prompts/nightly-job-search.md` and `prompts/prefill-applications.md`.
2. Replace every placeholder:

   | Placeholder | Where to get it |
   |---|---|
   | `{{FULL_NAME}}`, `{{PRIMARY_EMAIL}}` | you |
   | `{{CURRENT_CTC}}`, `{{EXPECTED_CTC}}` | your `profile.md` |
   | `{{JOB_QUEUE_FOLDER_ID}}`, `{{FILTER_SCRIPT_FILE_ID}}`, `{{RESUME_BUILDER_FILE_ID}}` | step 4.4 |
   | `{{APPLY_BOARD_URL}}` | step 4.7 |
   | `{{LOCAL_RESUMES_FOLDER}}` | e.g. `/Users/you/Documents/resumes` |
   | `{{MAX_ROLES_PER_NIGHT}}` | e.g. `8` |

3. Create the tasks. You can just tell Claude *"Create a scheduled task from this prompt"* and paste it.

   | Task | Schedule | Require this computer | Folder | Connectors |
   |---|---|---|---|---|
   | **Nightly job search** | Daily ~01:42 local | **Off** | none | Gmail, Google Drive |
   | **Prefill my applications** | None (Run now) | **On** | your resumes folder | Gmail, Google Drive, Claude in Chrome |

4. In each task's settings, turn on **Automatically approve** so the night run doesn't stop to wait
   for a click, and turn on **push notifications**.
5. Test: press **Run now** on the nightly task once and read the report.

---

## 5. Your daily routine

1. **Morning:** open the push report and the **Apply Board**. Each card shows the role, why it fits,
   flags (pay cut, comp not stated, US hours), the resume filename and an **Open application** button.
2. **Referrals:** for each role, open the two LinkedIn people-search links from the report and send
   the prepared note or message **yourself** to at least 5 people. Before sharing a resume's Drive
   link, set it to *"anyone with the link can view"*.
3. **At your desk:** press **Run now** on *Prefill my applications*. Chrome opens one tab per role,
   with everything filled except the resume.
4. In each tab: **Attach** the named file from `~/Documents/resumes` → review → **Submit** →
   press **Mark applied** on the Apply Board.
5. Follow-up drafts for applications with no reply after 10 days appear in Gmail **Drafts**. Review
   and send them yourself.

---

## 6. Using Codex or another agent

| Piece | Claude | Codex / other agents |
|---|---|---|
| Rules | uploaded skill | `AGENTS.md` → `skills/job-apply/SKILL.md` |
| Gmail / Drive | built-in connectors | a Gmail/Drive MCP server, or save resumes to `./out/` |
| Tracker | Apply Board | `tracker/applications.csv` (append only) |
| Form filling | Claude in Chrome | Playwright MCP / Chrome DevTools MCP, with the same rules |
| Schedule | scheduled tasks | cron / launchd / Task Scheduler |

```bash
# Codex, every night at 01:42
42 1 * * * cd ~/ai-job-hunt-agent && codex exec "Run prompts/nightly-job-search.md. Use tracker/applications.csv as the tracker and ./out for resumes instead of Drive."
```
More: [docs/05-other-agents.md](docs/05-other-agents.md).

---

## 7. Safety rules

- **Never makes things up.** Every resume line and form answer comes from `profile.md`.
- **Never submits.** It fills the form and stops. You submit.
- **Never applies twice.** It searches Gmail for an earlier confirmation before opening any form.
- **Never automates LinkedIn.** It reads alert emails only. You send referral messages yourself.
- **Lists only real, open jobs.** Every role is opened on the employer's own page first. Pay figures
  from job-board sites are labelled as estimates.
- **Never sends email.** Follow-ups are saved as drafts.
- **Never attaches test or placeholder files** to a real form.

---

## 8. Privacy

Your filled-in profile holds your phone number and salary. **Don't commit it to a public fork.**
Keep it as `profile.private.md` (git ignores it) or use a private fork. Never commit resumes,
Drive IDs, artifact links or tokens. `.gitignore` already excludes `*.pdf`, `out/` and `.env`.

---

## 9. Troubleshooting

| Problem | Fix |
|---|---|
| Ashby field looks empty after filling | It's often set already. The skill reads the real value with JavaScript before retyping, which stops text doubling up |
| Greenhouse asks for a "security code" | You've already applied to that role. Don't apply again |
| No LinkedIn alerts found | Check that the alert emails go to the connected Gmail and aren't deleted |
| Dataset says "scraped" more than 3 days ago | The run relies more on the ATS boards and YC that night |
| Resume runs to 2 pages | The builder shrinks the font from 9.8 to 9.2 pt. If it's still 2 pages, cut the weakest project |
| Prefill can't write resumes | Attach your resumes folder to the task (Add folder in the desktop app) |
| Filled form disappeared | You closed the built-in browser panel. Use Claude in Chrome instead |
| Microsoft/Meta/Uber careers pages don't load | They block cloud access. They're listed under "Needs manual check" |

---

## 10. Contributing

PRs are welcome: fixes for more ATS quirks, filters for other countries, support for other agents
and trackers (Notion, Airtable), and resume templates. See [CONTRIBUTING.md](CONTRIBUTING.md).
**Never include personal data in a PR.**

## License

MIT. Use at your own risk: you are responsible for what gets submitted in your name and for
following each site's terms.
