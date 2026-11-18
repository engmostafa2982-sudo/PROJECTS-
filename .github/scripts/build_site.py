"""Build the progress-report website (GitHub Pages) from the generated reports.

Usage: build_site.py OUT_DIR

  OUT_DIR/index.html        the MODON project card (main files/MODON_Project_Card_*.html), refreshed with the newest
                            Projects Info and CWAR workbooks in "main files", plus a «تقارير التقدم الأسبوعية» tab
  OUT_DIR/reports.html      every project with a weekly report: physical % complete from the CWAR file, links
  OUT_DIR/<NN>/index.html   project NN's latest report (a fixed link that always shows the newest week)
  OUT_DIR/<NN>/<week>.html  every earlier week's report, e.g. 05/W04-22-Oct-2026.html
The PDF buttons open the PDFs stored in the repository, so the site itself stays small.

Everything in OUT_DIR except .git is replaced, so the site always matches the repository.
"""
import html
import os
import re
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).parent))
from weeks import NEW_NAME  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REPO = os.environ.get("GITHUB_REPOSITORY", "engmostafa2982-sudo/PROJECTS-")
RAW = f"https://github.com/{REPO}/raw/main"
FONTS = ROOT / "_report-standard" / "tools" / "fonts"
MAIN = ROOT / "main files"
CONTRACT_ID = re.compile(r"\b[A-Z]{3,4}\d?-\d{2}-\d{2,3}\b")


def newest(pattern):
    """The newest file in main files matching pattern: by the date in its name (03Nov2026, 2026-10-25), else by name."""
    def key(f):
        m = re.search(r"(\d{1,2})([A-Za-z]{3})(20\d\d)", f.name)
        if m:
            try:
                return datetime.strptime("".join(m.groups()), "%d%b%Y").strftime("%Y-%m-%d")
            except ValueError:
                pass
        m = re.search(r"(20\d\d)-(\d\d)-(\d\d)", f.name)
        return "-".join(m.groups()) if m else f.name
    files = sorted((f for f in MAIN.glob(pattern) if not f.name.startswith("~$")), key=key)
    return files[-1] if files else None


def build_card(out_html):
    """Refresh the project card with the newest Projects Info and CWAR files, using the card's own reader."""
    card = newest("MODON_Project_Card*.html")
    if not card:
        return None
    files = [f for f in (newest("Projects Info*.xls*"), newest("CWAR*.xls*")) if f]
    try:
        r = subprocess.run(["node", str(Path(__file__).parent / "build_card.js"), str(card), str(out_html), *map(str, files)],
                           capture_output=True, text=True, timeout=900)
        print(r.stdout.strip(), r.stderr.strip()[-2000:], sep="\n")
        if r.returncode == 0 and out_html.exists():
            return out_html.read_text(encoding="utf-8")
    except (OSError, subprocess.TimeoutExpired) as e:
        print("project card not refreshed:", e)
    print("using the project card as uploaded (Excel files not applied)")
    return card.read_text(encoding="utf-8")


def card_data(page):
    """(progress map {contract id: {planP, revP, actP, sv, progDate}}, its source file, CWAR records) from the card."""
    dec = json.JSONDecoder()
    try:
        data, _ = dec.raw_decode(page, page.index("var DATA = ") + 11)
        cwar, _ = dec.raw_decode(page, page.index("var CWAR = ") + 11)
    except ValueError:
        return {}, "", {}
    prog = data.get("prog") or {}
    return prog.get("map") or {}, prog.get("src", ""), cwar


def contract_id(num, page, ids):
    if num in ids:
        return ids[num]
    head = page[page.find('<header class="top"'):][:4000]
    m = CONTRACT_ID.search(head) or CONTRACT_ID.search(re.sub(r"base64,[A-Za-z0-9+/=]+", "", page))
    return m.group(0) if m else None


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def facts(page):
    """Headline figures from a report: physical % actual and plan, SPI, data date, week, P6 finish."""
    s = re.sub(r"base64,[A-Za-z0-9+/=]+", "", page)
    f = {}
    m = re.search(r'class="label">Physical % complete</span>\s*<div class="big">(.*?)</div>', s, re.S)
    if m:
        nums = re.findall(r"(\d+(?:\.\d+)?)%", text(m.group(1)))
        if nums:
            f["actual"] = float(nums[0])
        if len(nums) > 1:
            f["plan"] = float(nums[1])
    m = re.search(r"SPI\s*(?:\(physical\)\s*)?(\d+\.\d+)", text(s[s.find('class="tiles"'):][:4000]))
    if m:
        f["spi"] = float(m.group(1))
    m = re.search(r"Data date (\d{1,2}-[A-Za-z]{3}-\d{4})", s)
    if m:
        f["date"] = m.group(1)
    m = re.search(r"Weekly progress report · Week (\d+)", s)
    if m:
        f["week"] = m.group(1)
    m = re.search(r"P6 (?:finish|forecast finish)[^0-9<]*(\d{1,2}-[A-Za-z]{3}-\d{4})", text(s[s.find('class="tiles"'):][:4000]))
    if m:
        f["finish"] = m.group(1)
    m = re.search(r"<title>(.*?)</title>", s)
    f["title"] = text(m.group(1)) if m else ""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    f["h1"] = text(m.group(1)) if m else ""
    return f


def slug(week_folder):
    return week_folder.replace(" - ", "-").replace(" ", "-")


def project_name(project):
    return (project / "README.md").read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()


def collect():
    projects = []
    for p in sorted(x for x in ROOT.glob("[0-9][0-9]-*") if x.is_dir()):
        weeks = []
        for w in sorted((x for x in (p / "4-Weekly update").iterdir() if x.is_dir() and NEW_NAME.match(x.name)), reverse=True):
            reports = sorted((w / "Generated Report").glob("*.html"))
            if reports:
                weeks.append((w, reports[0]))
        projects.append((p, weeks))
    return projects


