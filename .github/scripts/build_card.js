// Refresh the MODON project card with the latest Excel files, using the card's own reader.
//
// Usage: node build_card.js CARD.html OUT.html FILE.xlsx [FILE.xlsx ...]
//
// Opens CARD.html in a headless browser, loads the Excel files through its "⬆ تحديث بيانات" button (in the order
// given: Projects Info first, then the CWAR file, so that every progress % and contract status comes from the CWAR
// file when it is the newer one), then saves
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
  // A standalone CWAR file normally only updates the progress %. Make it also replace the contract records
  // (status, dates, values) when it is newer than the CWAR sheet inside Projects Info, so a contract that the
  // newer file shows as complete is not still counted as active.
  await page.evaluate(() => {
    const orig = detectApply;
    detectApply = function (wb, fname) {
      const msg = orig(wb, fname);
      const sn = wb.SheetNames.find((n) => n.trim().toUpperCase() === "CWAR");
      if (msg.startsWith("✔") && !wb.Sheets["All Projects"] && sn) {
        const c = parseCwar(wb.Sheets[sn]);
        const newest = (m) => Object.values(m).map((x) => x.dataDate || "").sort().pop() || "";
        if (Object.keys(c).length && newest(c) >= newest(CWAR)) {
          applyProg(c, CWAR);
          CWAR = c;
          applyExclusions();
          DATA_SRC.cwar = { src: fname, when: new Date().toLocaleString("sv-SE").slice(0, 16) };
          return msg + " · حالة العقود وتواريخها من نفس الملف (" + Object.keys(c).length + " سجل)";
        }
      }
      return msg;
    };
  });
  const status = [];
  for (const f of files) {   // one file at a time, so the order is kept
    await page.evaluate(() => { document.getElementById("uplStatus").textContent = ""; });
    await page.setInputFiles("#uplFile", path.resolve(f));
    await page.waitForFunction(() => /[✔✖]/.test(document.getElementById("uplStatus").textContent), null, { timeout: 180000 });
    status.push(await page.textContent("#uplStatus"));
  }
  const [download] = await Promise.all([page.waitForEvent("download"), page.click("#dlBtn")]);
  await download.saveAs(path.resolve(out));
  console.log(status.join("\n"));
  if (errors.length) console.log("page errors:\n" + errors.join("\n"));
  await browser.close();
  if (status.some((s) => s.includes("✖")) || !fs.existsSync(out)) process.exit(1);
})();
