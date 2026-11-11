"""Project dashboard (لوحة متابعة المشروع) for the Project Tracker website.

The dashboard follows the layout of MODON's follow-up workbook (لوحة متابعة): project information, performance
indicators, scope items with their progress, and challenges. Its figures come from two places:

  1. the latest generated weekly report of the project (always available once a report exists), and
  2. a MODON follow-up workbook uploaded to any week's All Files (sheets «المشاريع», «بنود الأعمال», «التحديات»),
     read from its Markdown copy in MD Files. Where it has a value, it is shown next to the weekly report's,
     with the date and source of each, so the two can be compared.

Every progress percentage is physical % complete. Values that no file gives yet are shown as «بانتظار البيانات».
"""
import html
import json
import re
from datetime import date, datetime
from pathlib import Path

PENDING = '<span class="pend">بانتظار البيانات</span>'
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
AR_MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def esc(s):
    return html.escape(str(s), quote=False)


def num(s):
    m = re.search(r"[-−]?\d[\d,]*(?:\.\d+)?", s or "")
    return float(m.group(0).replace(",", "").replace("−", "-")) if m else None


def parse_date(s):
    if isinstance(s, date):
        return s
    s = (s or "").strip()
    m = re.search(r"(\d{1,2})-([A-Za-z]{3})-(\d{4})", s)
    if m and m.group(2).title() in MONTHS:
        return date(int(m.group(3)), MONTHS.index(m.group(2).title()) + 1, int(m.group(1)))
    m = re.search(r"(20\d\d)-(\d\d)-(\d\d)", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def d_ar(d):
    """26-أكتوبر-2026, written left to right like the reports."""
    return f'<bdi dir="ltr">{d.day:02d}-{AR_MONTHS[d.month - 1]}-{d.year}</bdi>' if d else PENDING


def pct(x, digits=1, sign=False):
    if x is None:
        return PENDING
    s = f"{x:+.{digits}f}%" if sign else f"{x:.{digits}f}%"
    return f'<bdi dir="ltr">{s.replace("-", "−")}</bdi>'


def money(x):
    if x is None:
        return PENDING
    if x >= 1e6:
        return f'<bdi dir="ltr">{x / 1e6:,.2f}</bdi> مليون ريال'
    return f'<bdi dir="ltr">{x:,.0f}</bdi> ريال'


# ---------------------------------------------------------------- weekly report

def _ar_dict(page):
    m = re.search(r"const AR\s*=\s*(\{.*?\});?\s*\n", page, re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(1))
    except ValueError:
        return {}


def _section(page, title):
    i = page.find(f"<h2>{title}")
    if i < 0:
        return ""
    j = page.find("</section>", i)
    return page[i:j if j > 0 else None]


def _rows(block):
    out = []
    for tr in re.findall(r"<tr>(.*?)</tr>", block, re.S):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if cells:
            out.append(cells)
    return out


def report_data(page):
    """Figures for the dashboard from one generated weekly report (standard layout)."""
    s = re.sub(r"base64,[A-Za-z0-9+/=]+", "", page)
    ar = _ar_dict(s)
    tr = lambda x: ar.get(x, x)
    r = {"ar": ar}
    for label, value in re.findall(r'<div><span class="label">(.*?)</span><b[^>]*>(.*?)</b></div>', s):
        r[text(label)] = text(value)
    m = re.search(r'<div class="ar ar-title">(.*?)</div>', s, re.S)
    r["name_ar"] = text(m.group(1)) if m else ""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    r["name_en"] = text(m.group(1)) if m else ""
    m = re.search(r"Data date (\d{1,2}-[A-Za-z]{3}-\d{4})", s)
    r["date"] = parse_date(m.group(1)) if m else None
    m = re.search(r"Weekly progress report · Week (\d+)", s)
    r["week"] = m.group(1) if m else None
    m = re.search(r'<span class="mono">Project ID ([^<]+)</span>', s)
    r["id"] = m.group(1).strip() if m else ""

    tiles = {}
    for t in re.findall(r'<div class="tile">(.*?)</div>\s*(?=<div class="tile">|</div>)', s, re.S):
        lab = re.search(r'<span class="label">(.*?)</span>', t)
        if lab:
            tiles[text(lab.group(1))] = t
    t = tiles.get("Physical % complete", "")
    big = re.search(r'<div class="big">(.*?)</div>', t, re.S)
    nums = re.findall(r"(\d+(?:\.\d+)?)%", text(big.group(1))) if big else []
    r["actual"] = float(nums[0]) if nums else None
    r["plan"] = float(nums[1]) if len(nums) > 1 else None
    m = re.search(r"SPI\s*(\d+\.\d+)", text(t))
    r["spi"] = float(m.group(1)) if m else None
    m = re.search(r"revised plan (\d+(?:\.\d+)?)%", text(t))
    r["revised_plan"] = float(m.group(1)) if m else None
    t = text(tiles.get("Contract time elapsed", ""))
    m = re.search(r"(\d+(?:\.\d+)?)%", t)
    r["elapsed"] = float(m.group(1)) if m else None
    m = re.search(r"day (\d[\d,]*) of (\d[\d,]*)", t)
    r["days"] = (int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))) if m else None
    m = re.search(r"[Ff]orecast finish (\d{1,2}-[A-Za-z]{3}-\d{4})", t) or re.search(
        r"P6 (?:finish|forecast finish)[^0-9]*(\d{1,2}-[A-Za-z]{3}-\d{4})", text(s[s.find('class="tiles"'):][:4000]))
    r["finish"] = parse_date(m.group(1)) if m else None
    t = text(tiles.get("Invoiced to date (gross)", ""))
    m = re.search(r"(\d+(?:\.\d+)?)%", t)
    r["inv_pct"] = float(m.group(1)) if m else None
    m = re.search(r"([\d.,]+)\s*M SAR", t)
    r["inv_value"] = float(m.group(1).replace(",", "")) * 1e6 if m else None
    m = re.search(r"(\d+) invoices?", t)
    r["inv_count"] = int(m.group(1)) if m else None

    m = re.search(r'<div class="callout (crit|warn|good)">\s*<b>(.*?)</b>', s, re.S)
    r["headline"] = (m.group(1), tr(text(m.group(2)))) if m else None

    r["phases"] = []
    for c in _rows(_section(s, "Progress by phase")):
        if len(c) >= 7:
            pill = re.search(r'class="pill (\w+)"', c[6])
            r["phases"].append({"name": tr(text(c[0])), "weight": num(text(c[1])), "plan": num(text(c[2])),
                                "actual": num(text(c[3])), "state": pill.group(1) if pill else "",
                                "label": tr(text(c[6]))})
    r["issues"] = []
    for c in _rows(_section(s, "Open issues")):
        if len(c) >= 3:
            r["issues"].append((tr(text(c[0])), tr(text(c[1])), tr(text(c[2]))))
    cost = _section(s, "Cost and invoicing")
    kv = [(text(k), text(v)) for k, v in re.findall(r"<span>(.*?)</span>\s*<span>(.*?)</span>", cost, re.S)]
    cv = [(k, num(v)) for k, v in kv if re.search(r"contract value", k, re.I) and not re.search(r"incl", k, re.I)]
    cv = [x for x in cv if x[1]]
    revised = [x for x in cv if "revised" in x[0].lower()]
    r["contract_value"] = (revised or cv or [(None, None)])[0][1]
    r["consultant"] = tr(r.get("Consultant", ""))
    r["contractor"] = tr(r.get("Contractor", ""))
    r["pm"] = tr(r.get("MODON PM", ""))
    r["start"] = parse_date(r.get("Site handover", ""))
    r["end"] = parse_date(r.get("Contract completion", "") or r.get("Revised completion", ""))
    return r


