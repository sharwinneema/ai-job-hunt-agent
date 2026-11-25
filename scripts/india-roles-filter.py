#!/usr/bin/env python3
"""Wide-net filter for the nightly job search.
Downloads the public daily dataset (ConorsCode/open-jobs-data, ~38k jobs, ~380 companies, 9 ATSs),
keeps non-senior software roles in India, and prints them as TSV: company, title, locations, platform, postedAt, applyUrl.
Usage: python3 -I india-roles-filter.py [--new]   (--new = only postings new since the dataset's previous snapshot)
These rows are LEADS: every role must still be opened on the employer's own page and screened before it is queued."""
import json, re, sys, urllib.request
BASE = "https://raw.githubusercontent.com/ConorsCode/open-jobs-data/main/data/"
name = "new-jobs.json" if "--new" in sys.argv else "jobs.json"
raw = json.load(urllib.request.urlopen(BASE + name, timeout=180))
jobs = raw if isinstance(raw, list) else raw.get("jobs", [])
IN  = re.compile(r"india|bengaluru|bangalore|hyderabad|pune|gurgaon|gurugram|noida|chennai|mumbai|delhi|\bgoa\b|\bIN-|, IND\b", re.I)
ENG = re.compile(r"engineer|developer|\bsde\b|\bswe\b|member of technical", re.I)
SENIOR = re.compile(r"senior|senio\b|\bsr\b|sr\.|staff|principal|\blead\b|manager|director|\bhead\b|intern\b|architect|\bvp\b|\bIII\b|\bIV\b|\bPMTS\b|\bLMTS\b|distinguished|new grad", re.I)
OFF = re.compile(r"sales|solution|support|security|vulnerab|\bqa\b|quality|test|sdet|validation|verification|asic|soc\b|gpu|cpu|silicon|pcb|rtl|signal|hardware|firmware|embedded|mechanical|automotive|network|reliability|\bsre\b|devops|success|escalation|account|field|analytics|data engineer|machine learning|research|android|\bios\b|mobile|netsuite|workday|content|marketing|ux\b|design\b|power delivery|services engineer|operations", re.I)
out, seen = [], set()
for x in jobs:
    loc = "; ".join(x.get("locations") or [])
    t = x.get("title") or ""
    if not IN.search(loc) or not ENG.search(t) or SENIOR.search(t) or OFF.search(t): continue
    key = (x.get("company"), t, x.get("applyUrl"))
    if key in seen: continue
    seen.add(key); out.append(x)
stamp = max((x.get("scrapedAt") or "" for x in jobs), default="")
print(f"# dataset {name}: {len(jobs)} jobs, scraped {stamp}; {len(out)} India non-senior software leads across {len({x['company'] for x in out})} companies")
for x in sorted(out, key=lambda x: (x["company"], x["title"])):
    print("\t".join([x["company"], x["title"], "; ".join(x.get("locations") or []), x.get("platform") or "", str(x.get("postedAt") or ""), x.get("applyUrl") or ""]))
