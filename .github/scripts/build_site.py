"""Build the progress-report website (GitHub Pages) from the generated reports.

Usage: build_site.py OUT_DIR

  OUT_DIR/index.html        one page with every project: latest physical progress, plan, SPI, finish and links
  OUT_DIR/<NN>/index.html   project NN's latest report (a fixed link that always shows the newest week)
  OUT_DIR/<NN>/<week>.html  every earlier week's report, e.g. 05/W04-22-Oct-2026.html
The PDF buttons open the PDFs stored in the repository, so the site itself stays small.

Everything in OUT_DIR except .git is replaced, so the site always matches the repository.
"""
import html
import os
import re
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).parent))
from weeks import NEW_NAME  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REPO = os.environ.get("GITHUB_REPOSITORY", "engmostafa2982-sudo/PROJECTS-")
RAW = f"https://github.com/{REPO}/raw/main"
FONTS = ROOT / "_report-standard" / "tools" / "fonts"


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
    return f"""<article class="card{'' if links else ' empty'}">
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
        f = facts(page)
        counts[status(f)[0]] += 1
        (d / "index.html").write_text(page, encoding="utf-8")
        links = [("التقرير / Report", f"{num}/", "main")]
        for pdf in sorted((latest_week / "Generated Report").glob("*.pdf")):
            arabic = bool(re.search(r"[؀-ۿ]", pdf.name))
            links.append(("PDF عربي" if arabic else "PDF English", f"{RAW}/{quote(pdf.relative_to(ROOT).as_posix())}", ""))
        older = []
        for w, rep in weeks:
            name_html = f"{slug(w.name)}.html"
            shutil.copy2(rep, d / name_html)
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
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<h1>Project Tracker</h1>
<p class="sub">تقارير تقدم المشاريع الأسبوعية · Weekly project progress reports · يُحدَّث تلقائياً عند رفع أي تقرير جديد · نسب الإنجاز فعلية (Physical % complete)</p>
<div class="sum">
  <div><b>{reported}</b><span>مشروع لديه تقرير / projects reported</span></div>
  <div><b style="color:var(--good)">{counts['good']}</b><span>حسب الخطة أو متقدم / on or ahead of plan</span></div>
  <div><b style="color:var(--warn)">{counts['warn']}</b><span>متأخر قليلاً / slightly behind</span></div>
  <div><b style="color:var(--crit)">{counts['crit']}</b><span>متأخر / behind (SPI &lt; 0.90)</span></div>
</div>
<div class="cards">
{chr(10).join(cards)}
</div>
<footer>آخر تحديث / Last updated: <bdi dir="ltr">{now:%d-%b-%Y %H:%M}</bdi> (توقيت الرياض)</footer>
</div>
</body>
</html>
"""
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"site built: {reported} projects with reports")


if __name__ == "__main__":
    build(Path(sys.argv[1]))
