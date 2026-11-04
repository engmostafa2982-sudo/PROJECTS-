"""Export each level of a Building to a DXF floor plan that opens in AutoCAD.

This is the open-source preview path. Final drawings come from Revit through
Design Automation; the layer names match the Revit DWG export mapping so both
paths produce the same layers.
"""

from __future__ import annotations

from pathlib import Path

import ezdxf
from ezdxf.enums import TextEntityAlignment
from shapely.geometry import Polygon

from .geometry import door_symbol, level_walls, polygons, window_symbol
from .models import Building

# name: (AutoCAD colour index, linetype, lineweight in 1/100 mm)
LAYERS = {
    "A-SITE": (3, "DASHED", 25),
    "A-WALL": (7, "Continuous", 50),
    "A-WALL-PATT": (8, "Continuous", 13),
    "A-DOOR": (2, "Continuous", 25),
    "A-GLAZ": (4, "Continuous", 18),
    "A-AREA-IDEN": (7, "Continuous", 18),
    "A-DIMS": (1, "Continuous", 13),
    "A-ANNO-TTLB": (7, "Continuous", 25),
}

TEXT_H = 0.25


def _setup(doc) -> None:
    doc.styles.add("ARABIC", font="arial.ttf")
    for name, (color, ltype, lw) in LAYERS.items():
        doc.layers.add(name, color=color, linetype=ltype, lineweight=lw)
    dim = doc.dimstyles.get("EZDXF")
    dim.dxf.dimtxt = TEXT_H
    dim.dxf.dimasz = 0.15
    dim.dxf.dimexe = 0.1
    dim.dxf.dimexo = 0.1
    dim.dxf.dimdec = 2
    dim.dxf.dimtxsty = "ARABIC"
    doc.header["$LTSCALE"] = 0.5


def _closed(msp, pts, layer):
    msp.add_lwpolyline(list(pts), close=True, dxfattribs={"layer": layer})


def export_level(b: Building, level_id: str, path: Path) -> Path:
    doc = ezdxf.new("R2018", setup=True, units=ezdxf.units.M)
    _setup(doc)
    msp = doc.modelspace()

    _closed(msp, b.site.boundary, "A-SITE")

    for poly in polygons(level_walls(b, level_id)):
        _closed(msp, poly.exterior.coords[:-1], "A-WALL")
        for hole in poly.interiors:
            _closed(msp, hole.coords[:-1], "A-WALL")
        hatch = msp.add_hatch(color=256, dxfattribs={"layer": "A-WALL-PATT"})
        hatch.set_pattern_fill("ANSI31", scale=0.02)
        hatch.paths.add_polyline_path(poly.exterior.coords[:-1], is_closed=True, flags=1)
        for hole in poly.interiors:
            hatch.paths.add_polyline_path(hole.coords[:-1], is_closed=True, flags=0)

    level_wall_ids = {w.id for w in b.walls if w.level == level_id}
    for o in b.openings:
        if o.host not in level_wall_ids:
            continue
        w = b.wall(o.host)
        if o.kind == "door":
            leaf, arc = door_symbol(o, w)
            msp.add_line(*leaf, dxfattribs={"layer": "A-DOOR"})
            msp.add_lwpolyline(arc, dxfattribs={"layer": "A-DOOR"})
        else:
            for seg in window_symbol(o, w):
                msp.add_line(*seg, dxfattribs={"layer": "A-GLAZ"})

    for r in b.rooms:
        if r.level != level_id:
            continue
        poly = Polygon(r.boundary)
        p = poly.representative_point()
        label = f"{r.name}\\P{poly.area:.2f} m²"
        msp.add_mtext(label, dxfattribs={"layer": "A-AREA-IDEN", "style": "ARABIC",
                                         "char_height": TEXT_H, "insert": (p.x, p.y),
                                         "attachment_point": 5})

    # Overall dimensions of the walls on this level.
    walls = level_walls(b, level_id)
    if not walls.is_empty:
        x0, y0, x1, y1 = walls.bounds
        msp.add_linear_dim(base=(x0, y0 - 1.2), p1=(x0, y0), p2=(x1, y0),
                           dimstyle="EZDXF", dxfattribs={"layer": "A-DIMS"}).render()
        msp.add_linear_dim(base=(x0 - 1.2, y0), p1=(x0, y0), p2=(x0, y1), angle=90,
                           dimstyle="EZDXF", dxfattribs={"layer": "A-DIMS"}).render()
        title = f"{b.project.name} - {b.level(level_id).name}"
        msp.add_text(title, height=TEXT_H * 2, dxfattribs={"layer": "A-ANNO-TTLB", "style": "ARABIC"}
                     ).set_placement((x0, y0 - 3.0), align=TextEntityAlignment.LEFT)

    path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(path)
    return path


def export(b: Building, out_dir: str | Path, stem: str = "plan") -> list[Path]:
    out = Path(out_dir)
    return [export_level(b, lv.id, out / f"{stem}_{lv.id}.dxf") for lv in b.levels]
