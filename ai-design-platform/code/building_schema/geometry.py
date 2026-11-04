"""Plan geometry shared by the DXF exporter and the PNG preview."""

from __future__ import annotations

import math
from dataclasses import dataclass

from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union

from .models import Building, Opening, Wall
from .validate import wall_line


@dataclass
class Frame:
    """A local frame on a wall: origin at the start, u along it, n to its left."""

    origin: tuple[float, float]
    u: tuple[float, float]
    n: tuple[float, float]

    @classmethod
    def of(cls, w: Wall) -> "Frame":
        dx, dy = w.end[0] - w.start[0], w.end[1] - w.start[1]
        length = math.hypot(dx, dy)
        u = (dx / length, dy / length)
        return cls(w.start, u, (-u[1], u[0]))

    def at(self, along: float, across: float = 0.0) -> tuple[float, float]:
        return (self.origin[0] + self.u[0] * along + self.n[0] * across,
                self.origin[1] + self.u[1] * along + self.n[1] * across)


def opening_rect(o: Opening, w: Wall, extra: float = 0.02) -> Polygon:
    f = Frame.of(w)
    a, z = o.position - o.width / 2, o.position + o.width / 2
    h = w.thickness / 2 + extra
    return Polygon([f.at(a, -h), f.at(z, -h), f.at(z, h), f.at(a, h)])


def level_walls(b: Building, level_id: str):
    """Wall outline for one level with door and window openings cut out."""
    walls = [w for w in b.walls if w.level == level_id]
    solid = unary_union([wall_line(w).buffer(w.thickness / 2, cap_style="square", join_style="mitre")
                         for w in walls])
    ids = {w.id for w in walls}
    cuts = [opening_rect(o, b.wall(o.host)) for o in b.openings if o.host in ids]
    return solid.difference(unary_union(cuts)) if cuts else solid


def door_symbol(o: Opening, w: Wall):
    """Leaf line and swing arc points for a door, in plan."""
    f = Frame.of(w)
    a, z = o.position - o.width / 2, o.position + o.width / 2
    side = 1 if o.swing == "left" else -1
    face = side * w.thickness / 2
    hinge_along, sweep = (a, z) if o.hinge == "start" else (z, a)
    hinge = f.at(hinge_along, face)
    tip = f.at(hinge_along, face + side * o.width)
    direction = 1 if sweep > hinge_along else -1
    arc = []
    for i in range(17):  # from fully open (leaf square to the wall) to closed
        t = math.radians(90 * i / 16)
        arc.append(f.at(hinge_along + direction * o.width * math.sin(t),
                        face + side * o.width * math.cos(t)))
    return [hinge, tip], arc


def window_symbol(o: Opening, w: Wall):
    """Two glass lines along the wall centre, inside the opening."""
    f = Frame.of(w)
    a, z = o.position - o.width / 2, o.position + o.width / 2
    g = w.thickness / 6
    return [[f.at(a, -g), f.at(z, -g)], [f.at(a, g), f.at(z, g)],
            [f.at(a, -w.thickness / 2), f.at(a, w.thickness / 2)],
            [f.at(z, -w.thickness / 2), f.at(z, w.thickness / 2)]]


def polygons(geom):
    if geom.is_empty:
        return []
    return list(geom.geoms) if hasattr(geom, "geoms") else [geom]
