"""Convert an Excel workbook to Markdown: one table per sheet, values only, empty rows and columns trimmed."""
import datetime
import warnings

import openpyxl

MAX_ROWS = 2000          # per sheet
MAX_EMPTY_RUN = 500      # stop reading a sheet after this many blank rows in a row (sheets often claim ~1M rows)


def fmt(v):
    if v is None:
        return ""
    if isinstance(v, datetime.datetime):
        return v.strftime("%Y-%m-%d") if v.time() == datetime.time(0) else v.strftime("%Y-%m-%d %H:%M")
    if isinstance(v, datetime.date):
        return v.isoformat()
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else f"{v:.4f}".rstrip("0").rstrip(".")
    return str(v).replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def col_name(i):
    name = ""
    while i:
        i, r = divmod(i - 1, 26)
        name = chr(65 + r) + name
    return name


def xlsx_to_markdown(path):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = []
    try:
        for ws in wb.worksheets:
            rows, empty, truncated = [], 0, False
            for r_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
                cells = [fmt(v) for v in row]
                if not any(cells):
                    empty += 1
                    if empty >= MAX_EMPTY_RUN:
                        break
                    continue
                empty = 0
                if len(rows) == MAX_ROWS:
                    truncated = True
                    break
                rows.append((r_idx, cells))
            out.append(f"## Sheet: {ws.title}\n")
            if not rows:
                out.append("_Empty sheet._\n")
                continue
            used = sorted({i for _, cells in rows for i, c in enumerate(cells) if c})
            out.append("| Row | " + " | ".join(col_name(i + 1) for i in used) + " |")
            out.append("|---" * (len(used) + 1) + "|")
            for r_idx, cells in rows:
                out.append(f"| {r_idx} | " + " | ".join(cells[i] if i < len(cells) else "" for i in used) + " |")
            if truncated:
                out.append(f"\n_Only the first {MAX_ROWS} filled rows are shown._")
            out.append("")
    finally:
        wb.close()
    return "\n".join(out)
