#!/usr/bin/env python3
r"""One-page tailored resume builder (LaTeX -> PDF).

HOW TO USE
1. Fill CONTACT, JOB, PREV, EDU, the bullet bank B, projects P and skills S with YOUR REAL facts
   (they must match skills/job-apply/profile.md - never put anything here you haven't done).
2. For each job, add one entry to V: summary, bullet order (keys of B), projects, skills order.
3. Run:  python3 resume-builder.py      (needs pdflatex + pdfinfo: texlive + poppler-utils)
   It tries font sizes 9.8 -> 9.2 until the PDF is exactly one page.
LaTeX: escape % as \%, & as \&, use --- for an em dash.
"""
import subprocess, sys, os
AR = r"$\rightarrow$"

CONTACT = {"NAME": "Jane Doe", "CITY": "Bengaluru, India", "PHONE": "+91 90000 00000",
           "EMAIL": "jane@example.com", "GITHUB": "github.com/janedoe", "LINKEDIN": "linkedin.com/in/janedoe"}
JOB  = {"employer": "Acme Corp", "title": "Software Engineer, Platform", "dates": "Jan 2024 -- Present", "location": "India"}
PREV = {"employer": "Acme Corp", "title": "Software Engineering Intern", "dates": "May 2023 -- Jul 2023", "location": "India",
        "bullet": r"Built an internal Python tool that cut weekly report prep from 3 hours to 10 minutes; converted to a full-time offer."}
# PREV = None   # if you have no second role
EDU  = {"school": r"Example Institute of Technology --- B.Tech Computer Science", "years": "2019 -- 2023",
        "line": r"CGPA 8.5/10 \textperiodcentered{} Lead, coding club: ran 12 workshops for 300+ students."}

# Bullet bank: every real achievement once, best-phrased. Variants pick and order them.
B = {
 "api":   r"Designed and shipped 8 REST services in Spring Boot on PostgreSQL and Redis serving 2M requests/day.",
 "perf":  rf"Cut p95 latency 40\% on the checkout API (N+1 queries {AR} batched reads, Redis for hot keys).",
 "kafka": r"Built a Kafka-based event pipeline replacing nightly cron syncs; data freshness went from 24h to under 1 minute.",
 "llm":   r"Shipped a RAG support assistant over 5k help articles; 35\% of tickets now resolved without an agent.",
 "ui":    r"Rebuilt the admin dashboard in React + TypeScript, used daily by 60 ops staff.",
}
P = {
 "side": (r"SideProject --- Next.js, PostgreSQL, Prisma, Vercel", "2024 -- Present", [
   r"Sole engineer on a live app with 1,200 users: schema, versioned APIs, payments and deployment.",
   r"Signed upload URLs and server-side validation for user files."]),
 "hack": (r"Hackathon Project --- MERN, WebSockets", "2023", [
   r"Won a 48-hour hackathon: real-time dashboard over WebSockets."]),
}
S = {
 "lang":  r"\textbf{Languages:} {L}",
 "be":    r"\textbf{Backend and data:} Spring Boot, Node.js, REST, Kafka, PostgreSQL, Redis",
 "ai":    r"\textbf{AI:} RAG, LLM tool calling, prompt engineering, vector databases",
 "fe":    r"\textbf{Frontend:} React, Next.js, TypeScript",
 "infra": r"\textbf{Infrastructure:} Docker, Kubernetes, CI/CD, Grafana",
}
# One entry per tailored resume. Key = output filename (no .pdf).
V = {
 "Jane_Doe_ExampleCo_Backend_Engineer": dict(
   summary=r"Backend engineer with 2 years building high-traffic Java/Spring Boot services on PostgreSQL, Redis and Kafka; owns systems from schema design to production rollout.",
   bullets=["api","perf","kafka","llm","ui"],
   projects=["side","hack"], pb={"side":2},
   skills=["lang","be","infra","ai","fe"], langs="Java, Python, TypeScript, SQL"),
}
HEAD = r"""\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\usepackage{cmap}
\usepackage{helvet}\renewcommand{\familydefault}{\sfdefault}
\usepackage[top=0.42in,bottom=0.4in,left=0.5in,right=0.5in]{geometry}
\usepackage{enumitem}\usepackage{titlesec}\usepackage[hidelinks]{hyperref}
\pagestyle{empty}\setlength{\parindent}{0pt}\frenchspacing
\titleformat{\section}{\normalsize\bfseries\uppercase}{}{0pt}{}[\vspace{-6pt}\rule{\linewidth}{0.4pt}]
\titlespacing*{\section}{0pt}{5pt}{3pt}
\setlist[itemize]{leftmargin=1.1em,itemsep=0.6pt,topsep=1.5pt,parsep=0pt,label=\textbullet}
\newcommand{\row}[2]{\textbf{#1}\hfill #2\par}
\begin{document}\fontsize{FS}{LS}\selectfont
\begin{center}{\LARGE\bfseries NAME}\\[3pt]
CITY \textperiodcentered{} PHONE \textperiodcentered{} \href{mailto:EMAIL}{EMAIL}\\
\href{https://GITHUB}{GITHUB} \textperiodcentered{} \href{https://LINKEDIN}{LINKEDIN}
\end{center}\vspace{-6pt}
"""
def build(name, v, fs=9.6):
    t = HEAD.replace("FS", str(fs)).replace("LS", str(round(fs*1.18,2)))
    for k,val in CONTACT.items(): t = t.replace(k, val)
    t += "\\section{Summary}\n" + v["summary"] + "\n"
    t += "\\section{Experience}\n\\row{"+JOB["employer"]+"}{"+JOB["dates"]+"}\n\\textit{"+JOB["title"]+"}\\hfill "+JOB["location"]+"\n\\begin{itemize}\n"
    t += "".join(f"\\item {B[k]}\n" for k in v["bullets"]) + "\\end{itemize}\n\\vspace{2pt}"
    t += ("\\row{"+PREV["employer"]+"}{"+PREV["dates"]+"}\n\\textit{"+PREV["title"]+"}\\hfill "+PREV["location"]+"\n\\begin{itemize}\\item " + PREV["bullet"] + "\\end{itemize}\n" if PREV else "")
    t += "\\section{Projects}\n"
    for p in v["projects"]:
        title, dates, bl = P[p]; bl = bl[:v["pb"].get(p, len(bl))]
        t += f"\\row{{{title}}}{{{dates}}}\n\\begin{{itemize}}\n" + "".join(f"\\item {x}\n" for x in bl) + "\\end{itemize}\n\\vspace{1pt}"
    t += "\\section{Skills}\n" + "\\\\\n".join(S[k].replace("{L}", v["langs"]) for k in v["skills"]) + "\n"
    t += "\\section{Education}\n\\row{"+EDU["school"]+"}{"+EDU["years"]+"}\n"+EDU["line"]+"\n\\end{document}\n"
    open(name+".tex","w").write(t)
    r = subprocess.run(["pdflatex","-interaction=nonstopmode","-halt-on-error",name+".tex"],capture_output=True,text=True)
    if r.returncode: print(r.stdout[-1500:]); sys.exit(1)
    pages = [l for l in subprocess.run(["pdfinfo",name+".pdf"],capture_output=True,text=True).stdout.splitlines() if l.startswith("Pages")][0]
    return pages
for n,v in V.items():
    for fs in (9.8, 9.6, 9.4, 9.2):
        pg = build(n, v, fs)
        if pg.split()[-1]=="1": break
    print(n, pg, "font", fs)
