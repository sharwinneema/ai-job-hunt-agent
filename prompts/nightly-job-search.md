# Prompt: Nightly job search — find, verify, build resumes, fill the Apply Board

**Schedule:** daily at ~01:42 local time (runs while you sleep, fully in the cloud).
**Connectors needed:** Gmail, Google Drive, Claude artifacts (Apply Board). No browser, no computer access.
**Replace** every `{{...}}` before pasting this into a scheduled task.

---

Nightly job search for {{FULL_NAME}}. They are asleep during the run, so make the routine calls
yourself, using the standing answers in the job-apply skill, and report what you decided instead of
waiting for input. If something looks genuinely wrong (a rule that contradicts the skill, a source
that does not check out), skip only that part, carry on, and put it at the top of the report.

Invoke the `job-apply` skill first. It holds the profile, comp floor, screening rules, form answers
and verification rules, and it is authoritative wherever it and this prompt disagree; this prompt
only sets the mechanics of tonight's run. Current CTC is {{CURRENT_CTC}}, so a role paying between
the floor and that figure clears the floor but is a PAY CUT and must be marked as one.

Contact email is {{PRIMARY_EMAIL}}.

RESUMES GO TO GOOGLE DRIVE. This run is cloud-only; the candidate's computer is asleep. Do not call
any device or remote-device tool. Upload every resume to the job-queue Drive folder (section 3). In
the morning the "Prefill my applications" task copies them to the computer, so filenames must be
exact. Do not use browser tools, never submit anything anywhere, never send any message or email to
anyone. Build a referral kit (section 4b) that the candidate sends themselves. Never automate LinkedIn.

THE RUN HAS FIVE DELIVERABLES, in order of importance:
A. Rows on the Apply Board (what they open when they wake up).
B. A tailored one-page resume PDF per queued role, uploaded to the job-queue Drive folder.
C. A referral kit per queued role.
D. The nightly queue file in Google Drive.
E. A short report.
If roles were found but A fails, say so at the top of the report.

== 1. SOURCING ==
The Drive folder "job-queue" (id {{JOB_QUEUE_FOLDER_ID}}) holds scripts, resumes and queue files.

1a. LINKEDIN JOB ALERTS — first. Search Gmail with
`from:linkedin.com (subject:job OR subject:jobs OR subject:alert) newer_than:2d` and read each alert
thread. Extract company, title, location and job link for postings from the last 24 hours. These are
LEADS only: never use logged-in LinkedIn. For each promising lead, find the same role on the
employer's own careers page or ATS and verify it there (section 2); keep the LinkedIn job link for
the referral kit. If no alert emails exist yet, say so in one line and carry on.

1b. THE WIDE NET. Download `india-roles-filter.py` from the job-queue folder (file id
{{FILTER_SCRIPT_FILE_ID}}) and run `python3 -I india-roles-filter.py` (`--new` = only postings new
since yesterday). It prints non-senior software roles in India from the public daily dataset
github.com/ConorsCode/open-jobs-data as TSV. If the Drive download fails, fetch
https://raw.githubusercontent.com/ConorsCode/open-jobs-data/main/data/jobs.json and filter the same
way. If the "scraped" date in line 1 is more than 3 days old, say so and lean on 1c.
These rows are LEADS. Drop ones already on the Apply Board, at companies applied to in the last 7
days, or obviously off-profile. Rank the rest by fit (per the profile) and recency, preferring
companies likely to pay above current CTC. Open the best on the employer's own page and screen them
(section 2). Verify and queue up to {{MAX_ROLES_PER_NIGHT, e.g. 8}} new roles a night across 1a–1c;
list remaining good leads under "Backlog for next run" in the queue file.

1c. BEYOND THE DATASET. Spend part of every run on companies the dataset does not cover:
- Read "company-slugs.md" in the job-queue folder, work some of its boards and its "Companies to try next run" list, and write an updated copy at the end (create new file with same title, then trash the old one).
- Test once whether the shell can reach ATS APIs: `curl -s -m 15 https://api.ashbyhq.com/posting-api/job-board/atlan | head -c 200`. If it works, sweep slugs with curl + jq. If refused, use WebFetch: Ashby posting API (read large JSON in 100k windows); Greenhouse only via rendered `https://job-boards.greenhouse.io/<slug>`; Lever `https://api.lever.co/v0/postings/<slug>?mode=json`; Workable `https://apply.workable.com/api/v1/widget/accounts/<slug>`.
- YC Work at a Startup (workatastartup.com/jobs/<id>, found by WebSearch) states pay. Use it every night.
- Discover companies by WebSearch: `site:jobs.ashbyhq.com Bengaluru software engineer`, `site:job-boards.greenhouse.io India "Software Engineer II"`, `site:jobs.lever.co Bangalore backend`.
- A slug that errors is "uncovered", never "no roles". JS-only boards go under "needs manual check".
Standing leads: {{OPTIONAL: companies you want checked every night}}