def status(f):
    sv = f.get("sv")
    if sv is not None:   # same bands as the project card's executive summary
        if sv > -1:
            return "good", "متقدم على الخطة" if sv >= 1 else "حسب الخطة"
        if sv > -15:
            return "warn", "متأخر"
        return "crit", "متأخر جداً"
    spi = f.get("spi")
    if spi is None and "actual" in f and "plan" in f and f["plan"]:
        spi = f["actual"] / f["plan"]
    if spi is None:
        return "none", "—"
    if spi >= 1.0:
        return "good", "متقدم على الخطة" if spi > 1.02 else "حسب الخطة"
    if spi >= 0.9:
        return "warn", "متأخر قليلاً"
    return "crit", "متأخر"


CSS = """
@font-face{font-family:"Plex Arabic";font-weight:400;src:url(fonts/ibm-plex-sans-arabic-arabic-400-normal.woff2) format("woff2");unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF}
@font-face{font-family:"Plex Arabic";font-weight:600;src:url(fonts/ibm-plex-sans-arabic-arabic-600-normal.woff2) format("woff2");unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF}
@font-face{font-family:"Plex Arabic";font-weight:400;src:url(fonts/ibm-plex-sans-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Plex Arabic";font-weight:600;src:url(fonts/ibm-plex-sans-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"Plex Mono";font-weight:500;src:url(fonts/ibm-plex-mono-latin-500-normal.woff2) format("woff2")}
:root{--bg:#f6f6f3;--panel:#fff;--ink:#17201d;--ink-2:#5b6661;--rule:#dfe2dd;--grid:#e9ebe7;--accent:#1f6f5c;
--good:#1b7a46;--good-bg:#e3f3e9;--warn:#9a6300;--warn-bg:#fbefd8;--crit:#b3261e;--crit-bg:#fbe5e3;--plan:#8a948f;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--bg:#121816;--panel:#1a2220;--ink:#e6ebe8;--ink-2:#9aa6a0;--rule:#2c3633;--grid:#25302d;--accent:#5cc3a5;
--good:#5fd08e;--good-bg:#173226;--warn:#f0b54a;--warn-bg:#3a2d12;--crit:#ff8a80;--crit-bg:#3d1c1a;--plan:#7d8984;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 "Plex Arabic",system-ui,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:28px 16px 48px}
h1{font-size:1.7rem;margin:0 0 2px;line-height:1.3}.sub{color:var(--ink-2);margin:0 0 20px}
.sum{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:0 0 22px}
.sum div{background:var(--panel);border:1px solid var(--rule);border-radius:8px;padding:12px 14px}
.sum .flt{cursor:pointer;transition:border-color .15s,box-shadow .15s}.sum .flt:hover{border-color:var(--accent)}
.sum .flt.on{border-color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}
.card.hide{display:none}
.sum b{display:block;font:500 1.6rem "Plex Mono",monospace}.sum span{color:var(--ink-2);font-size:.85rem}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px}
.card{background:var(--panel);border:1px solid var(--rule);border-radius:10px;padding:16px;display:grid;gap:10px;align-content:start}
.card.empty{opacity:.55}
.top{display:flex;gap:10px;align-items:flex-start;justify-content:space-between}
.num{font:500 .8rem "Plex Mono",monospace;color:var(--ink-2);border:1px solid var(--rule);border-radius:6px;padding:1px 7px;flex:none}
.name{font-weight:600;line-height:1.45}.en{color:var(--ink-2);font-size:.82rem;direction:ltr;text-align:right}
.fig{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}.fig span{color:var(--ink-2);font-size:.85rem}
.fig .big{font:500 1.9rem/1 "Plex Mono",monospace;direction:ltr;color:var(--ink)}.planv{margin-inline-start:auto}
.st{display:flex;align-items:center;gap:10px}.spi{font:500 .85rem "Plex Mono",monospace;color:var(--ink-2);direction:ltr;unicode-bidi:isolate}
.bar{height:8px;background:var(--grid);border-radius:99px;position:relative;overflow:visible;direction:ltr}
.bar i{position:absolute;inset:0 auto 0 0;border-radius:99px;background:var(--accent)}
.bar u{position:absolute;top:-4px;bottom:-4px;width:2px;background:var(--plan)}
.pill{display:inline-block;font-size:.8rem;font-weight:600;border-radius:99px;padding:2px 10px}
.pill.good{color:var(--good);background:var(--good-bg)}.pill.warn{color:var(--warn);background:var(--warn-bg)}
.pill.crit{color:var(--crit);background:var(--crit-bg)}.pill.none{color:var(--ink-2);background:var(--grid)}
.meta{display:flex;flex-wrap:wrap;gap:6px 14px;color:var(--ink-2);font-size:.85rem}.meta bdi{color:var(--ink)}
.links{display:flex;flex-wrap:wrap;gap:8px}
.links a{color:var(--accent);text-decoration:none;font-weight:600;font-size:.88rem;border:1px solid var(--rule);border-radius:99px;padding:4px 12px}
.links a.main{background:var(--accent);color:var(--bg);border-color:var(--accent)}
.links a:hover{border-color:var(--accent)}
details{font-size:.85rem;color:var(--ink-2)}details a{color:var(--accent);margin-inline-end:10px;white-space:nowrap}
footer{margin-top:28px;color:var(--ink-2);font-size:.82rem}
"""


