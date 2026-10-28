"""Make a report a single self-contained file: embed its photos and fonts, and declare UTF-8.

Usage: python embed_assets.py REPORT.html
Photos are read from photos/ next to the report; fonts from fonts/ next to the report, else from this tools folder.
"""
import base64, re, sys
from pathlib import Path

FONTS = Path(__file__).parent / "fonts"


def b64(path):
    return base64.b64encode(path.read_bytes()).decode()


def font(here, name):
    p = here / "fonts" / name
    return p if p.exists() else FONTS / name


def embed(html):
    s = html.read_text(encoding="utf-8")
    here = html.parent
    s = re.sub(r'href="photos/([^"]+)" class="ph"><img src="photos/\1"',
               lambda m: f'href="#photo" class="ph"><img src="data:image/jpeg;base64,{b64(here / "photos" / m.group(1))}"', s)
    s = re.sub(r'url\(fonts/([^)]+)\)', lambda m: f'url(data:font/woff2;base64,{b64(font(here, m.group(1)))})', s)
    if not s.lstrip().lower().startswith("<!doctype"):
        s = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
             '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + s)
    left = re.findall(r'(?:src|href)="photos/[^"]+"|url\(fonts/', s)
    if left:
        sys.exit(f"not embedded: {left[:3]}")
    html.write_text(s, encoding="utf-8")
    print(f"{html}: {len(s) / 1e6:.1f} MB, self-contained")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        embed(Path(arg))
