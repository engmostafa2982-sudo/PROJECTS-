---
name: progress-report
description: Build the standard weekly progress report (HTML + English and Arabic dark PDFs) for any project in this repository from its MD Files. Use when asked for a progress report, weekly report, or "the standard report" for a project or week.
---

# Standard progress report

The standard is defined in `_report-standard/README.md`. Read it first. Then build the new report by copying `_report-standard/template.html` (the reference report before its photos and fonts were embedded, small enough to edit) and replacing its data. Do not design a new page: the layout, CSS, scripts, switches, Edit, PDF and photo viewer stay exactly as in the reference.

## 1. Gather the data

1. **Pick the week.** Unless told otherwise, use the project's highest `4-Weekly update/W<n>` that has files. Its data date is the weekly report's cut-off date, and the report week is that date's week number of the year.
2. **Read the MD files.**
   - The week's `MD Files`: weekly report sheets, progress presentation, P6 update.
   - The previous week's `MD Files`, for the this-week values and the gained-this-week figures.
   - `3-Baseline/MD Files` and `1-BOQ/MD Files`, when the sections need them.
3. **Write down every figure with its file and sheet.** If two files disagree, keep both values and add a Data notes item. Never estimate a missing figure; leave the section out instead.
4. **Choose photos.** Take 6 photos from the week's `All Files`. Read each photo's MD file (EXIF and OCR) for its date and GPS stamp. Resize each to 1280 px wide (JPEG, quality about 82) into `Generated Report/photos/`.

## 2. Fill the reference

Copy `_report-standard/template.html` to `Generated Report/<Project>-progress-report-week-<NN>.html`. Use a short Latin project name, e.g. `Sudair`. Then replace, keeping the markup structure:

- **Markup:** the header text and facts, each section's intro line, tiles, tables and callouts, and the photo `<figure>` blocks.
  - Photos use `href="photos/<file>" class="ph"><img src="photos/<file>"`, which `embed_assets.py` turns into embedded data.
- **Script data arrays:**
  - `months` / `base` / … for the S-curve
  - `proc` for procurement
  - `scope` for quantities, with the previous week's finished value so the this-week column fills
  - `mpM` / `mpP` / `mpA` for manpower
- **Storage keys:** change the `kharj-report-lang` and `kharj-report-theme` localStorage keys to `<project>-report-lang` / `<project>-report-theme`.
- **PDF names:** change the PDF file names in the export script to this project's names and week.
- **Old text:** remove every Kharj-specific sentence. Search the result for `Kharj`, `الخرج`, `Week 46` and `26-Oct-2026` to make sure none are left.

### Arabic

The page is translated by the `const AR = {...}` dictionary: an English visible text maps to its Arabic.
- Every new or changed English text needs an entry. The key is the element's visible text, with no tags and with `&amp;` written as `&`.
- Use the wording table in the standard; for example, write *متأخر بنسبة 5.5%*, never *نقطة*.
- Delete entries that no longer appear on the page.

## 3. Finish and check

```bash
cd "<project>/4-Weekly update/W<n>/Generated Report"
python ../../../../_report-standard/tools/embed_assets.py <Project>-progress-report-week-<NN>.html
node ../../../../_report-standard/tools/export_pdf.js <Project>-progress-report-week-<NN>.html <Project>-progress-report-week-<NN>.pdf en dark
node ../../../../_report-standard/tools/export_pdf.js <Project>-progress-report-week-<NN>.html "تقرير-تقدم-<المشروع>-الأسبوع-<NN>.pdf" ar dark
```

Before committing, open the HTML with Playwright, in English and Arabic, and check that:
- there are no page errors
- all 6 photos load
- no English text is left on the Arabic page, apart from names, codes and units
- no table is wider than the page
- the PDFs have several A4-shaped pages with no row cut in half

Look at page 1 of each PDF as an image. Then commit the `Generated Report` folder and push.
