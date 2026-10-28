// Saves a report's PDF exactly as its own "⬇ PDF" button does: same look as the HTML, A4-shaped pages,
// cut only between rows, cards and photos, table headers repeated.
// Usage: node export_pdf.js REPORT.html OUT.pdf [en|ar] [dark|light]
// Needs Playwright. The PDF libraries load from cdn.jsdelivr.net; set PDF_LIBS to a folder holding
// html-to-image.js and jspdf.umd.min.js to work offline.
const { chromium } = require('playwright'); const path = require('path');
const [,, html, out, lang = 'en', theme = 'dark'] = process.argv;
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ acceptDownloads: true, viewport: { width: 1200, height: 900 } });
  if (process.env.PDF_LIBS) await ctx.route('https://cdn.jsdelivr.net/**', r => r.fulfill({ contentType: 'application/javascript',
    path: path.join(process.env.PDF_LIBS, r.request().url().includes('html-to-image') ? 'html-to-image.js' : 'jspdf.umd.min.js') }));
  const p = await ctx.newPage();
  await p.addInitScript(`try { for (const k of Object.keys(localStorage)) if (/-theme$/.test(k)) localStorage.removeItem(k); } catch (e) {}`);
  await p.goto('file://' + path.resolve(html) + '#' + lang);
  await p.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
  const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 180000 }), p.click('#pdf-btn')]);
  await dl.saveAs(out); console.log(out); await b.close();
})();
