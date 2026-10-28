# Standard weekly progress report

Every project's weekly progress report follows the report in [`reference-report.html`](reference-report.html) (Al-Kharj, week 46). It has the same sections, the same look, the same features and the same file names. Only the project's data changes.

To get a report, ask Claude in this repository, for example: *"Generate the standard progress report for project 07 from its latest weekly upload."* The [`progress-report`](../.claude/skills/progress-report/SKILL.md) skill tells Claude how to build it.

## Where it goes

`<project>/4-Weekly update/W<n>/Generated Report/` — the week the report is built from.

| File | What it is |
|---|---|
| `<Project>-progress-report-week-<NN>.html` | The report. One self-contained file: photos and fonts are inside it, so it works when downloaded, emailed or opened from disk. |
| `<Project>-progress-report-week-<NN>.pdf` | English PDF, dark. |
| `تقرير-تقدم-<المشروع>-الأسبوع-<NN>.pdf` | Arabic PDF, dark. |
| `photos/` | The site photos used in the report. |

`<NN>` is the **project week**: whole weeks from site handover (or commencement, if no handover date is given) to the data date, i.e. `(data date − handover) // 7` days. Kharj: 03-Dec-2025 → 26-Oct-2026 is 327 days, week 46. If the weekly report states the contract week (e.g. "Current Contract Weeks: 33 of 44"), use that number (it can be one higher than the formula, because contract weeks count from 1). A report's serial number ("Weekly Report #29") is not the week number.

## Sections, in order

| # | Section (EN / AR) | Content | Usual source in MD Files |
|---|---|---|---|
| — | Header | Project name in Arabic and English, report week and data date, project number, contract number. Facts row: owner, contractor, consultant, project manager, site handover, contract end. One-line scope. | Weekly report cover / project info sheet |
| 1 | Status at a glance / ملخص تقدم المشروع | One paragraph, then 4 tiles: physical % complete vs plan (with SPI), progress this week vs plan, time elapsed of contract, invoiced to date. Then a red or amber callout with the main schedule message. | Physical progress sheet, P6 update (XER) |
| 2 | Site photos this week / صور الموقع هذا الأسبوع | 6 photos, 2 per row, all the same size, each with a title and one line (date and GPS stamp if visible). Clicking opens the photo inside the report. | Photos in the week's All Files |
| 3 | Progress S-curve / منحنى التقدم (S-Curve) | Cumulative planned vs actual (and revised plan if one exists), monthly. Table of the last 6 weeks: planned, actual, variance, gained this week, SPI. | Physical-Chart Data sheet |
| 4 | Progress by phase / التقدم حسب المرحلة | Per WBS phase: weight, planned, actual, variance, SPI, status pill. | Physical progress by WBS |
| 5 | Scope of work: quantities / نطاق العمل: الكميات | Bar chart of % finished per network. Table per item and zone: unit, total, finished, **this week**, remaining, % finished, backfilled where relevant. Subtotal row per item. | Quantity tables in the progress presentation |
| 6 | Milestones / المعالم الرئيسية | Baseline, weekly-report forecast, P6 forecast, P6 float, status. Callout if the two forecasts disagree. | Milestone sheet, P6 update |
| 7 | Procurement of key materials / توريد المواد الرئيسية | % delivered per material as bars, coloured by status, plus a callout for the critical items. | Procurement sheet |
| 8 | Manpower / القوى العاملة | Monthly planned vs actual head count. | Manpower sheet |
| 9 | Cost and invoicing / التكلفة والمستخلصات | Contract value, variations, invoices submitted and approved. | Cost / invoice sheet |
| 10 | Health, safety and quality / الصحة والسلامة والجودة | Safe man-hours, incidents, inspections (MIR, IR, NCR). | HSE and QA/QC sheets |
| 11 | Open issues and risks / المشكلات والمخاطر القائمة | Issue, owner, detail. | Issues / risks sheet |
| 12 | Data notes / ملاحظات على البيانات | Inconsistencies found in the uploaded files, so the team can correct them. | Comparing the files |

A section with no data for a project is left out. A section is never filled with guessed numbers. There is **no Sources section**; the source of each chart is named in one short line under its heading.

## Rules

- **Progress is physical % complete only**, weighted by budgeted man-hours. Do not show cost-based or earned-value progress as the main figure.
- Scope quantities always include a **this-week** column (this week's cumulative minus last week's).
- Variances are written as percentages, e.g. Arabic *متأخر بنسبة 5.5%*. Do not write them as points.
- Dates are written `26-Oct-2026` (Arabic: `26-أكتوبر-2026`), always left-to-right.
- Every number in the report comes from the MD Files of that project. When two files disagree, both values are shown and the difference is listed under Data notes.

### Arabic wording (use exactly these)

| Use | Not |
|---|---|
| ملخص تقدم المشروع | الوضع في لمحة |
| يقاس بعدد ساعات العمل المخططة | موزونة بساعات العمل المخططة |
| متأخر بنسبة … % | متأخر بـ … نقطة |
| التوريدات | التوريد |
| المناهل | المناهيل |
| مواسير السيول الفرعية | مواسير السيول الثانوية |
| صنبور إطفاء الحريق | حنفيات الحريق |
| العبارة الصندوقية | القناة الصندوقية |
| تمديدات (cables) | كابل |
| تمديدات الاتصالات | مجاري الاتصالات |

## Features every report has

- **English / عربي** switch: the whole page, including charts, switches to Arabic, right-to-left.
- **Light / Dark** switch.
- **✎ Edit**: click any text, change it, Save.
  - Inside Claude, the change is saved for everyone.
  - In a downloaded file, Save downloads an updated copy of the file with the change inside it.
- **⬇ PDF**: the page exactly as on screen, in A4-shaped pages. Pages are cut only between rows, cards and photos, and table headers repeat on the next page.
- The photo viewer opens inside the page, with arrows, swipe and keyboard.
- Tables fit the page width. Nothing scrolls sideways in the PDF.

## Tools

| Tool | Use |
|---|---|
| [`template.html`](template.html) | The reference report before embedding (photos and fonts as links). Copy and edit this one. |
| [`tools/embed_assets.py`](tools/embed_assets.py) | `python embed_assets.py REPORT.html` embeds `photos/` and the fonts into the HTML, so it is one self-contained file. |
| [`tools/export_pdf.js`](tools/export_pdf.js) | `node export_pdf.js REPORT.html OUT.pdf ar dark` saves the PDF the same way as the page's own PDF button. Needs Playwright. |
| `tools/fonts/` | The report's fonts: IBM Plex Sans, IBM Plex Sans Arabic, IBM Plex Mono and Archivo. |
