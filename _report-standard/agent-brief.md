Build the standard weekly progress report AND the Arabic email to the project manager for ONE project, in the repo /home/user/infrastructure-projects.

Read first, in full:
- /home/user/infrastructure-projects/_report-standard/README.md — the standard (sections, rules, Arabic wording, week number, physical-%-only rule, email rules)
- /home/user/infrastructure-projects/.claude/skills/progress-report/SKILL.md — build steps
- /home/user/infrastructure-projects/_report-standard/template.html — the page to copy (study the markup, the `const AR = {...}` dictionary and the chart data arrays before editing)
- /home/user/infrastructure-projects/_report-standard/email-template.md — the email
Week folders are now named "W<nn> - <DD-Mon-YYYY>" (Thursday the week starts on). Build from the week folder given below (its MD Files; All Files only for photos / originals). If the project has an earlier week folder with files, use the previous week's MD Files for this-week / gained-this-week values; otherwise show "—" and say so in Data notes.

Hard rules:
- Every number from the MD files. Never guess; never carry over another project's numbers. Leave out any section without data (delete the <section> and make sure no script errors result).
- Every PROGRESS percentage is PHYSICAL % complete (man-hour weighted). No cost-based / earned-value / value-weighted progress or its SPI anywhere (not even Data notes, except saying a file labels cost-based progress as "actual", without numbers). If no man-hour physical figure exists in the weekly report, compute it from the P6 XER (activity phys_complete_pct weighted by labour units; planned from the baseline/target dates) if sound, and state the method in one line; otherwise say plainly no physical % is available.
- Week number = contract week the report states (e.g. "Current Contract Weeks: 41"), else (data date − site handover/commencement) // 7. Never the report's serial number ("WPR #56").
- Keep layout/CSS/scripts unchanged except data, texts, localStorage keys (`kharj-report-lang/theme` → `<slug>-report-lang/theme`) and the PDF names in the export script. Remove every Kharj text (grep the result for Kharj, الخرج, Week 46, 26-Oct-2026, w46 — only real data may remain).
- Arabic: every visible English string needs an AR entry (key = visible text without tags, &amp; as &); delete unused entries; use the standard's wording table.
- Photos: photo files in the week's All Files first; else images embedded in the weekly report xlsx/pptx (unzip xl/media or ppt/media) or PDFs (pdfimages); only real site photos ≥ 600 px wide; an even number (2/4/6); resize to max 1280 px wide JPEG q82 into Generated Report/photos/<slug>-N.jpg; none → delete the photos section but keep the viewer markup outside sections so its script runs.

Output in "<WEEKDIR>/Generated Report/" (keep its README.md):
- <Short>-progress-report-week-NN.html (embedded with embed_assets.py; keep an un-embedded working copy OUTSIDE the repo in your own scratch folder under /tmp/claude-0/-home-user/5611010b-33b1-52ef-8788-9cdca09c6b43/scratchpad/<slug>/)
- <Short>-progress-report-week-NN.pdf (English, dark) and تقرير-تقدم-<ArabicShort>-الأسبوع-NN.pdf (Arabic, dark)
- <Short>-PM-email-week-NN.md — formal Arabic, per the email template and rules (أولاً three bullets with physical figures, required weekly rate = (100 − actual) ÷ whole weeks left to contract completion, computed in Python; ثانياً this-week works table; ثالثاً causes; رابعاً actions with owner). Put a BLANK line between the **إلى:** and **الموضوع:** lines. Addressee = MODON PM named in the files, else "مدير المشروع".
- photos/ if any

Commands (no CDN access here; use exactly):
  cd "<WEEKDIR>/Generated Report"
  python3 /home/user/infrastructure-projects/_report-standard/tools/embed_assets.py "<html>"
  export NODE_PATH=$(npm root -g) PDF_LIBS=/home/user/infrastructure-projects/_report-standard/tools/libs
  node /home/user/infrastructure-projects/_report-standard/tools/export_pdf.js "<html>" "<en pdf>" en dark
  node /home/user/infrastructure-projects/_report-standard/tools/export_pdf.js "<html>" "<ar pdf>" ar dark

Verify (Playwright via file://, NODE_PATH as above): no page errors EN and #ar; photos load; no leftover English sentences on the Arabic page; no table wider than the page at 1080 px; render page 1 of each PDF with pdftoppm and look at it.
Do NOT git add/commit/push, do not touch other projects or _report-standard. Put no temp files in the repo.

Final reply (short): file paths, data date, week number and why, sections left out and why, photo source, the three أولاً figures, and data problems found.
