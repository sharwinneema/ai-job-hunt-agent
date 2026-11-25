# 1. Connectors — only what this actually uses

| Connector | Used by | What for | Required? |
|---|---|---|---|
| **Gmail** | Nightly + Prefill | Read LinkedIn job-alert emails; detect "already applied" acknowledgements; spot recruiter replies; create follow-up **drafts** (never sends) | Yes |
| **Google Drive** | Nightly + Prefill | `job-queue` folder: scripts, tailored resume PDFs, nightly queue file, `company-slugs.md` | Yes |
| **Claude artifacts** (built in) | Nightly + Prefill | The Apply Board page + its database (`roles`) | Yes on Claude (or use the CSV tracker) |
| **Claude in Chrome** (browser extension) | Prefill only | Fill the application forms in your real Chrome, tabs stay open | Strongly recommended |
| Built-in browser (Claude desktop app) | Prefill fallback | Same, if the extension isn't available — closing the pane wipes the form | Fallback |
| Your computer ("Require this computer" + a folder) | Prefill only | Copy resumes into e.g. `~/Documents/resumes` so the file picker finds them | Yes for prefill |
| Web search / web fetch / shell (built in) | Nightly | Search ATS boards, run the Python scripts, build PDFs with LaTeX | Built in |

**Not needed:** Supabase, Vercel, OpenArt, Autosheet, Claude Docs. They happen to be attached to the
original tasks but the workflow never uses them — leave them off when you create yours.

## Connect them in Claude

1. claude.ai (or the desktop app) → **Settings → Connectors**.
2. Connect **Gmail** and **Google Drive** with the Google account that receives your job emails.
3. When you create each scheduled task, tick only the connectors in the table above.

## Set up the Drive folder

1. In Google Drive create a folder named **`job-queue`**.
2. Upload `scripts/india-roles-filter.py` and your filled-in `scripts/resume-builder.py`.
3. Create an empty `company-slugs.md` (the nightly run keeps it updated — a list of ATS board slugs
   it has checked and "Companies to try next run").
4. Get IDs: open the folder → the URL ends in `/folders/<FOLDER_ID>`. Right-click a file → *Share →
   Copy link* → the ID is between `/d/` and `/view`. Paste these into `prompts/nightly-job-search.md`
   (`{{JOB_QUEUE_FOLDER_ID}}`, `{{FILTER_SCRIPT_FILE_ID}}`, `{{RESUME_BUILDER_FILE_ID}}`).
