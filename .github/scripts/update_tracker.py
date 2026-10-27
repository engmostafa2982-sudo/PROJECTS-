"""Rebuild the upload tracker in README.md: files per folder for every project, plus the latest uploads from git history."""
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
START, END = "<!-- tracker:start -->", "<!-- tracker:end -->"
FOLDERS = [("BOQ", "1-BOQ"), ("Drawing", "2-Project Drawing"), ("Baseline", "3-Baseline")]
WEEKS = [f"W{i}" for i in range(1, 11)]
RECENT = 30


def uploaded(folder):
    files = folder / "All Files"
    if not files.is_dir():
        return 0
    return sum(1 for p in files.rglob("*") if p.is_file() and p.name != "README.md" and not p.name.startswith("."))


def link(path, text):
    return f"[{text}]({quote(path.relative_to(ROOT).as_posix())}/All%20Files)"


def cell(folder):
    n = uploaded(folder)
    return link(folder, f"✅ {n}") if n else link(folder, "⬜")


def project_name(project):
    first = (project / "README.md").read_text(encoding="utf-8").splitlines()[0]
    return first.lstrip("# ").strip()


def recent_uploads():
    env = dict(os.environ, TZ="Asia/Riyadh")
    log = subprocess.run(
        ["git", "log", "--no-renames", "--diff-filter=A", "--name-only", "-z",
         "--date=format-local:%Y-%m-%d %H:%M", "--format=%x01%ad%x00%an",
         "--", ":(glob)[0-9]*/**/All Files/**"],
        cwd=ROOT, capture_output=True, text=True, env=env, check=True).stdout
    rows = []
    for entry in log.split("\x01")[1:]:
        date, author, *paths = [p.strip("\n") for p in entry.split("\x00")]
        for path in filter(None, paths):
            if Path(path).name == "README.md":
                continue
            project, _, rest = path.partition("/")
            where, _, name = rest.partition("/All Files/")
            rows.append(f"| {date} | {author} | {project[:2]} | {where} | {name.replace('|', '¦')} |")
            if len(rows) == RECENT:
                return rows
    return rows


def build():
    projects = sorted(p for p in ROOT.glob("[0-9][0-9]-*") if p.is_dir())
    head = ["#", "Project / المشروع"] + [label for label, _ in FOLDERS] + WEEKS
    out = [START, "",
           "## Upload tracker / متابعة الرفع",
           "",
           "_Updated automatically after every upload. ✅ n = number of files in **All Files**, ⬜ = nothing uploaded yet. Click a cell to open the folder._",
           "",
           "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    total = filled = 0
    for p in projects:
        cells = [cell(p / d) for _, d in FOLDERS] + [cell(p / "4-Weekly update" / w) for w in WEEKS]
        total += len(cells)
        filled += sum("✅" in c for c in cells)
        out.append(f"| {p.name[:2]} | [{project_name(p)}]({quote(p.name)}/) | " + " | ".join(cells) + " |")
    out[4:4] = [f"**{filled} of {total} folders have uploads.**", ""]
    out += ["", f"### Latest uploads / آخر الملفات المرفوعة (Riyadh time)", "",
            "| Date | Uploaded by | # | Folder | File |", "|---|---|---|---|---|"]
    out += recent_uploads() or ["| – | – | – | – | No uploads yet |"]
    out += ["", END]
    return "\n".join(out)


def main():
    text = README.read_text(encoding="utf-8")
    block = build()
    if START in text:
        text = re.sub(re.escape(START) + ".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    README.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