def card(num, name, f, links, older):
    cls, label = status(f)
    has = "actual" in f
    bar = ""
    if has:
        plan = f.get("plan")
        bar = (f'<div class="bar" title="Actual {f["actual"]}%{f", plan " + str(plan) + "%" if plan is not None else ""}">'
               f'<i style="width:{min(f["actual"], 100)}%"></i>'
               + (f'<u style="left:{min(plan, 100)}%"></u>' if plan is not None else "") + "</div>")
    big = ""
    if has:
        big = (f'<div class="fig"><span class="big">{f["actual"]:.1f}%</span><span>فعلي</span>'
               + (f'<span class="planv">المخطط <bdi dir="ltr">{f["plan"]:.1f}%</bdi></span>' if "plan" in f else "") + "</div>")
    spi = f'<span class="spi">SPI <bdi dir="ltr">{f["spi"]:.2f}</bdi></span>' if "spi" in f else ""
    if f.get("sv") is not None:
        spi += f'<span class="spi">الفارق <bdi dir="ltr">{f["sv"]:+.1f}%</bdi></span>'
    meta = []
    if "date" in f:
        meta.append(f'تاريخ البيانات <bdi dir="ltr">{f["date"]}</bdi>')
    if "week" in f:
        meta.append(f'الأسبوع {f["week"]}')
    if "finish" in f:
        meta.append(f'الانتهاء المتوقع (P6) <bdi dir="ltr">{f["finish"]}</bdi>')
    hist = ""
    if older:
        hist = "<details><summary>الأسابيع السابقة / Earlier weeks</summary>" + "".join(
            f'<a href="{href}">{html.escape(lbl)}</a>' for lbl, href in older) + "</details>"
    return f"""<article class="card{'' if links else ' empty'}" data-st="{cls if links else 'none'}">
  <div class="top"><div><div class="name">{html.escape(name)}</div><div class="en">{html.escape(f.get('h1', ''))}</div></div><span class="num">{num}</span></div>
  {big}{bar}
  <div class="st"><span class="pill {cls}">{label}</span>{spi}</div>
  <div class="meta">{''.join(f'<span>{m}</span>' for m in meta) or '<span>لا يوجد تقرير بعد / No report yet</span>'}</div>
  <div class="links">{''.join(f'<a class="{c}" href="{h}">{t}</a>' for t, h, c in links)}</div>
  {hist}
</article>"""


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    for item in out.iterdir():
        if item.name != ".git":
            shutil.rmtree(item) if item.is_dir() else item.unlink()
    (out / ".nojekyll").write_text("", encoding="utf-8")
    (out / "fonts").mkdir()
    for font in FONTS.glob("*.woff2"):
        shutil.copy2(font, out / "fonts" / font.name)

    with tempfile.TemporaryDirectory() as tmp:
        card_page = build_card(Path(tmp) / "card.html") if MAIN.is_dir() else None
    prog, prog_src, _ = card_data(card_page) if card_page else ({}, "", {})
    ids_file = Path(__file__).parent / "cwar_ids.json"
    ids = json.loads(ids_file.read_text(encoding="utf-8")) if ids_file.exists() else {}
    reports = {}   # contract id -> weekly report link, for the project card

    cards, counts = [], {"good": 0, "warn": 0, "crit": 0, "none": 0}
    reported = 0
    for project, weeks in collect():
        num, name = project.name[:2], project_name(project)
        if not weeks:
            cards.append(card(num, name, {}, [], []))
            continue
        reported += 1
        d = out / num
        d.mkdir()
        latest_week, latest = weeks[0]
        page = latest.read_text(encoding="utf-8")
        cid = contract_id(num, page, ids)
        f = facts(page)   # progress figures from the weekly report itself (not CWAR)
        if f.get("actual") is not None and f.get("plan") is not None:
            f["sv"] = round(f["actual"] - f["plan"], 2)
        if cid:
            reports[cid] = {"url": f"{num}/", "num": num, "week": f.get("week", ""), "date": f.get("date", "")}
        counts[status(f)[0]] += 1
        (d / "index.html").write_text(site_report(page, latest), encoding="utf-8")
        links = [("التقرير / Report", f"{num}/", "main")]
        for pdf in sorted((latest_week / "Generated Report").glob("*.pdf")):
            arabic = bool(re.search(r"[؀-ۿ]", pdf.name))
            links.append(("PDF عربي" if arabic else "PDF English", f"{RAW}/{quote(pdf.relative_to(ROOT).as_posix())}", ""))
        older = []
        for w, rep in weeks:
            name_html = f"{slug(w.name)}.html"
            (d / name_html).write_text(site_report(rep.read_text(encoding="utf-8"), rep), encoding="utf-8")
            if w != latest_week:
                older.append((w.name.split(" - ")[1], f"{num}/{name_html}"))
        cards.append(card(num, name, f, links, older))

    now = datetime.now(timezone.utc) + timedelta(hours=3)
    page = f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Project Tracker</title>
{'<base target="_top">' if card_page else ''}
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<h1>تقارير التقدم الأسبوعية</h1>
<p class="sub">تقارير تقدم المشاريع الأسبوعية · يُحدَّث تلقائياً عند رفع أي تقرير جديد · نسب الإنجاز الفعلية (Physical % complete) من التقارير الأسبوعية</p>
<div class="sum">
  <div class="flt on" data-f="all" title="عرض كل المشاريع"><b>{reported}</b><span>مشروع لديه تقرير / projects reported</span></div>
  <div class="flt" data-f="good" title="اضغط لعرض هذه المشاريع فقط"><b style="color:var(--good)">{counts['good']}</b><span>حسب الخطة أو متقدم (الفارق أعلى من −1%)</span></div>
  <div class="flt" data-f="warn" title="اضغط لعرض هذه المشاريع فقط"><b style="color:var(--warn)">{counts['warn']}</b><span>متأخر (الفارق من −1% إلى −15%)</span></div>
  <div class="flt" data-f="crit" title="اضغط لعرض هذه المشاريع فقط"><b style="color:var(--crit)">{counts['crit']}</b><span>متأخر جداً (الفارق −15% أو أقل)</span></div>
