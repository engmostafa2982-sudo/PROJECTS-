"""Weekly folder names, and a tidy-up that keeps uploads in the right place.

Week folders are named by the Thursday each week starts on, from the first Thursday of October 2026:
"W01 - 01-Oct-2026", "W02 - 08-Oct-2026", ... The zero-padded number keeps them in order.

Run as a script, it:
  - creates any missing week folders (with All Files, MD Files and Generated Report),
  - moves the contents of old-style folders ("W4") into the dated folder ("W04 - 22-Oct-2026"),
  - moves files dropped straight into a week folder into its All Files.
"""
import re
import shutil
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


if __name__ == "__main__":
    tidy()
