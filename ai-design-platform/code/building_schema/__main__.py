"""Command line: python -m building_schema <validate|dxf|preview|schema> ..."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .models import Building, load
from .validate import has_errors, validate


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="building_schema")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate", help="check a building JSON file")
    v.add_argument("file")
    for name in ("dxf", "preview"):
        p = sub.add_parser(name, help=f"export each level to {name.upper() if name == 'dxf' else 'PNG'}")
        p.add_argument("file")
        p.add_argument("-o", "--out", default="out")
    sub.add_parser("schema", help="print the JSON Schema")
    args = ap.parse_args(argv)

    if args.cmd == "schema":
        print(json.dumps(Building.model_json_schema(), indent=2, ensure_ascii=False))
        return 0

    b = load(args.file)
    issues = validate(b)
    for i in issues:
        print(i)
    if args.cmd == "validate":
        print("OK" if not issues else f"{len(issues)} issue(s)")
        return 1 if has_errors(issues) else 0
    if has_errors(issues):
        print("not exported: fix the errors first", file=sys.stderr)
        return 1

    stem = Path(args.file).stem
    if args.cmd == "dxf":
        from .export_dxf import export
        paths = export(b, args.out, stem)
    else:
        from .preview import preview
        paths = preview(b, args.out, stem)
    for p in paths:
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
