"""Convert every file in each "All Files" folder to Markdown in the sibling "MD Files" folder.

Each generated file starts with a marker holding the source file's hash, so a file is
only reconverted when it changes, and its Markdown is removed when the source is deleted.
"""
import hashlib
import re
import sys
from pathlib import Path

from markitdown import MarkItDown

from image_to_md import IMAGE_EXTS, image_to_markdown, ocr_pdf
from xer_to_md import xer_to_markdown

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR, OUT_DIR = "All Files", "MD Files"
MARKER = re.compile(r"^<!-- converted-from: (.+?) sha256: ([0-9a-f]{64}) -->")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_marker(md_path):
    with md_path.open(encoding="utf-8", errors="ignore") as f:
        m = MARKER.match(f.readline())
    return m.groups() if m else None


def convert(converter, src, target):
    ext = src.suffix.lower()
    if ext == ".md":
        return src.read_text(encoding="utf-8", errors="replace")
    if ext == ".xer":
        return xer_to_markdown(src)
    if ext in IMAGE_EXTS:
        return image_to_markdown(src, target)
    text = converter.convert(str(src)).text_content
    if ext == ".pdf" and len(text.strip()) < 20:  # scanned PDF with no text layer
        text = ocr_pdf(src) or text
    return text


def main():
    converter = MarkItDown()
    changed, failed = 0, []
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
            name = (rel.as_posix() + ".md") if stems.count(stem) > 1 else (stem.as_posix() + ".md")
            target = out_dir / name
            expected.add(target)
            digest = sha256(src)
            if target.exists() and read_marker(target) == (rel.as_posix(), digest):
                continue
            try:
                text = convert(converter, src, target)
            except Exception as e:  # keep going so one bad file doesn't block the rest
                failed.append(f"{src.relative_to(ROOT)}: {e}")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"<!-- converted-from: {rel.as_posix()} sha256: {digest} -->\n"
                              f"# {src.name}\n\n{text.strip()}\n", encoding="utf-8")
            print(f"converted: {src.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
            changed += 1
        # Remove Markdown generated from sources that were deleted or renamed.
        for md in out_dir.rglob("*.md"):
            if md not in expected and read_marker(md):
                md.unlink()
                print(f"removed: {md.relative_to(ROOT)}")
                changed += 1
    print(f"{changed} change(s)")
    if failed:
        print("Failed to convert:\n  " + "\n  ".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
