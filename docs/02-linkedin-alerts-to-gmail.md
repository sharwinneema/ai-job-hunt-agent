# 2. LinkedIn job alerts → Gmail (the first lead source)

The nightly run reads LinkedIn's **alert emails** in Gmail. It never logs in to LinkedIn and never
automates it (that's against LinkedIn's terms and gets accounts restricted). It only uses the emails
as leads, then verifies each role on the employer's own careers page.

## Create the alerts (5 minutes, once)

1. On linkedin.com click **Jobs**.
2. Search the role in your own words + a location, e.g. `Software Engineer II` · `Bengaluru`.
3. Add filters: **Date posted → Past 24 hours**, **Experience level → Associate / Mid-Senior**, and
   **Remote / Hybrid** if you like.
4. Turn on the **job alert toggle** on the results page (on some layouts it's a "Set alert" button).
5. Click **Manage alerts** → set **Frequency: Daily** and **Notify: Email** (email + app is fine).
6. Repeat for each search. LinkedIn allows **up to 20 alerts**. Good set for a 2-YOE engineer:
   - `Software Engineer` — Bengaluru / Hyderabad / Pune / Remote (India)
   - `Backend Engineer`, `AI Engineer`, `Agent`/`LLM` engineer, `Full Stack Engineer`
   - Company alerts: on a target company's LinkedIn page → **Jobs → Create job alert**.

## Make sure they land where the agent looks

- Use the **same Google account** for LinkedIn email and the Gmail connector.
  (LinkedIn → Me → Settings → Sign in & security → Email addresses → make it primary.)
- The agent's search is:
  `from:linkedin.com (subject:job OR subject:jobs OR subject:alert) newer_than:2d`
- If you auto-archive or filter LinkedIn mail, that's fine (search covers all mail) — just **don't
  auto-delete** it.
- Optional Gmail filter: Settings → Filters → *Create filter* → From: `jobalerts-noreply@linkedin.com`
  → *Apply label* `job-alerts` + *Never send to Spam*.

## Test it

Ask Claude: *"Search my Gmail for LinkedIn job alert emails from the last 2 days and list company,
title and job link."* If it finds them, the nightly run will too.