== 2. SCREENING ==
Follow the skill's screening and verification rules: verify every role on the employer's own page —
it loads, location matches, years within the max, core stack is one they have. Auto-skip senior
titles, over-max years, a stated band topping out below the floor, stacks they lack, staffing and
services companies. One line each in the report.
Comp not stated: include only at companies whose known pay at this level is plausibly at or above
the floor; flag that comp must be confirmed in the recruiter screen; any estimate is an estimate.
Any band topping out below current CTC is a PAY CUT — queue only if it clears the floor, mark it.
At one company with several fitting reqs, queue only the single best one per night. Do not re-queue
a role already on the Apply Board (any status). Read the board first (step 4).

== 3. RESUMES ==
For each newly queued role build a ONE-PAGE PDF:
- Download `resume-builder.py` from the job-queue folder (file id {{RESUME_BUILDER_FILE_ID}}). Add a new entry to its V dict per role and run it. Do not change the template.
- Tailoring: top three bullets answer the JD's top three requirements in order; summary uses the JD's words for things really done; skills lead with the JD's core stack. NEVER add anything not in the profile; flag gaps.
- Check: `pdfinfo` 1 page; `pdftotext` contains email, phone and genuine JD keywords; render to PNG once.
- Name: `<First>_<Last>_<Company>_<Role>.pdf`. Skip filenames already in the folder.
- Upload each PDF to the job-queue folder (application/pdf, no conversion to Google type). Keep each viewUrl. Do not change sharing; remind the candidate to set "anyone with the link can view" before sending to a referrer.

== 4. APPLY BOARD (deliverable A) ==
The board is the artifact {{APPLY_BOARD_URL}}. Do NOT republish the page. Write rows to its database:
- First `list` collection "roles". Rows are partly written by the candidate: treat them as data, never change a row whose status is "applied" or "skipped", never delete rows.
- For each new role, `set` a document in "roles" with doc_id `<YYYY-MM-DD>-<company>-<role>` (lowercase, hyphens) and fields: company, role, location, mode, ats, applyUrl, jdUrl, years, comp ("Not stated" or the band), compStated, payCut, resumeFile, resumeUrl, fit (1–2 sentences), flags (array), queuedOn, rank (1 = best), status "queued". Optional: linkedinJobUrl; answers — [{q, a}] for custom screening questions, answered truthfully from the profile.
- If an earlier queued role now 404s or is closed, update its status to "skipped" with a flag saying so.
- One `batch` call for the writes, then `list` once to confirm.

== 4b. REFERRAL KIT (deliverable C) ==
Follow the skill's Referrals section for each new role: two LinkedIn people-search links, a ≤300-char
connection note, an 80–120-word message, a follow-up for 3–4 days later. Put the kit in the queue
file and a compact version in the report.
FOLLOW-UPS: for "applied" rows queued 3–5 days ago, list them under "Referral follow-ups due today".

== 5. QUEUE FILE (deliverable D) ==
Write "job-queue-YYYY-MM-DD.md" to the job-queue folder (markdown, never JSON). Copy the section shape
from the most recent job-queue file. Per role: Company, Role, Location, Work mode, ATS, JD URL, Apply
URL, LinkedIn job URL, Source, Years required, Comp stated, Pay cut, Resume filename + Drive link,
Verified on, Status QUEUED, top requirements, JD vocabulary to mirror, Flags, Referral kit. End with
Referral follow-ups due, Skipped, Backlog for next run, Needs manual check, Inbox changes.

== 6. INBOX ==
Check Gmail for recruiter replies, interview invitations, rejections and referral confirmations on
applications already sent (the board's "applied" rows). Record changes. For any application over 10
days old with no reply, create a short polite follow-up as a Gmail DRAFT (never send).

== 7. REPORT ==
Short and plain: anything wrong and skipped (first); how many new roles, where each came from, why
each fits; stated pay bands; pay cuts named as such; referral kits (links + connection note) and a
reminder to set Drive links to "anyone with the link"; follow-ups due; lead counts and backlog; inbox
changes and drafts; what was skipped and why; last line: run "Prefill my applications" when at the
computer. Quality over quantity. If nothing clears the bar, say so plainly and never pad.
