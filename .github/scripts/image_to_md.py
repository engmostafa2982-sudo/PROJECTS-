"""Describe a photo as Markdown: the embedded image, its EXIF details (date, camera, GPS) and any text found by OCR."""
import os
import shutil
import subprocess
import tempfile
from urllib.parse import quote

from PIL import Image, ExifTags

try:
    from pillow_heif import register_heif_opener  # iPhone .heic photos
    register_heif_opener()
except ImportError:
    pass

OCR_LANGS = "ara+eng"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".webp", ".heic", ".heif"}


def ocr_image(path):
    if not shutil.which("tesseract"):
        return ""
    result = subprocess.run(["tesseract", str(path), "-", "-l", OCR_LANGS],
                            capture_output=True, text=True)
    return result.stdout.strip()


def ocr_pdf(path):
    """OCR every page of a scanned PDF (one with no text layer)."""
    if not (shutil.which("tesseract") and shutil.which("pdftoppm")):
        return ""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", "300", "-png", str(path), os.path.join(tmp, "p")], check=True)
        pages = sorted(os.listdir(tmp))
        return "\n\n".join(f"### Page {i}\n\n{ocr_image(os.path.join(tmp, p))}"
                           for i, p in enumerate(pages, 1))


def _gps(exif):
    info = exif.get_ifd(ExifTags.IFD.GPSInfo)
    try:
        def deg(v, ref):
            d = float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600
            return -d if ref in ("S", "W") else d
        return deg(info[2], info[1]), deg(info[4], info[3])
    except (KeyError, IndexError, TypeError, ZeroDivisionError):
        return None


def image_to_markdown(src, target):
    link = quote(os.path.relpath(src, target.parent).replace(os.sep, "/"))
    out = [f"![{src.name}]({link})", ""]
    rows = []
    with Image.open(src) as img:
        rows.append(("Size", f"{img.width} x {img.height}"))
        exif = img.getexif()
        sub = exif.get_ifd(ExifTags.IFD.Exif)
        taken = sub.get(ExifTags.Base.DateTimeOriginal) or exif.get(ExifTags.Base.DateTime)
        if taken:
            rows.append(("Date taken", str(taken).replace(":", "-", 2)))
        camera = " ".join(str(exif.get(t, "")).strip() for t in (ExifTags.Base.Make, ExifTags.Base.Model)).strip()
        if camera:
            rows.append(("Camera", camera))
        gps = _gps(exif)
        if gps:
            lat, lon = gps
            rows.append(("Location", f"[{lat:.6f}, {lon:.6f}](https://maps.google.com/?q={lat:.6f},{lon:.6f})"))
    out += ["| Field | Value |", "|---|---|"] + [f"| {k} | {v} |" for k, v in rows] + [""]
    text = ocr_image(src)
    if len(text) > 3:
        out += ["## Text in photo (OCR)", "", text]
    return "\n".join(out)
