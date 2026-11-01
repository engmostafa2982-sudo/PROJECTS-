"""Weekly folder names, and a tidy-up that keeps uploads in the right place.

Week folders are named by the Thursday each week starts on, from the first Thursday of October 2026:
"W01 - 01-Oct-2026", "W02 - 08-Oct-2026", ... The zero-padded number keeps them in order.
Reports dated before 01-Oct-2026 go in "W00 - 24-Sep-2026", which exists only in projects that need it.

Run as a script, it:
  - creates any missing week folders (with All Files, MD Files and Generated Report),
  - moves the contents of old-style folders ("W4") into the dated folder ("W04 - 22-Oct-2026"),
  - moves files dropped straight into a week folder into its All Files,
  - reads the weekly report's date from the uploaded file names and, when the files sit in the wrong
    week, moves the whole week (All Files, MD Files, Generated Report) to the week of that date.
    It only moves into an empty week, so nothing is ever overwritten; anything unclear is left alone.
"""
import re
import shutil
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIRST_THURSDAY = date(2026, 10, 1)
COUNT = 10
SUBFOLDERS = ["All Files", "MD Files", "Generated Report"]
OLD_NAME = re.compile(r"^W(\d+)$")
NEW_NAME = re.compile(r"^W(\d+) - ")


def start(n):
    return FIRST_THURSDAY + timedelta(weeks=n - 1)


def folder_name(n):
    return f"W{n:02d} - {start(n):%d-%b-%Y}"


def label(n):
    """Short column label for the tracker, e.g. "W04<br>22-Oct"."""
    return f"W{n:02d}<br>{start(n):%d-%b}"


WEEKS = [folder_name(n) for n in range(1, COUNT + 1)]


def week_of(day):
    """Week number a report dated `day` belongs to (0 for the week before W01)."""
    return (day - FIRST_THURSDAY).days // 7 + 1


MONTHS = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
SPREADSHEETS = (".xlsx", ".xlsb", ".xlsm", ".xls")
NOT_THE_REPORT = re.compile(r"look ?ahead|baseline|tracker|procurement|fir log|failed start", re.I)
SUBS = SUBFOLDERS


def _date(y, m, d):
    try:
        x = date(y, m, d)
    except ValueError:
        return None
    return x if FIRST_THURSDAY - timedelta(days=60) <= x <= FIRST_THURSDAY + timedelta(days=200) else None


def dates_in(text):
    """Dates written in a file name: 2026-10-26, 26-10-2026, 26.Oct.2026, Oct. 26, 2026, 10-26-2026 (month first)..."""
    s, out = text.lower(), []
    for y, m, d in re.findall(r"(?=(?<!\d)(20\d\d)[-./_ ](\d{1,2})[-./_ ](\d{1,2})(?!\d))", s):
        out.append(_date(int(y), int(m), int(d)))
    for y, mon, d in re.findall(r"(20\d\d)[-./ ]([a-z]{3})[a-z]*[-./ ](\d{1,2})(?!\d)", s):
        out.append(_date(int(y), MONTHS.get(mon, 0), int(d)))
    for a, b, y in re.findall(r"(?=(?<!\d)(\d{1,2})[-./_ ](\d{1,2})[-./_ ](20\d\d|\d\d)(?!\d))", s):
        a, b, y = int(a), int(b), 2000 + int(y) % 100
        out.append(_date(y, b, a) or _date(y, a, b))   # day first, else month first
    for d, mon, y in re.findall(r"(?<!\d)(\d{1,2})[-./ ]?([a-z]{3})[a-z]*\.?[-./ ,]*(20\d\d|\d\d)(?!\d)", s):
        out.append(_date(2000 + int(y) % 100, MONTHS.get(mon, 0), int(d)))
    for mon, d, y in re.findall(r"([a-z]{3})[a-z]*\.? (\d{1,2}),? (20\d\d)", s):
        out.append(_date(int(y), MONTHS.get(mon, 0), int(d)))
    return [x for x in out if x]


def report_date(week):
    """The weekly report's date, from the names of the files uploaded for that week (None if unclear)."""
    files = [f for f in (week / "All Files").rglob("*") if f.is_file() and f.name != "README.md" and not f.name.startswith("~$")]
    rel = lambda f: str(f.relative_to(week / "All Files"))
    groups = (
        [f for f in files if f.suffix.lower() in SPREADSHEETS and not NOT_THE_REPORT.search(rel(f))],
        [f for f in files if not NOT_THE_REPORT.search(rel(f))],
    )
    for group in groups:
        found = Counter(d for f in group for d in dates_in(rel(f)))
        if found:
            return max(found)
    return None


def has_files(folder):
    return folder.is_dir() and any(f.is_file() and f.name != "README.md" for f in folder.rglob("*"))


def merge(src, dst):
    """Move everything in src into dst; a file already in dst keeps the uploaded copy from src."""
    dst.mkdir(parents=True, exist_ok=True)
    for item in list(src.iterdir()):
        target = dst / item.name
        if item.is_dir() and target.is_dir():
            merge(item, target)
        else:
            if target.exists():
                target.unlink() if target.is_file() else shutil.rmtree(target)
            shutil.move(str(item), str(target))
    src.rmdir()


def tidy():
    for weekly in sorted(ROOT.glob("[0-9][0-9]-*/4-Weekly update")):
        for d in sorted(p for p in weekly.iterdir() if p.is_dir()):
            m = OLD_NAME.match(d.name)
            if m and 1 <= int(m.group(1)) <= COUNT:
                merge(d, weekly / folder_name(int(m.group(1))))
                print(f"renamed: {d.relative_to(ROOT)} -> {folder_name(int(m.group(1)))}")
        for n in range(1, COUNT + 1):
            week = weekly / folder_name(n)
            for sub in SUBFOLDERS:
                folder = week / sub
                if not folder.is_dir():
                    folder.mkdir(parents=True)
                    (folder / "README.md").write_text(f"# {sub}\n", encoding="utf-8")
            for f in sorted(p for p in week.iterdir() if p.is_file() and p.name != "README.md"):
                shutil.move(str(f), str(week / "All Files" / f.name))
                print(f"moved into All Files: {f.relative_to(ROOT)}")
        for week in sorted(p for p in weekly.iterdir() if p.is_dir() and NEW_NAME.match(p.name)):
            if not has_files(week / "All Files"):
                continue
            day = report_date(week)
            if day is None:
                continue
            target = weekly / folder_name(week_of(day))
            if target == week:
                continue
            if any(has_files(target / sub) for sub in SUBS):
                print(f"left in place (report dated {day:%d-%b-%Y}, but {target.name} already has files): {week.relative_to(ROOT)}")
                continue
            for sub in SUBS:
                if (week / sub).is_dir():
                    for item in list((week / sub).iterdir()):
                        if item.name != "README.md":
                            (target / sub).mkdir(parents=True, exist_ok=True)
                            shutil.move(str(item), str(target / sub / item.name))
                    if not (target / sub / "README.md").exists():
                        (target / sub / "README.md").write_text(f"# {sub}\n", encoding="utf-8")
            print(f"moved to the week of its report date {day:%d-%b-%Y}: {week.relative_to(ROOT)} -> {target.name}")


if __name__ == "__main__":
    tidy()