</div>
<div class="cards">
{chr(10).join(cards)}
</div>
{FILTER_JS}
<footer>آخر تحديث / Last updated: <bdi dir="ltr">{now:%d-%b-%Y %H:%M}</bdi> (توقيت الرياض)</footer>
</div>
</body>
</html>
"""
    if card_page:
        (out / "reports.html").write_text(page, encoding="utf-8")
        (out / "index.html").write_text(merge_card(card_page, reports), encoding="utf-8")
    else:
        (out / "index.html").write_text(page, encoding="utf-8")
    print(f"site built: {reported} projects with reports (progress from the weekly reports)")



# ---- saving report edits straight back to the repository --------------------------------------------
# On the website, the report's "✎ Edit → Save" commits the edited page to the same file in the repository
# (GitHub contents API, with a GitHub token the editor enters once in their browser). The two snippets
# below are added only to the website copy and are taken out again before the page is committed.
SAVE_HOOK_OLD = "    if (standalone) {\n      const name = "
SAVE_HOOK_NEW = ("    /*site-save*/if (standalone && window.__siteSave) { try { await window.__siteSave(pageWith(next)); edits = next; stop(); "
                 "leaves().forEach(e => { delete e.dataset.edited; }); apply(); say(\"Saved to the repository. The website updates in about 2 minutes.\", 8000); } "
                 "catch (err) { save.disabled = false; cancel.hidden = false; say(String((err && err.message) || err)); } return; }/*/site-save*/\n")
SITE_SAVE_JS = """<script id="site-save">
window.__siteSave = async function (html) {
  var REPO = __REPO__, PATH = __PATH__, API = "https://api.github.com/repos/" + REPO + "/contents/" + PATH.split("/").map(encodeURIComponent).join("/");
  html = html.replace(/<script id="site-save">[\\s\\S]*?<\\/script>\\n?/g, "").replace(/\\/\\*site-save\\*\\/[\\s\\S]*?\\/\\*\\/site-save\\*\\/\\n/g, "");
  var token = ""; try { token = localStorage.getItem("gh-token") || ""; } catch (e) {}
  if (!token) {
    token = (prompt("للحفظ في الريبو مباشرة أدخل GitHub token (مرة واحدة على هذا الجهاز).\\nأنشئه من GitHub: Settings → Developer settings → Fine-grained tokens، للريبو " + REPO + " بصلاحية Contents: Read and write.") || "").trim();
    if (!token) throw new Error("لم يتم الحفظ: لا يوجد GitHub token.");
  }
  var h = { "Authorization": "Bearer " + token, "Accept": "application/vnd.github+json" };
  var cur = await fetch(API + "?ref=main", { headers: h, cache: "no-store" });
  if (cur.status === 401 || cur.status === 403) { try { localStorage.removeItem("gh-token"); } catch (e) {} throw new Error("الـ token غير صالح أو بدون صلاحية كتابة. حاول مرة أخرى."); }
  if (!cur.ok) throw new Error("تعذر الوصول للملف في الريبو (" + cur.status + ").");
  var sha = (await cur.json()).sha;
  var bytes = new TextEncoder().encode(html), bin = "";
  for (var i = 0; i < bytes.length; i += 32768) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 32768));
  var res = await fetch(API, { method: "PUT", headers: h, body: JSON.stringify({ message: "Edit report from the website: " + PATH.split("/").pop(), content: btoa(bin), sha: sha, branch: "main" }) });
  if (!res.ok) { var t = ""; try { t = (await res.json()).message || ""; } catch (e) {} if (res.status === 401 || res.status === 403) { try { localStorage.removeItem("gh-token"); } catch (e) {} } throw new Error("فشل الحفظ في الريبو (" + res.status + ") " + t); }
  try { localStorage.setItem("gh-token", token); } catch (e) {}
};
</script>"""


def site_report(page, path):
    """The website copy of a report: its Save button commits the edited page back to its file in the repository."""
    head = re.search(r'<meta charset="?utf-8"?>', page[:5000], re.I)   # the real <head> (reports have no </head> tag)
    if SAVE_HOOK_OLD not in page or not head:
        return page
    rel = path.relative_to(ROOT).as_posix()
    js = SITE_SAVE_JS.replace("__REPO__", json.dumps(REPO)).replace("__PATH__", json.dumps(rel))
    page = page.replace(SAVE_HOOK_OLD, SAVE_HOOK_NEW + SAVE_HOOK_OLD, 1)
    return page[:head.end()] + "\n" + js + page[head.end():]


CARD_PATCHES = [
    ('<td class="num" data-sort="${r.b||""}">${r.b?fmtSAR(r.b):"—"}</td>',
     '<td class="num" data-sort="${r.cv||""}">${r.cv?fmtSAR(r.cv):"—"}</td>'),
    ('"مدير المشروع","الميزانية المعتمدة","الإنجاز الفعلي"', '"مدير المشروع","قيمة العقد","الإنجاز الفعلي"'),
    ('const tot = list.reduce((a,r)=>a+(r.b||0),0);', 'const tot = list.reduce((a,r)=>a+(r.cv||0),0);'),
    ('<div class="k">الميزانية المعتمدة — SAR</div></div>\n    <div class="dk"><div class="v">${avg!==null',
     '<div class="k">قيمة العقود — SAR</div></div>\n    <div class="dk"><div class="v">${avg!==null'),
    ('cv:c?(c.cacv||c.ocv||0):0};\n  }).sort((a,b)=>b.b-a.b);', 'cv:c?(c.cacv||c.ocv||0):0};\n  }).sort((a,b)=>b.cv-a.cv);'),
    # project managers: list every PM, also those with no contracts under the current filter
    ('    rows = dirAgg(by);\n  }',
     '    if(kind==="pm" && window.__pmNames) window.__pmNames().forEach(n=>{ if(!by[n]) by[n]=[]; });\n    rows = dirAgg(by);\n  }'),
]

FILTER_JS = """<script>
(function(){
  var boxes=document.querySelectorAll(".sum .flt"), cards=document.querySelectorAll(".cards .card");
  function apply(f){
    boxes.forEach(function(b){ b.classList.toggle("on", b.dataset.f===f); });
    cards.forEach(function(c){ c.classList.toggle("hide", f!=="all" && c.dataset.st!==f); });
    try{ var fr=window.frameElement; if(fr){ fr.style.height="300px"; fr.style.height=(document.documentElement.scrollHeight+20)+"px"; } }catch(e){}
  }
  boxes.forEach(function(b){ b.addEventListener("click", function(){
    apply(b.classList.contains("on") && b.dataset.f!=="all" ? "all" : b.dataset.f); }); });
})();
</script>"""

MERGE_HTML = """<div id="savPage" style="display:none"></div>
<div id="repPage" style="display:none;margin-top:14px">
  <iframe id="repFrame" src="reports.html" title="تقارير التقدم الأسبوعية" style="width:100%;border:0;min-height:80vh;display:block"></iframe>
