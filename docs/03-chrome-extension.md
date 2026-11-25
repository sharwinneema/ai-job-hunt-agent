# 3. Claude in Chrome extension (for the Prefill run)

The Prefill run opens each application in **its own tab in your real Chrome** and fills every field
except the resume. Real Chrome is better than the app's built-in browser because the tabs stay open
until *you* close them.

## Requirements
- A paid Claude plan (Pro, Max, Team or Enterprise).
- Desktop **Google Chrome** (not Edge/Brave/Arc, not mobile).
- The **Claude desktop app** (Mac/Windows) on the same computer, for scheduled/remote runs.

## Install
1. Open Chrome → Chrome Web Store → search **"Claude"** by **Anthropic**
   (https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn).
2. **Add to Chrome**, then sign in with your Claude account.
3. Pin it: puzzle-piece icon → thumbtack next to **Claude**.

## Connect it to the Claude desktop app
1. Desktop app → your initials (bottom-left) → **Settings → Connectors**.
2. Find **Claude in Chrome** → **Configure** → toggle **on**.
3. Settings → **Preferred browser** → choose **Claude in Chrome** (otherwise the built-in browser is used).
4. Site permissions: the first time Claude acts on a site (e.g. `jobs.ashbyhq.com`,
   `job-boards.greenhouse.io`, `jobs.lever.co`, `*.myworkdayjobs.com`) you'll be asked to allow it.
   Allow the ATS sites you apply through.

## Before you press "Run now" on Prefill
- Chrome is open and the extension is signed in.
- The Claude desktop app is open (the task has **Require this computer** on).
- Your resumes folder (e.g. `~/Documents/resumes`) is attached to the task.

## What the agent will and won't do
- ✅ Opens one tab per role, fills name/email/phone/links/CTC/notice/screening questions, reads every
  field back (Ashby fields can *look* empty when set — it checks with JavaScript first).
- ❌ Never clicks Submit. ❌ Never attaches the resume (native file pickers can't be driven) —
  you click *Attach*, pick the named file from your resumes folder, review, submit.
- ❌ Never logs in to LinkedIn or sends messages.

Safety: read Anthropic's "Use Claude in Chrome safely" guide in the Claude Help Center. Only allow
sites you trust.
