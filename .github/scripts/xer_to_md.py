"""Summarise a Primavera P6 .xer export as Markdown: project info, status counts and an activity table."""
from collections import Counter

STATUS = {"TK_NotStart": "Not Started", "TK_Active": "In Progress", "TK_Complete": "Completed"}
MILESTONES = {"TT_Mile", "TT_FinMile"}


def decode(raw):
    for enc in ("utf-8-sig", "cp1256"):  # cp1256 = Arabic Windows, common for P6 exports here
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode("latin-1")


def parse_xer(text):
    tables, name, fields = {}, None, []
    for line in text.splitlines():
        parts = line.rstrip("\r").split("\t")
        if parts[0] == "%T":
            name, fields = parts[1], []
            tables[name] = []
        elif parts[0] == "%F":
            fields = parts[1:]
        elif parts[0] == "%R" and name:
            tables[name].append(dict(zip(fields, parts[1:])))
    return tables


def cell(value):
    return (value or "").replace("|", "\\|").replace("\n", " ").strip()


def date(value):
    return (value or "")[:10]


def xer_to_markdown(path):
    tables = parse_xer(decode(path.read_bytes()))
    projects = tables.get("PROJECT", [])
    tasks = tables.get("TASK", [])
    wbs = {w.get("wbs_id"): w.get("wbs_name", "") for w in tables.get("PROJWBS", [])}
    day_hours = {}
    for c in tables.get("CALENDAR", []):
        try:
            day_hours[c.get("clndr_id")] = float(c.get("day_hr_cnt") or 8) or 8.0
        except ValueError:
            day_hours[c.get("clndr_id")] = 8.0

    out = []
    for p in projects:
        out += [f"## Project: {cell(p.get('proj_short_name'))}", "",
                "| Field | Value |", "|---|---|",
                f"| Data date | {date(p.get('last_recalc_date'))} |",
                f"| Planned start | {date(p.get('plan_start_date'))} |",
                f"| Scheduled finish | {date(p.get('scd_end_date'))} |",
                f"| Must finish by | {date(p.get('plan_end_date'))} |", ""]

    counts = Counter(STATUS.get(t.get("status_code"), t.get("status_code") or "-") for t in tasks)
    out += ["## Activity status", "", "| Status | Count |", "|---|---|"]
    out += [f"| {s} | {n} |" for s, n in sorted(counts.items())]
    out += [f"| **Total** | **{len(tasks)}** |", ""]

    out += ["## Activities", "",
            "| ID | Name | WBS | Type | Status | Start | Finish | Actual Start | Actual Finish | % Complete | Total Float (d) |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in tasks:
        try:
            tf = float(t.get("total_float_hr_cnt")) / day_hours.get(t.get("clndr_id"), 8.0)
            tf = f"{tf:g}" if tf == int(tf) else f"{tf:.1f}"
        except (TypeError, ValueError):
            tf = ""
        kind = "Milestone" if t.get("task_type") in MILESTONES else "Task"
        out.append("| " + " | ".join([
            cell(t.get("task_code")), cell(t.get("task_name")), cell(wbs.get(t.get("wbs_id"))), kind,
            STATUS.get(t.get("status_code"), cell(t.get("status_code"))),
            date(t.get("target_start_date")), date(t.get("target_end_date")),
            date(t.get("act_start_date")), date(t.get("act_end_date")),
            cell(t.get("phys_complete_pct")), tf]) + " |")
    if not tasks and not projects:
        out.append("_No PROJECT or TASK tables found in this file._")
    return "\n".join(out)