</div>"""

MERGE_JS = """<style>
/* side menu: the page tabs and the data buttons in a column beside the page instead of a row above it */
@media(min-width:900px){
  .wrap.sideNav{display:flex;flex-direction:row-reverse;align-items:flex-start;gap:20px}
  .sideNav>.sideCol{flex:0 0 210px;position:sticky;top:14px;max-height:calc(100vh - 28px);overflow:auto;display:flex;flex-direction:column;gap:12px}
  .sideNav>.mainCol{flex:1 1 auto;min-width:0}
  .sideCol .tabs{flex-direction:column;margin:0;gap:6px}
  .sideCol .tabBtn{width:100%;text-align:right;padding:10px 14px}
  .sideCol .uplRow{flex-direction:column;align-items:stretch;margin:0;gap:8px}
  .sideCol .uplRow button{width:100%}
  .sideCol #uplStatus{font-size:11.5px;line-height:1.6}
}
@media(max-width:899px){.sideCol .tabs{overflow-x:auto;flex-wrap:nowrap}.sideCol .tabBtn{flex:none}}
#dirMore:not(:empty),#stMore:not(:empty){cursor:pointer}
.savT td.savTxt{white-space:pre-line;font-size:11.5px;line-height:1.6;min-width:220px;max-width:340px;color:#3c5561}
.savT td.num .sb{display:block;font-size:10.5px;color:#5E7783;font-weight:600}
#stPage.stDone .ex2T th:nth-child(n+5),#stPage.stDone .ex2T td:nth-child(n+5){display:none}
#dirMore:not(:empty)::after,#stMore:not(:empty)::after{content:"  ·  عرض الكل ⌄";color:#006666;font-weight:800;text-decoration:underline}
@media(min-width:1100px){.ex2HeroKpis{grid-template-columns:repeat(6,minmax(0,1fr)) !important}}
.hkCount .hk2{line-height:1.5}
</style>
<script>
// Project Tracker: side menu, weekly reports tab, and a link from each project card to its weekly report.
(function(){
  var wrap=document.querySelector(".wrap"), t=wrap&&wrap.querySelector(":scope>.tabs");
  if(wrap && t){
    var side=document.createElement("nav"), main=document.createElement("div");
    side.className="sideCol"; main.className="mainCol";
    var upl=wrap.querySelector(":scope>.uplRow");
    Array.prototype.slice.call(wrap.childNodes).forEach(function(n){ if(n!==t && n!==upl) main.appendChild(n); });
    side.appendChild(t); if(upl) side.appendChild(upl);
    wrap.appendChild(side); wrap.appendChild(main); wrap.classList.add("sideNav");
  }
})();
(function(){
  var REPORTS = __REPORTS__;
  var tabs = document.querySelector(".tabs"), rep = document.getElementById("repPage");
  if(!tabs || !rep) return;
  var btn = document.createElement("button");
  btn.className = "tabBtn"; btn.id = "tabRep"; btn.type = "button"; btn.textContent = "تقارير التقدم الأسبوعية";
  tabs.appendChild(btn);
  var pages = ["execPage","ongPage","olPage","dirPage","stPage","page","hint","savPage"];
  btn.addEventListener("click", function(){
    tabs.querySelectorAll(".tabBtn").forEach(function(b){ b.classList.remove("active"); });
    btn.classList.add("active");
    pages.forEach(function(id){ var e=document.getElementById(id); if(e) e.style.display="none"; });
    var sb=document.querySelector(".selbox"); if(sb) sb.style.display="none";
    rep.style.display="";
    fit(); setTimeout(fit,300);
    if(location.hash!=="#reports") history.replaceState(null,"","#reports");
  });
  tabs.addEventListener("click", function(e){
    var b=e.target.closest(".tabBtn");
    if(b && b!==btn){ rep.style.display="none"; btn.classList.remove("active"); if(location.hash==="#reports") history.replaceState(null,"",location.pathname); }
  }, true);
  var fr=document.getElementById("repFrame");
  function fit(){ try{ fr.style.height=(fr.contentDocument.documentElement.scrollHeight+20)+"px"; }catch(e){} }
  fr.addEventListener("load", function(){ fit(); setTimeout(fit,500); });
  window.addEventListener("resize", fit);
  if(location.hash==="#reports") btn.click();

  // الوفورات (savings) page, from the newest «الوفورات» workbook in main files
  var SAV = __SAVINGS__;
  var sav=document.getElementById("savPage");
  if(SAV && sav){
    var sbtn=document.createElement("button"); sbtn.className="tabBtn"; sbtn.id="tabSav"; sbtn.type="button"; sbtn.textContent="الوفورات";
    tabs.insertBefore(sbtn, btn);
    var seg="all", sec="all", q="";
    var fmt=function(v){ return (v===null||v===undefined)?"—":(typeof fmtSAR==="function"?fmtSAR(v):String(v)); };
    var escH=function(x){ return String(x==null?"":x).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];}); };
    var cell=function(r,k){ var v=r[k]; return v!==null&&v!==undefined ? fmt(v) : (r[k+"_t"]?escH(r[k+"_t"]):"—"); };
    var segs=[["all","الكل"],["exec","تحت التنفيذ"],["done","المكتملة"],["svc","الخدمات (إيصال الخدمات)"]];
    function rows(){
      return SAV.rows.filter(function(r){
        if(seg!=="all" && r.grp!==seg) return false;
        if(sec!=="all" && r.sector!==sec) return false;
        if(q){ var h=(r.name+" "+(r.code||"")+" "+r.sector+" "+(r.works||"")+" "+(r.prop||"")).toLowerCase(); if(h.indexOf(q)<0) return false; }
        return true; });
    }
    function sum(list,k){ return list.reduce(function(a,r){ return a+(typeof r[k]==="number"?r[k]:0); },0); }
    function render(){
      var list=rows(), tc=sum(list,"cv"), ts=sum(list,"tot"), us=sum(list,"used"), av=sum(list,"avail");
      var pidIdx=(typeof buildPidIdx==="function")?buildPidIdx():{};
      var secs=[]; SAV.rows.forEach(function(r){ if(secs.indexOf(r.sector)<0) secs.push(r.sector); });
      var body=list.map(function(r,i){
        var idx=r.code?pidIdx[r.code]:undefined, pct=(typeof r.tot==="number"&&r.cv)?(r.tot/r.cv*100):null;
        return '<tr'+(idx!==undefined?' class="clkRow" data-idx="'+idx+'" title="اضغط لفتح بطاقة المشروع"':'')+'><td class="rank">'+(i+1)+'</td>'+
          '<td class="nm">'+escH(r.name)+'<span class="sb">'+escH(r.code||"")+(r.code?" · ":"")+escH(r.sector)+' · '+({exec:"تحت التنفيذ",done:"مكتمل",svc:"خدمات"}[r.grp])+'</span></td>'+
          '<td class="num" data-sort="'+(r.cv||"")+'">'+fmt(r.cv)+'</td>'+
          '<td class="num" data-sort="'+(typeof r.tot==="number"?r.tot:"")+'">'+cell(r,"tot")+(pct!==null?'<span class="sb">'+pct.toFixed(1)+'% من العقد</span>':'')+'</td>'+
          '<td class="num" data-sort="'+(typeof r.used==="number"?r.used:"")+'">'+cell(r,"used")+'</td>'+
          '<td class="num" data-sort="'+(typeof r.avail==="number"?r.avail:"")+'">'+(typeof r.avail==="number"&&r.avail>0?'<b style="color:#006666">'+fmt(r.avail)+'</b>':cell(r,"avail"))+'</td>'+
          '<td class="savTxt">'+escH(r.works||"—")+'</td><td class="savTxt">'+escH(r.prop||"—")+'</td></tr>';
      }).join("");
      sav.innerHTML='<div class="dirHead" style="background:linear-gradient(135deg,#0E3B36,#3E7A2E)"><div><h2>الوفورات</h2>'+
        '<div class="sub">'+escH(SAV.title)+' · المصدر: '+escH(SAV.file)+' (القيم بدون ضريبة القيمة المضافة)</div></div>'+
        '<div class="dirKpis"><div class="dk"><div class="v">'+list.length+'</div><div class="k">مشروع</div></div>'+
        '<div class="dk"><div class="v">'+fmt(tc)+'</div><div class="k">قيمة العقود — SAR</div></div>'+
        '<div class="dk"><div class="v" style="color:#9FE8B8">'+fmt(ts)+'</div><div class="k">إجمالي الوفر — SAR</div></div>'+
        '<div class="dk"><div class="v">'+fmt(us)+'</div><div class="k">الوفر المستخدم في أعمال — SAR</div></div>'+
        '<div class="dk"><div class="v" style="color:#FFE08A">'+fmt(av)+'</div><div class="k">الوفر المتاح حالياً — SAR</div></div></div></div>'+
        '<div class="segBar" style="margin-top:14px">'+segs.map(function(x){ return '<button type="button" class="segBtn savSeg'+(seg===x[0]?" active":"")+'" data-v="'+x[0]+'">'+x[1]+'</button>'; }).join("")+'</div>'+
        '<div class="segBar" style="margin-top:8px"><button type="button" class="segBtn sm savSec'+(sec==="all"?" active":"")+'" data-v="all">كل القطاعات</button>'+
          secs.map(function(x){ return '<button type="button" class="segBtn sm savSec'+(sec===x?" active":"")+'" data-v="'+escH(x)+'">'+escH(x)+'</button>'; }).join("")+'</div>'+
        '<div class="dirFilter"><input id="savQ" type="text" placeholder="فلترة بالاسم أو الكود أو الأعمال…" value="'+escH(q)+'"></div>'+
        '<div class="exCard dirCard" style="overflow-x:auto"><table class="ex2T savT"><thead><tr><th class="rank">#</th><th>المشروع</th><th>قيمة العقد</th><th>إجمالي الوفر</th><th>الوفر المستخدم</th><th>الوفر المتاح حالياً</th><th>الأعمال المنفذة</th><th>المقترحات</th></tr></thead><tbody>'+
        (body||'<tr><td colspan="8" style="text-align:center;padding:16px">لا نتائج</td></tr>')+'</tbody></table></div>';
      sav.querySelectorAll(".savSeg").forEach(function(b){ b.onclick=function(){ seg=b.dataset.v; render(); }; });
      sav.querySelectorAll(".savSec").forEach(function(b){ b.onclick=function(){ sec=b.dataset.v; render(); }; });
      var qi=document.getElementById("savQ"); qi.oninput=function(){ q=qi.value.trim().toLowerCase(); var p=qi.selectionStart; render(); var n=document.getElementById("savQ"); n.focus(); n.setSelectionRange(p,p); };
    }
    sbtn.addEventListener("click", function(){
      tabs.querySelectorAll(".tabBtn").forEach(function(b){ b.classList.remove("active"); });
      sbtn.classList.add("active");
      pages.concat(["repPage"]).forEach(function(id){ var e=document.getElementById(id); if(e) e.style.display="none"; });
      var sb=document.querySelector(".selbox"); if(sb) sb.style.display="none";
      render(); sav.style.display="";
      if(location.hash!=="#savings") history.replaceState(null,"","#savings");
    });
    tabs.addEventListener("click", function(e){
      var b=e.target.closest(".tabBtn");
      if(b && b!==sbtn){ sav.style.display="none"; sbtn.classList.remove("active"); if(location.hash==="#savings") history.replaceState(null,"",location.pathname); }
    }, true);
    if(location.hash==="#savings") sbtn.click();
  }

  // «المقاولين»: one menu item for contractors, design offices and supervision contracts, with a switch between them
  (function(){
    var cont=document.getElementById("tabCont"), des=document.getElementById("tabDes"), cons=document.getElementById("tabCons"), dp=document.getElementById("dirPage");
    if(!cont || !des || !cons || !dp) return;
    des.style.display="none"; cons.style.display="none";
    var KINDS={cont:cont, des:des, cons:cons};
    function sw(){
      var k=(typeof curDirKind!=="undefined")?curDirKind:null;
      if(!KINDS[k] || getComputedStyle(dp).display==="none") return;
      cont.classList.add("active");
      var bar=dp.querySelector(".consSw");
      if(!bar){ bar=document.createElement("div"); bar.className="segBar consSw"; bar.style.margin="0 0 12px";
        bar.innerHTML='<button type="button" class="segBtn" data-k="cont">المقاولين</button><button type="button" class="segBtn" data-k="des">مكاتب التصميم</button><button type="button" class="segBtn" data-k="cons">عقود الإشراف</button>';
        dp.insertBefore(bar, dp.firstChild);
        bar.addEventListener("click", function(e){ var b=e.target.closest("[data-k]"); if(b) KINDS[b.dataset.k].click(); }); }
      bar.querySelectorAll("[data-k]").forEach(function(b){ b.classList.toggle("active", b.dataset.k===k); });
    }
    new MutationObserver(sw).observe(dp,{childList:true});
    [cont,des,cons].forEach(function(b){ b.addEventListener("click", function(){ setTimeout(sw,0); }); });
  })();

  // every project manager named in CWAR (any status) or in All Projects (design / execution PM)
  window.__pmNames=function(){
    var set={};
    try{ Object.keys(CWAR).forEach(function(k){ var n=(CWAR[k].pm||"").trim(); if(n) set[n]=1; }); }catch(e){}
    try{ ALL.forEach(function(p){ [p.dpm,p.epm].forEach(function(n){ n=(n||"").trim(); if(n) set[n]=1; }); }); }catch(e){}
    return Object.keys(set);
  };
  // "show all" for the lists that stop at 30 rows
  if(typeof renderStatus==="function"){ var rs=renderStatus, last=null;
    // finished projects: no progress % or health indicator (columns التصميم / التنفيذ / المؤشر and their tiles)
    var DONE=["Completed Project","Project Closed"];
    function tidyDone(st){
      var pg=document.getElementById("stPage"); if(!pg) return;
      var done=DONE.indexOf(st)>=0; pg.classList.toggle("stDone",done);
      if(!done) return;
      pg.querySelectorAll("div").forEach(function(d){
        if(d.children.length<=3 && /^(متوسط التصميم|متوسط التنفيذ|متعثرة)$/.test((d.lastElementChild||{}).textContent||"")) d.style.display="none";
      });
    }
    renderStatus=function(){ last=arguments; var r=rs.apply(this,arguments); tidyDone(arguments[0]); return r; };
    window.__rerenderStatus=function(){ if(last){ rs.apply(null,last); tidyDone(last[0]); } }; }
  document.addEventListener("click", function(e){
    var n=e.target.closest("#dirMore, #stMore"); if(!n || !n.textContent.trim()) return;
    window.__showAll=true;
    if(n.id==="dirMore" && typeof renderDir==="function" && typeof curDirKind!=="undefined") renderDir(curDirKind);
    if(n.id==="stMore" && window.__rerenderStatus) window.__rerenderStatus();
    window.__showAll=false;
  });

  // a "number of projects" card first in the hero cards of the executive and ongoing-works summaries
  function countCard(pageId){
    var pg=document.getElementById(pageId); if(!pg || typeof ALL==="undefined") return;
    var k=pg.querySelector(".ex2HeroKpis");
    if(!k || k.querySelector(".hkCount")) return;
    var list=ALL, by=function(st){ return list.filter(function(p){ return p.st===st; }).length; }, sub;
    if(pageId==="ongPage"){
      list=ALL.filter(function(p){ return p.st==="Ongoing Projects"||p.st==="Under Design"; });
      var seg=(typeof ongSeg!=="undefined")?ongSeg:"all", cats=(typeof ongCats!=="undefined")?ongCats:[];
      var PH={exec:"Execution",design:"Design",utility:"Utilities"}[seg];
      if(PH) list=list.filter(function(p){ return (p.ph||"").trim()===PH; });
      if(cats.length) list=list.filter(function(p){ return cats.indexOf(p.cat||"غير مصنف")>=0; });
      sub=by("Ongoing Projects")+" قيد التنفيذ · "+by("Under Design")+" قيد التصميم";
    } else {
      sub=by("Ongoing Projects")+" جاري · "+by("Under Design")+" قيد التصميم · "+by("Completed Project")+" مكتمل";
    }
    var d=document.createElement("div"); d.className="hk hkCount";
    d.innerHTML='<div class="hv">'+list.length+'</div><div class="hk2">عدد المشاريع — '+sub+'</div>';
    k.insertBefore(d,k.firstChild);
  }
  ["execPage","ongPage"].forEach(function(id){
    var pg=document.getElementById(id); if(!pg) return;
    countCard(id);
    new MutationObserver(function(){ countCard(id); }).observe(pg,{childList:true,subtree:true});
  });

  // link from the project card to the weekly report
  function linkFor(idx){
    var old=document.getElementById("repLink"); if(old) old.remove();
    var p=(typeof ALL!=="undefined")?ALL[idx]:null; if(!p) return;
    var ids=[p.idD,p.idE];
    try{ var rc=relatedCwar(p); [rc.design,rc.exec].concat(rc.extras||[]).forEach(function(c){ if(c&&c.pid) ids.push(c.pid); }); }catch(e){}
    var hit=null; ids.forEach(function(i){ if(i&&!hit&&REPORTS[String(i).trim()]) hit=REPORTS[String(i).trim()]; });
    if(!hit) return;
    var a=document.createElement("a");
    a.id="repLink"; a.href=hit.url;
    a.textContent="📄 التقرير الأسبوعي للمشروع"+(hit.week?" — الأسبوع "+hit.week:"")+(hit.date?" (بيانات "+hit.date+")":"")+" ←";
    a.style.cssText="display:inline-block;margin-top:12px;padding:8px 16px;border-radius:20px;background:#fff;color:#006666;font-weight:800;font-size:13px;text-decoration:none";
    var h=document.querySelector("#page .phead"); if(h) h.appendChild(a);
  }
  if(typeof show==="function"){ var orig=show; show=function(idx){ var r=orig.apply(this,arguments); linkFor(idx); return r; }; }
})();
</script>"""


def _num(v):
    if isinstance(v, (int, float)):
        return float(v)
    t = str(v or "").replace(",", "").strip()
    try:
        return float(t)
    except ValueError:
        return None


def savings_data():
    """Rows of the newest «الوفورات» workbook in main files: the updated execution sheet (projects under
    execution and completed projects) and the services sheet."""
    f = newest("الوفورات*.xls*")
    if not f:
        return None
    try:
        import openpyxl
    except ImportError:
        print("savings page skipped: openpyxl not installed")
        return None
    wb = openpyxl.load_workbook(f, data_only=True, read_only=True)
    names = wb.sheetnames
    main = next((n for n in names if "محدث" in n), None) or next((n for n in names if "التنفيذ" in n), None)
    svc = next((n for n in names if "الخدمات" in n), None)
    out, title = [], ""

    def txt(v):
        return "" if v is None else str(v).strip()

    def val(row, i):
        v = row[i] if i < len(row) else None
        n = _num(v)
        return (n, None) if n is not None else (None, txt(v) or None)

    for sheet, default in ((main, "exec"), (svc, "svc")):
        if not sheet:
            continue
        grp, head = default, None
        for row in wb[sheet].iter_rows(values_only=True):
            row = list(row)
            first = txt(row[0]) if row else ""
            if first.startswith("وفورات") and sheet == main and not title:
                title = first
            if first.startswith("وفورات المشاريع المكتملة"):
                grp = "done"
                continue
            if len(row) > 1 and txt(row[1]) == "القطاع":
                head = [txt(x) for x in row]
                continue
            if head is None or not first.isdigit():
                continue
            col = lambda *keys: next((i for i, h in enumerate(head) if any(h.startswith(k) for k in keys)), None)
            ic, iname, icv = col("كود المشروع"), col("المشاريع"), col("قيمة العقد")
            itot = col("إجمالي الوفر", "الوفر المحقق / المتوقع")
            iused = next((i for i, h in enumerate(head) if h == "الوفر"), None)
            iav, iw, ip = col("الوفر المتاح"), col("الأعمال المنفذة", "الأعمال المعتمدة"), col("المقترحات")
            r = {"grp": grp, "sector": txt(row[1]), "code": txt(row[ic]) if ic is not None else "",
                 "name": txt(row[iname]) if iname is not None else "", "cv": _num(row[icv]) if icv is not None else None}
            for k, i in (("tot", itot), ("used", iused), ("avail", iav)):
                if i is not None:
                    r[k], t = val(row, i)
                    if t:
                        r[k + "_t"] = t
            r["works"] = txt(row[iw]) if iw is not None else ""
            r["prop"] = txt(row[ip]) if ip is not None else ""
            out.append(r)
    print(f"savings page: {len(out)} rows from {f.name} ({main}, {svc})")
    return {"file": f.name, "title": title, "rows": out}


def merge_card(card_page, reports):
    """The project card with the weekly reports added: a tab with every report and a link on each project's card."""
    s = card_page
    i = s.find('<div class="selbox"')
    if i > 0:
        s = s[:i] + MERGE_HTML + "\n  " + s[i:]
    s = re.sub(r"<title>.*?</title>", "<title>Project Tracker</title>", s, count=1, flags=re.S)
    # long lists stop at 30 rows: let the viewer show the rest ("عرض الكل")
    s = re.sub(r"const CAP ?= ?30;", "const CAP = window.__showAll ? 1e9 : 30;", s)
    # ongoing-projects list: show the contract value (CWAR current contract value) instead of the approved budget
    for old, new in CARD_PATCHES:
        if old in s:
            s = s.replace(old, new, 1)
        else:
            print("project card patch not applied (text not found):", old[:60])
    js = MERGE_JS.replace("__REPORTS__", json.dumps(reports, ensure_ascii=False))

    js = js.replace("__SAVINGS__", json.dumps(savings_data(), ensure_ascii=False).replace("</", "<\\/"))
    j = s.rfind("</body>")
    return s[:j] + js + s[j:] if j > 0 else s + js


if __name__ == "__main__":
    build(Path(sys.argv[1]))
