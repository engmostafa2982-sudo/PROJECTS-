"""Quick PNG preview of each level, for checking a design without AutoCAD.

Needs matplotlib 3.11 or later, which shapes Arabic text itself.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402

from .geometry import door_symbol, level_walls, polygons, window_symbol  # noqa: E402
from .models import Building  # noqa: E402


def preview_level(b: Building, level_id: str, path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(9, 9), dpi=150)
    site = b.site.boundary + [b.site.boundary[0]]
    ax.plot(*zip(*site), color="#3a7d44", linestyle="--", linewidth=1)

    for r in b.rooms:
        if r.level != level_id:
            continue
        poly = Polygon(r.boundary)
        ax.fill(*poly.exterior.xy, color="#eef3f8", zorder=1)
        p = poly.representative_point()
        ax.text(p.x, p.y, f"{r.name}\n{poly.area:.1f} m²", ha="center", va="center",
                fontsize=8, zorder=5)

    for poly in polygons(level_walls(b, level_id)):
        ax.fill(*poly.exterior.xy, color="#2b2b2b", zorder=3)
        for hole in poly.interiors:
            ax.fill(*hole.xy, color="#eef3f8", zorder=3)

    ids = {w.id for w in b.walls if w.level == level_id}
    for o in b.openings:
        if o.host not in ids:
            continue
        w = b.wall(o.host)
        if o.kind == "door":
            leaf, arc = door_symbol(o, w)
            ax.plot(*zip(*leaf), color="#c0392b", linewidth=1.2, zorder=4)
            ax.plot(*zip(*arc), color="#c0392b", linewidth=0.6, zorder=4)
        else:
            for seg in window_symbol(o, w):
                ax.plot(*zip(*seg), color="#1f78b4", linewidth=0.8, zorder=4)

    ax.set_aspect("equal")
    ax.set_title(f"{b.project.name} - {b.level(level_id).name}")
    ax.grid(color="#dddddd", linewidth=0.4)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def preview(b: Building, out_dir: str | Path, stem: str = "plan") -> list[Path]:
    out = Path(out_dir)
    return [preview_level(b, lv.id, out / f"{stem}_{lv.id}.png") for lv in b.levels]
