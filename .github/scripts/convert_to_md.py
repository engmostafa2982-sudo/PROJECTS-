"""Convert every file in each "All Files" folder to Markdown in the sibling "MD Files" folder.

Each generated file starts with a marker holding the source file's hash, so a file is
only reconverted when it changes, and its Markdown is removed when the source is deleted.

Every file is converted in its own process with a time limit, so one slow or broken file
can't block the rest; it gets a short warning page instead.

Usage:
  convert_to_md.py [--budget SECONDS]   convert pending files; exit 3 if the budget ran out first
  convert_to_md.py --one SRC TARGET     print the Markdown for one file (used internally)
"""
import hashlib
import re
import subprocess
import sys
import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR, OUT_DIR = "All Files", "MD Files"
MARKER = re.compile(r"^<!-- converted-from: (.+?) sha256: ([0-9a-f]{64}) -->")
PER_FILE_TIMEOUT = 600  # seconds
MORE_WORK = 3           # exit code: budget used up, run again
MARKITDOWN_EXTS = {".docx", ".pptx", ".xls", ".csv", ".html", ".htm", ".txt", ".json", ".xml", ".msg", ".epub"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_marker(md_path):
    with md_path.open(encoding="utf-8", errors="ignore") as f:
        m = MARKER.match(f.readline())
    return m.groups() if m else None


def pdf_to_markdown(src):
    from image_to_md import ocr_pdf
    text = subprocess.run(["pdftotext", "-layout", str(src), "-"],
                          capture_output=True, text=True, check=True).stdout
    if len(text.strip()) < 20:  # scanned PDF with no text layer
        return ocr_pdf(src) or "_No text found in this PDF._"
    pages = [p.rstrip() for p in text.split("\f")]
    return "\n\n".join(f"## Page {i}\n\n```text\n{p}\n```" for i, p in enumerate(pages, 1) if p.strip())


def size(src):
    n = src.stat().st_size
    return f"{n / 1e6:.1f} MB" if n >= 1e5 else f"{n / 1e3:.0f} KB"


def convert(src, target):
    ext = src.suffix.lower()
    if ext == ".md":
        return src.read_text(encoding="utf-8", errors="replace")
    if ext == ".xer":
        from xer_to_md import xer_to_markdown
        return xer_to_markdown(src)
    if ext in (".xlsx", ".xlsm"):
        from xlsx_to_md import xlsx_to_markdown
        return xlsx_to_markdown(src)
    if ext == ".pdf":
        return pdf_to_markdown(src)
    from image_to_md import IMAGE_EXTS, image_to_markdown
    if ext in IMAGE_EXTS:
        return image_to_markdown(src, target)
    if ext == ".zip":
        with zipfile.ZipFile(src) as z:
            names = [i.filename for i in z.infolist() if not i.is_dir()]
        return f"Archive ({size(src)}) containing {len(names)} file(s):\n\n" + "\n".join(f"- {n}" for n in names)
    if ext in MARKITDOWN_EXTS:
        from markitdown import MarkItDown
        return MarkItDown().convert(str(src)).text_content
    return (f"> ⚠️ No text version is available for **{ext or 'this'}** files ({size(src)}). "
            f"Open the original file in **All Files**.")


def convert_in_child(src, target):
    """Run convert() in a separate process so it can be killed if it takes too long."""
    try:
        r = subprocess.run([sys.executable, __file__, "--one", str(src), str(target)],
                           capture_output=True, timeout=PER_FILE_TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, f"took longer than {PER_FILE_TIMEOUT // 60} minutes"
    if r.returncode != 0:
        lines = r.stderr.decode("utf-8", "replace").strip().splitlines()
        return None, lines[-1] if lines else f"exit code {r.returncode}"
    return r.stdout.decode("utf-8", "replace"), None


def pending_work():
    """Yield (src, rel, target, digest) for files needing conversion; delete Markdown of removed sources."""
    for src_dir in sorted(p for p in ROOT.glob(f"[0-9]*/**/{SRC_DIR}") if p.is_dir()):
        out_dir = src_dir.parent / OUT_DIR
        out_dir.mkdir(exist_ok=True)
        sources = sorted(p for p in src_dir.rglob("*")
                         if p.is_file() and p.name != "README.md" and not p.name.startswith("."))
        # Use "report.md"; fall back to "report.pdf.md" when two sources share a name.
        stems = [p.relative_to(src_dir).with_suffix("") for p in sources]
        expected = set()
        for src, stem in zip(sources, stems):
            rel = src.relative_to(src_dir)
            name = (rel.as_posix() + ".md") if stems.count(stem) > 1 else (stem.as_posix().strip() + ".md")
            target = out_dir / name
            expected.add(target)
            digest = sha256(src)
            if not (target.exists() and read_marker(target) == (rel.as_posix(), digest)):
                yield src, rel, target, digest
        for md in out_dir.rglob("*.md"):
            if md not in expected and read_marker(md):
                md.unlink()
                print(f"removed: {md.relative_to(ROOT)}", flush=True)


def main(budget):
    start = time.monotonic()
    done = failed = 0
    for src, rel, target, digest in pending_work():
        if budget and time.monotonic() - start > budget:
            print(f"{done} converted, {failed} with warnings; time budget used, more files remain", flush=True)
            sys.exit(MORE_WORK)
        t = time.monotonic()
        text, error = convert_in_child(src, target)
        if error:
            text = f"> ⚠️ This file could not be converted automatically: {error}\n> Open the original file in **All Files**."
            failed += 1
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"<!-- converted-from: {rel.as_posix()} sha256: {digest} -->\n"
                          f"# {src.name}\n\n{text.strip()}\n", encoding="utf-8")
        print(f"{'WARNING' if error else 'converted'} ({time.monotonic() - t:.0f}s): "
              f"{src.relative_to(ROOT)}{' - ' + error if error else ''}", flush=True)
        done += 1
    print(f"{done} converted, {failed} with warnings", flush=True)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--one"]:
        sys.path.insert(0, str(Path(__file__).parent))
        sys.stdout.write(convert(Path(sys.argv[2]), Path(sys.argv[3])))
    else:
        main(int(sys.argv[2]) if sys.argv[1:2] == ["--budget"] else 0)