# ---------------------------------------------------------------- MODON follow-up workbook

def _md_sheets(md):
    """{sheet name: {row number: {column letter: value}}} from a converted workbook."""
    sheets, cur, cols = {}, None, []
    for line in md.splitlines():
        if line.startswith("## Sheet: "):
            cur = sheets.setdefault(line[10:].strip(), {})
            cols = []
        elif cur is not None and line.startswith("|"):
            cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
            if cells and cells[0] == "Row":
                cols = cells[1:]
            elif cells and cells[0].isdigit() and cols:
                cur[int(cells[0])] = {k: v for k, v in zip(cols, cells[1:]) if v}
    return sheets


def _table(sheet, must):
    """Rows of a sheet as dicts keyed by the header row (the first row that contains `must`)."""
    head = next((n for n, row in sorted(sheet.items()) if must in row.values()), None)
    if head is None:
        return []
    names = sheet[head]
    return [{names[k]: v for k, v in row.items() if k in names} for n, row in sorted(sheet.items()) if n > head]


def _f(x):
    try:
        return float(str(x).replace(",", ""))
    except (TypeError, ValueError):
        return None


def modon_workbook(project, names):
    """The newest MODON follow-up workbook uploaded for this project, or None."""
    found = []
    for md in (project / "4-Weekly update").glob("W*/MD Files/*.md"):
        s = md.read_text(encoding="utf-8", errors="ignore")
        if "## Sheet: المشاريع" in s and "## Sheet: بنود الأعمال" in s:
            found.append((md.parent.parent.name, md, s))
    for week, md, s in sorted(found, reverse=True):
        sh = _md_sheets(s)
        rows = [r for r in _table(sh.get("المشاريع", {}), "المعرف") if r.get("المعرف")]
        if not rows:
            continue
        key = lambda x: re.sub(r"[\sـ–\-]+", "", x or "")
        pick = [r for r in rows if any(key(n) and (key(n) in key(r.get("اسم المشروع")) or key(r.get("اسم المشروع")) in key(n))
                                      for n in names)]
        row = pick[0] if pick else (rows[0] if len(rows) == 1 else None)
        if not row:
            continue
        pid = row["المعرف"]
        settings = sh.get("الإعدادات", {})
        day = None
        for r in settings.values():
            if r.get("B", "").startswith("تاريخ التقرير"):
                day = parse_date(r.get("C"))
        m = re.search(r"(\d{1,2})-(\d{1,2})-(20\d\d)", md.name)
        day = day or (date(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else None)
        items = [r for r in _table(sh.get("بنود الأعمال", {}), "بند الأعمال") if r.get("معرف المشروع") == pid and r.get("بند الأعمال")]
        challenges = [r.get("التحدي") for r in _table(sh.get("التحديات", {}), "التحدي")
                      if r.get("معرف المشروع") == pid and r.get("التحدي")]
        g = lambda k: row.get(k)
        return {
            "file": md.stem, "week": week, "date": day,
            "contractor": g("المقاول"), "start": parse_date(g("بداية المشروع")),
            "end": parse_date(g("نهاية المشروع التعاقدية")), "target": parse_date(g("نهاية المشروع المستهدفة")),
            "labour": _f(g("عدد العمالة")), "equipment": _f(g("عدد المعدات")),
            "contract_value": _f(g("قيمة العقد")), "inv_value": _f(g("قيمة المستخلصات")),
            "inv_count": _f(g("عدد المستخلصات")),
            "actual": (_f(g("الإنجاز الفعلي")) or 0) * 100 if g("الإنجاز الفعلي") else None,
            "recovery": (_f(g("النسبة حسب الجدول التصحيحي")) or 0) * 100 if g("النسبة حسب الجدول التصحيحي") else None,
            "items": [{"name": i.get("بند الأعمال"), "unit": i.get("الوحدة", ""), "total": _f(i.get("الكمية الإجمالية")),
                       "done": _f(i.get("الكمية المنفذة")), "pct": (_f(i.get("نسبة الإنجاز المعلنة")) or 0) * 100,
                       "check": i.get("تنبيه جودة البيانات", ""), "state": i.get("حالة البند", "")} for i in items],
            "challenges": challenges,
        }
    return None


# ---------------------------------------------------------------- page

def status(variance):
    """Same thresholds as the MODON follow-up workbook: within 5% = on plan, 5–10% behind = under watch, more = late."""
    if variance is None:
        return "none", "—"
    if variance >= -5:
        return "good", "ضمن الخطة"
    if variance >= -10:
        return "warn", "تحت المتابعة"
    return "crit", "متأخر"


def summary(project, page, names):
    """Everything the dashboard and the portfolio table need, merged from the report and the workbook."""
    r = report_data(page)
    w = modon_workbook(project, names + [r["name_ar"]])
    var = r["actual"] - r["plan"] if r["actual"] is not None and r["plan"] is not None else None
    return {"r": r, "w": w, "variance": var, "status": status(var)}


def _kpi(label, value, sub="", cls=""):
    return f'<div class="kpi {cls}"><span class="k">{label}</span><b>{value}</b><span class="s">{sub}</span></div>'


def _bar(p, plan=None, cls=""):
    p = max(0, min(p or 0, 100))
    u = f'<u style="left:{max(0, min(plan, 100))}%"></u>' if plan is not None else ""
    return f'<div class="bar {cls}"><i style="width:{p}%"></i>{u}</div>'


def item_class(p):
    return "crit" if p < 10 else ("good" if p >= 50 else "warn")


def page(num, name, info, links, css):
    r, w = info["r"], info["w"]
    cls, label = info["status"]
    rd = r["date"]
    src_r = f'التقرير الأسبوعي (الأسبوع {r["week"]}، بيانات {d_ar(rd)})' if r["week"] else "التقرير الأسبوعي"
    src_w = f'لوحة متابعة مدن ({d_ar(w["date"])})' if w else ""

    start = (w and w["start"]) or r["start"]
    end = (w and w["end"]) or r["end"]
    months = round((end - start).days / 30.44) if start and end else None
    ref = rd or date.today()
    left = (end - ref).days if end else None
    contractor = (w and w["contractor"]) or r["contractor"]
    cv = (w and w["contract_value"]) or r["contract_value"]
    inv_v = (w and w["inv_value"]) or r["inv_value"]
    inv_n = (w and w["inv_count"]) or r["inv_count"]
    inv_p = inv_v / cv * 100 if inv_v and cv else r["inv_pct"]
    inv_src = "لوحة متابعة مدن" if w and w["inv_value"] else "التقرير الأسبوعي"

    info_rows = [
        ("المقاول", esc(contractor) if contractor else PENDING),
        ("الاستشاري", esc(r["consultant"]) if r["consultant"] else PENDING),
        ("مدير المشروع - مدن", esc(r["pm"]) if r["pm"] else PENDING),
        ("بداية المشروع", d_ar(start)),
        ("نهاية المشروع التعاقدية", d_ar(end)),
        ("نهاية المشروع المستهدفة", d_ar(w["target"]) if w and w["target"] else PENDING),
        ("الانتهاء المتوقع (P6)", d_ar(r["finish"])),
        ("المدة الزمنية", f"{months} شهراً" if months else PENDING),
        ("عدد العمالة", f'<bdi dir="ltr">{w["labour"]:,.0f}</bdi>' if w and w["labour"] else PENDING),
        ("عدد المعدات", f'<bdi dir="ltr">{w["equipment"]:,.0f}</bdi>' if w and w["equipment"] else PENDING),
        ("الأيام المتبقية لنهاية العقد", (f'<bdi dir="ltr">{left}</bdi> يوماً' if left >= 0 else f'انقضى منذ <bdi dir="ltr">{-left}</bdi> يوماً') if left is not None else PENDING),
        ("حالة الأداء", f'<span class="pill {cls}">{label}</span>'),
    ]
    info_html = "".join(f"<div><span>{k}</span><b>{v}</b></div>" for k, v in info_rows)

    kpis = [
        _kpi("الزمن المنقضي من العقد", pct(r["elapsed"]), f'{left} يوماً متبقياً' if left is not None and left >= 0 else ""),
        _kpi("نسبة الإنجاز الفعلي", pct(r["actual"], 2), f'المتبقي: {pct(100 - r["actual"], 2)}' if r["actual"] is not None else ""),
        _kpi("النسبة المخططة حتى تاريخه", pct(r["plan"], 2),
             f'الخطة المعدلة: {pct(r["revised_plan"], 2)}' if r["revised_plan"] is not None else "حسب التقرير الأسبوعي"),
        _kpi("الفارق (فعلي − مخطط)", pct(info["variance"], 2, sign=True), label, cls),
        _kpi("قيمة المستخلصات", money(inv_v),
             (f'{pct(inv_p)} من قيمة العقد' if inv_p is not None else "") + (f' | {inv_n:.0f} مستخلصات' if inv_n else "")),
        _kpi("قيمة العقد", money(cv), f"المدة: {months} شهراً" if months else ""),
    ]
    compare = ""
    if w and (w["actual"] is not None or w["recovery"] is not None):
        wv = w["actual"] - w["recovery"] if w["actual"] is not None and w["recovery"] is not None else None
        compare = f"""<div class="note"><b>حسب {src_w}:</b> الإنجاز الفعلي {pct(w['actual'], 2)}، والنسبة حسب الجدول التصحيحي {pct(w['recovery'], 2)}،
والفارق {pct(wv, 2, sign=True)}. أما التقرير الأسبوعي للمقاول (بيانات {d_ar(rd)}) فيذكر {pct(r['actual'], 2)} مقابل {pct(r['plan'], 2)} مخططاً.
{"المستخلصات في اللوحة " + money(w["inv_value"]) + " مقابل " + money(r["inv_value"]) + " في التقرير الأسبوعي." if w["inv_value"] and r["inv_value"] and abs(w["inv_value"] - r["inv_value"]) > 1 else ""}</div>"""

    if w and w["items"]:
        cards = []
        for i in w["items"]:
            p = i["pct"] or 0
            qty = (f'المنفذ: <bdi dir="ltr">{i["done"]:,.0f} / {i["total"]:,.0f}</bdi> {esc(i["unit"])}'
                   if i["total"] else "الكمية الإجمالية: غير محددة")
            warn = ' <span class="chk" title="نسبة الإنجاز المعلنة لا تطابق نسبة الكميات">⚠ راجع البيانات</span>' if "راجع" in i["check"] else ""
            cards.append(f'<div class="item {item_class(p)}"><span class="nm">{esc(i["name"])}</span><b>{pct(p, 0)}</b>'
                         f'{_bar(p)}<span class="q">{qty}{warn}</span></div>')
        scope = f"""<section><h2>نطاق الأعمال – نسب الإنجاز</h2><p class="src">المصدر: {src_w}. اللون: أحمر أقل من 10%، ذهبي من 10% إلى 50%، أخضر 50% فأكثر.</p>
<div class="items">{''.join(cards)}</div></section>"""
    else:
        scope = ""
    phases = ""
    if r["phases"]:
        rows = "".join(
            f'<tr><td>{esc(p["name"])}</td><td class="n">{pct(p["weight"])}</td><td class="n">{pct(p["plan"])}</td>'
            f'<td class="n">{pct(p["actual"])}</td><td class="bc">{_bar(p["actual"], p["plan"])}</td>'
            f'<td><span class="pill {p["state"]}">{esc(p["label"])}</span></td></tr>' for p in r["phases"])
        phases = f"""<section><h2>التقدم حسب المرحلة</h2><p class="src">المصدر: {src_r}. يقاس بعدد ساعات العمل المخططة؛ الخط العمودي هو المخطط.</p>
<div class="scroll"><table><thead><tr><th>المرحلة</th><th class="n">الوزن</th><th class="n">المخطط</th><th class="n">الفعلي</th><th></th><th>الحالة</th></tr></thead>
<tbody>{rows}</tbody></table></div></section>"""

    if w and w["challenges"]:
        ch = "".join(f"<li>{esc(c)}</li>" for c in w["challenges"])
        challenges = f'<section><h2>التحديات</h2><p class="src">المصدر: {src_w}. عدد التحديات المفتوحة: {len(w["challenges"])}</p><ol class="ch">{ch}</ol></section>'
    elif r["issues"]:
        ch = "".join(f'<li><b>{esc(a)}</b> <span class="own">({esc(o)})</span><br><span>{esc(d)}</span></li>' for a, o, d in r["issues"])
        challenges = f'<section><h2>التحديات</h2><p class="src">المصدر: {src_r} — قسم المشكلات والمخاطر القائمة.</p><ol class="ch">{ch}</ol></section>'
    else:
        challenges = ""

    head = ""
    if r["headline"]:
        head = f'<div class="callout {r["headline"][0]}">{esc(r["headline"][1])}</div>'
    pending = []
    if not w:
        pending.append("لوحة متابعة مدن / بيانات المشروع (نهاية المشروع المستهدفة، عدد العمالة والمعدات، بنود الأعمال والتحديات)")
    elif not (w["labour"] and w["equipment"]):
        pending.append("عدد العمالة والمعدات")
    if inv_v is None:
        pending.append("المستخلصات")
    pend = (f'<p class="src">بيانات لم تُرفع بعد: {"، ".join(pending)}.</p>') if pending else ""
    title_ar = r["name_ar"] or name
    link_html = "".join(f'<a class="{c}" href="{h}">{t}</a>' for t, h, c in links)
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>لوحة متابعة {esc(title_ar)}</title>
<style>{css.replace('url(fonts/', 'url(../fonts/')}{DASH_CSS}</style>
</head>
<body>
<div class="wrap">
<p class="crumb"><a href="../">Project Tracker</a> ‹ <span>{num}</span></p>
<div class="dh"><div><h1>{esc(title_ar)}</h1><div class="en">{esc(r['name_en'])}</div></div>
<div class="dd"><span>تاريخ البيانات: {d_ar(rd)}{f" · الأسبوع {r['week']}" if r['week'] else ""}</span><span class="pill {cls}">{label}</span></div></div>
<div class="links top">{link_html}</div>
<div class="grid2">
<section><h2>مؤشرات الأداء</h2><div class="kpis">{''.join(kpis)}</div>{compare}{head}</section>
<section><h2>معلومات المشروع</h2><div class="info">{info_html}</div>{pend}</section>
</div>
{scope}
{phases}
{challenges}
<footer>نسب الإنجاز فعلية (Physical % complete) وتقاس بعدد ساعات العمل المخططة. حالة الأداء: الفارق أعلى من −5% ضمن الخطة، ومن −5% إلى −10% تحت المتابعة، وأقل من −10% متأخر.</footer>
</div>
</body>
</html>
"""


DASH_CSS = """
.crumb{margin:0 0 10px;color:var(--ink-2);font-size:.9rem}.crumb a{color:var(--accent)}
.dh{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;flex-wrap:wrap;margin-bottom:6px}
.dh h1{margin:0}.dh .en{color:var(--ink-2);font-size:.9rem;direction:ltr;text-align:right}
.dd{display:flex;gap:10px;align-items:center;color:var(--ink-2);font-size:.9rem;flex-wrap:wrap}
.links.top{margin:10px 0 16px}
section{background:var(--panel);border:1px solid var(--rule);border-radius:12px;padding:16px;margin:0 0 16px;min-width:0}
section h2{margin:0 0 10px;font-size:1.1rem}
.grid2{display:grid;grid-template-columns:1.4fr 1fr;gap:16px}.grid2 section{margin:0}
@media(max-width:860px){.grid2{grid-template-columns:1fr}}
.grid2+section,.grid2{margin-bottom:16px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}
.kpi{border:1px solid var(--rule);border-radius:10px;padding:10px 12px;display:grid;gap:4px}
.kpi .k{color:var(--ink-2);font-size:.85rem}.kpi b{font-size:1.45rem}.kpi .s{color:var(--ink-2);font-size:.8rem}
.kpi.crit b{color:var(--crit)}.kpi.warn b{color:var(--warn)}.kpi.good b{color:var(--good)}
.info{display:grid;gap:0}.info div{display:flex;justify-content:space-between;gap:12px;padding:7px 0;border-bottom:1px solid var(--rule)}
.info div:last-child{border-bottom:0}.info span{color:var(--ink-2)}.info b{text-align:left;font-weight:600}
.pend{color:var(--ink-3,var(--ink-2));font-weight:400;font-style:italic;font-size:.85rem}
.src{color:var(--ink-2);font-size:.82rem;margin:-4px 0 10px}
.note,.callout{margin-top:12px;padding:10px 12px;border-radius:8px;border:1px solid var(--rule);font-size:.9rem;line-height:1.7}
.callout.crit{border-color:var(--crit)}.callout.warn{border-color:var(--warn)}.callout.good{border-color:var(--good)}
.items{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px}
.item{border:1px solid var(--rule);border-top:4px solid var(--rule);border-radius:10px;padding:10px;display:grid;gap:6px}
.item.crit{border-top-color:var(--crit)}.item.warn{border-top-color:var(--warn)}.item.good{border-top-color:var(--good)}
.item .nm{font-weight:600}.item b{font-size:1.3rem}.item .q{color:var(--ink-2);font-size:.8rem}.chk{color:var(--warn)}
.item.crit .bar i{background:var(--crit)}.item.warn .bar i{background:var(--warn)}.item.good .bar i{background:var(--good)}
.scroll{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:.9rem}
th,td{padding:7px 8px;border-bottom:1px solid var(--rule);text-align:right;vertical-align:middle}th{color:var(--ink-2);font-weight:600}
td.n,th.n{text-align:left;white-space:nowrap}td.bc{min-width:110px}
.ch{margin:0;padding-inline-start:22px;display:grid;gap:8px;line-height:1.7}.ch .own{color:var(--ink-2);font-size:.85rem}.ch li span{color:var(--ink-2)}
"""
