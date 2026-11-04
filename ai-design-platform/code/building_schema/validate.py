"""Geometric checks a Building must pass before it is sent to Revit or AutoCAD.

Errors would make the Revit add-in fail or produce a broken model; warnings
are worth a look but do not block export.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Literal

from shapely.geometry import LineString, Point, Polygon

from .models import Building, Opening, Wall

TOL = 0.01  # metres
MIN_WALL = 0.10
EDGE_CLEARANCE = 0.05  # gap kept between an opening and the end of its wall


@dataclass(frozen=True)
class Issue:
    severity: Literal["error", "warning"]
    code: str
    element: str
    message: str

    def __str__(self) -> str:
        return f"[{self.severity}] {self.code} {self.element}: {self.message}"


def wall_line(w: Wall) -> LineString:
    return LineString([w.start, w.end])


def opening_span(o: Opening) -> tuple[float, float]:
    return o.position - o.width / 2, o.position + o.width / 2


def validate(b: Building) -> list[Issue]:
    issues: list[Issue] = []
    err = lambda code, el, msg: issues.append(Issue("error", code, el, msg))  # noqa: E731
    warn = lambda code, el, msg: issues.append(Issue("warning", code, el, msg))  # noqa: E731

    # Unique ids across every element, because Revit maps them one to one.
    seen: set[str] = set()
    for el in [*b.levels, *b.walls, *b.openings, *b.rooms]:
        if el.id in seen:
            err("duplicate-id", el.id, "id is used more than once")
        seen.add(el.id)

    levels = {lv.id: lv for lv in b.levels}
    walls = {w.id: w for w in b.walls}
    site = Polygon(b.site.boundary)
    if not site.is_valid or site.area <= 0:
        err("site-invalid", "site", "site boundary is not a simple polygon")

    for w in b.walls:
        if w.level not in levels:
            err("unknown-level", w.id, f"level '{w.level}' does not exist")
        line = wall_line(w)
        if line.length < MIN_WALL:
            err("wall-too-short", w.id, f"length {line.length:.2f} m is below {MIN_WALL} m")
            continue
        if site.is_valid and not site.buffer(TOL).contains(line):
            warn("wall-outside-site", w.id, "wall leaves the plot boundary")
        lv = levels.get(w.level)
        if lv and w.height and w.height > lv.height + TOL:
            warn("wall-taller-than-level", w.id, f"{w.height} m is taller than level height {lv.height} m")

    # Every wall end should meet another wall on the same level; a free end
    # usually means a gap in the outline that Revit rooms will leak through.
    for w in b.walls:
        others = [wall_line(o) for o in b.walls if o.id != w.id and o.level == w.level]
        for name, pt in (("start", w.start), ("end", w.end)):
            if not any(o.distance(Point(pt)) <= TOL for o in others):
                warn("free-wall-end", w.id, f"{name} {pt} does not meet another wall")

    # Openings must fit inside their wall and must not cut through a junction.
    for o in b.openings:
        w = walls.get(o.host)
        if w is None:
            err("unknown-host", o.id, f"wall '{o.host}' does not exist")
            continue
        length = wall_line(w).length
        a, z = opening_span(o)
        if a < EDGE_CLEARANCE - TOL or z > length - EDGE_CLEARANCE + TOL:
            err("opening-outside-wall", o.id,
                f"spans {a:.2f}-{z:.2f} m but wall {w.id} is {length:.2f} m long")
        wall_h = w.height or (levels[w.level].height if w.level in levels else None)
        if wall_h and o.sill + o.height > wall_h + TOL:
            err("opening-too-tall", o.id, f"top at {o.sill + o.height:.2f} m is above wall height {wall_h} m")
        if o.kind == "window" and o.sill <= 0:
            warn("window-no-sill", o.id, "window sill is 0 m")
        line = wall_line(w)
        for other in b.walls:
            if other.id == w.id or other.level != w.level:
                continue
            for pt in (other.start, other.end):
                p = Point(pt)
                if line.distance(p) <= TOL:
                    d = line.project(p)
                    clear = other.thickness / 2
                    if a - clear < d < z + clear:
                        err("opening-on-junction", o.id,
                            f"wall {other.id} meets {w.id} at {d:.2f} m, inside the opening")

    by_wall: dict[str, list[Opening]] = {}
    for o in b.openings:
        by_wall.setdefault(o.host, []).append(o)
    for host, ops in by_wall.items():
        for o1, o2 in combinations(sorted(ops, key=lambda o: o.position), 2):
            if opening_span(o1)[1] > opening_span(o2)[0] - TOL:
                err("openings-overlap", o2.id, f"overlaps {o1.id} in wall {host}")

    # Rooms: valid outlines, no overlaps on the same level.
    polys: dict[str, Polygon] = {}
    for r in b.rooms:
        if r.level not in levels:
            err("unknown-level", r.id, f"level '{r.level}' does not exist")
        poly = Polygon(r.boundary)
        if not poly.is_valid or poly.area <= 0:
            err("room-invalid", r.id, "outline crosses itself or has no area")
            continue
        polys[r.id] = poly
    rooms = {r.id: r for r in b.rooms}
    for (id1, p1), (id2, p2) in combinations(polys.items(), 2):
        if rooms[id1].level == rooms[id2].level and p1.intersection(p2).area > TOL:
            err("rooms-overlap", id2, f"overlaps {id1} by {p1.intersection(p2).area:.2f} m2")

    return issues


def has_errors(issues: list[Issue]) -> bool:
    return any(i.severity == "error" for i in issues)
