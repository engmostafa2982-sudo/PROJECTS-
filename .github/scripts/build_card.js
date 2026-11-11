// Refresh the MODON project card with the latest Excel files, using the card's own reader.
//
// Usage: node build_card.js CARD.html OUT.html FILE.xlsx [FILE.xlsx ...]
//
// Opens CARD.html in a headless browser, loads the Excel files through its "⬆ تحديث بيانات" button (in the order
// given: Projects Info first, then the CWAR file). Project status comes only from the "All Projects" sheet; contract
// records and progress % only from the CWAR file. Then saves
// the page through its "⬇ حفظ نسخة HTML" button. Prints the card's own status message.
const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs");

(async () => {
  const [card, out, ...files] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ acceptDownloads: true })).newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("file://" + path.resolve(card));
  await page.waitForSelector("#uplFile", { state: "attached" });
  // Sources, as the user set them:
  //  - project status: only the "All Projects" sheet of Projects Info. The CWAR sheet inside Projects Info is never used.
  //  - contract records and every progress %: only the standalone CWAR file.
  //  - a contract whose project is not ongoing in "All Projects" is never counted as Active.
  await page.evaluate(() => {
    const orig = detectApply;
    detectApply = function (wb, fname) {
      if (wb.Sheets["All Projects"]) {          // Projects Info: drop its CWAR sheet before the card reads it
        for (const n of wb.SheetNames.filter((n) => n.trim().toUpperCase() === "CWAR")) delete wb.Sheets[n];
        wb.SheetNames = wb.SheetNames.filter((n) => wb.Sheets[n]);
        return orig(wb, fname);
      }
      const msg = orig(wb, fname);
      const sn = wb.SheetNames.find((n) => n.trim().toUpperCase() === "CWAR");
      if (msg.startsWith("✔") && sn) {
        const c = parseCwar(wb.Sheets[sn]);
        if (Object.keys(c).length) {
          applyProg(c, CWAR);
          CWAR = c;
          applyExclusions();
          DATA_SRC.cwar = { src: fname, when: new Date().toLocaleString("sv-SE").slice(0, 16) };
          return msg + " · سجلات العقود من نفس الملف (" + Object.keys(c).length + " سجل)";
        }
      }
      return msg;
    };
  });
  const statusFromProjects = () => page.evaluate(() => {
    const st = {}, byParent = {};
    for (const p of ALL) {
      for (const id of [p.idD, p.idE]) if (id) st[String(id).trim()] = p.st;
      if (p.parent) (byParent[String(p.parent).trim()] = byParent[String(p.parent).trim()] || []).push(p.st);
    }
    let n = 0;
    for (const [pid, c] of Object.entries(CWAR)) {
      let s = st[pid];
      if (s === undefined && c.parent && byParent[String(c.parent).trim()] && byParent[String(c.parent).trim()].length === 1)
        s = byParent[String(c.parent).trim()][0];
      if (s !== undefined && c.cstat === "Active" && s !== "Ongoing Projects" && s !== "Under Design") {
        c.cstatCwar = c.cstat;
        c.cstat = s;          // shown and counted as the project's status from "All Projects"
        n++;
      }
    }
    return n;
  });
  const status = [];
  for (const f of files) {   // one file at a time, so the order is kept
    await page.evaluate(() => { document.getElementById("uplStatus").textContent = ""; });
    await page.setInputFiles("#uplFile", path.resolve(f));
    await page.waitForFunction(() => /[✔✖]/.test(document.getElementById("uplStatus").textContent), null, { timeout: 180000 });
    status.push(await page.textContent("#uplStatus"));
  }
  const fixed = await statusFromProjects();
  status.push("عقود Active في CWAR لكن مشروعها غير جاري في All Projects (اعتُمدت حالة All Projects): " + fixed);
  const [download] = await Promise.all([page.waitForEvent("download"), page.click("#dlBtn")]);
  await download.saveAs(path.resolve(out));
  console.log(status.join("\n"));
  if (errors.length) console.log("page errors:\n" + errors.join("\n"));
  await browser.close();
  if (status.some((s) => s.includes("✖")) || !fs.existsSync(out)) process.exit(1);
})();
