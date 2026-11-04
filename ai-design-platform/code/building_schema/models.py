"""Building Schema: the one format every design is stored in.

Every generator (templates, AI, manual input) produces a ``Building``; every
exporter (Revit add-in, DXF, IFC, BOQ) reads one. Units are metres and
coordinates are plan coordinates (x to the east, y to the north before the
site's north angle is applied).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

SCHEMA_VERSION = "0.1"

Point = tuple[float, float]


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid")


def _polygon(points: list[Point]) -> list[Point]:
    if len(points) > 1 and points[0] == points[-1]:
        points = points[:-1]
    if len(points) < 3:
        raise ValueError("a polygon needs at least 3 distinct points")
    return points


class ProjectInfo(_Model):
    name: str
    owner: str | None = None
    plot_number: str | None = None
    city: str | None = None


class Site(_Model):
    boundary: list[Point] = Field(description="Plot boundary, in order, not closed.")
    north_angle: float = Field(0.0, description="Degrees from plan-up to true north, clockwise.")

    _check_boundary = field_validator("boundary")(_polygon)


class Level(_Model):
    id: str
    name: str
    elevation: float = Field(description="Finished floor level in metres.")
    height: float = Field(gt=0, description="Floor-to-floor height in metres.")


class Wall(_Model):
    id: str
    level: str = Field(description="Id of the level the wall stands on.")
    type: str = Field(description="Wall type name, matched to a Revit wall type, e.g. EXT_200.")
    thickness: float = Field(gt=0, le=1.0)
    start: Point = Field(description="Start of the wall centreline.")
    end: Point = Field(description="End of the wall centreline.")
    height: float | None = Field(None, gt=0, description="Defaults to the level height.")


class Opening(_Model):
    id: str
    host: str = Field(description="Id of the wall the opening sits in.")
    kind: Literal["door", "window"]
    family: str = Field(description="Revit family name, e.g. Door_Single.")
    type: str = Field(description="Revit type name, e.g. 90x220.")
    position: float = Field(ge=0, description="Distance along the wall from its start to the opening centre.")
    width: float = Field(gt=0)
    height: float = Field(gt=0)
    sill: float = Field(0.0, ge=0, description="Height of the bottom of the opening above the floor.")
    hinge: Literal["start", "end"] = Field("start", description="Doors: hinge side, toward the wall start or end.")
    swing: Literal["left", "right"] = Field("left", description="Doors: opens to the left or right of the wall direction.")


class Room(_Model):
    id: str
    level: str
    name: str
    usage: str | None = Field(None, description="Machine-readable room type, e.g. majlis_men, kitchen.")
    boundary: list[Point] = Field(description="Room outline along wall centrelines, not closed.")

    _check_boundary = field_validator("boundary")(_polygon)


class Building(_Model):
    schema_version: Literal["0.1"] = SCHEMA_VERSION
    units: Literal["m"] = "m"
    project: ProjectInfo
    site: Site
    levels: list[Level] = Field(min_length=1)
    walls: list[Wall] = Field(default_factory=list)
    openings: list[Opening] = Field(default_factory=list)
    rooms: list[Room] = Field(default_factory=list)

    def level(self, level_id: str) -> Level:
        return next(lv for lv in self.levels if lv.id == level_id)

    def wall(self, wall_id: str) -> Wall:
        return next(w for w in self.walls if w.id == wall_id)


def load(path: str) -> Building:
    with open(path, encoding="utf-8") as f:
        return Building.model_validate_json(f.read())
