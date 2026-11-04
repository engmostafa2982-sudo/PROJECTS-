import json
from pathlib import Path

import ezdxf
import pytest
from pydantic import ValidationError

from building_schema import Building, load, validate
from building_schema.export_dxf import LAYERS, export

EXAMPLES = Path(__file__).parent.parent / "examples"


def codes(b):
    return {i.code for i in validate(b)}


def villa_dict():
    return json.loads((EXAMPLES / "villa_ground_floor.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", ["single_room", "villa_ground_floor"])
def test_examples_are_clean(name):
    assert validate(load(EXAMPLES / f"{name}.json")) == []


def test_committed_schema_is_current():
    committed = json.loads((Path(__file__).parent.parent / "schema" / "building.schema.json").read_text("utf-8"))
    assert committed == Building.model_json_schema()


def test_rejects_unknown_fields_and_bad_polygons():
    d = villa_dict()
    d["walls"][0]["colour"] = "red"
    with pytest.raises(ValidationError):
        Building.model_validate(d)
    d = villa_dict()
    d["rooms"][0]["boundary"] = [[0, 0], [1, 1]]
    with pytest.raises(ValidationError):
        Building.model_validate(d)


def test_duplicate_ids_and_unknown_references():
    d = villa_dict()
    d["walls"][1]["id"] = d["walls"][0]["id"]
    d["openings"][0]["host"] = "NOPE"
    d["rooms"][0]["level"] = "L9"
    assert {"duplicate-id", "unknown-host", "unknown-level"} <= codes(Building.model_validate(d))


def test_opening_outside_wall_and_too_tall():
    d = villa_dict()
    d["openings"][0]["position"] = 13.9  # 1.2 m door at the very end of a 14 m wall
    d["openings"][1]["height"] = 4.0
    assert {"opening-outside-wall", "opening-too-tall"} <= codes(Building.model_validate(d))


def test_opening_on_junction():
    d = villa_dict()
    door = next(o for o in d["openings"] if o["id"] == "D04")
    door["position"] = 6.0  # wall W01 meets W03 at 6.0 m
    assert "opening-on-junction" in codes(Building.model_validate(d))


def test_overlapping_openings_and_rooms():
    d = villa_dict()
    d["openings"].append({**d["openings"][0], "id": "DX", "position": 7.5})
    d["rooms"].append({**d["rooms"][0], "id": "RX", "boundary": [[4, 5], [8, 5], [8, 9], [4, 9]]})
    assert {"openings-overlap", "rooms-overlap"} <= codes(Building.model_validate(d))


def test_free_wall_end_is_a_warning():
    d = villa_dict()
    d["walls"].append({"id": "WX", "level": "L0", "type": "INT_100", "thickness": 0.1,
                       "start": [5, 13], "end": [5, 15]})
    issues = validate(Building.model_validate(d))
    assert {(i.code, i.severity) for i in issues if i.element == "WX"} == {("free-wall-end", "warning")}


def test_dxf_export(tmp_path):
    b = load(EXAMPLES / "villa_ground_floor.json")
    [path] = export(b, tmp_path, "villa")
    doc = ezdxf.readfile(path)
    assert not doc.audit().has_errors
    used = {e.dxf.layer for e in doc.modelspace()}
    assert used <= set(LAYERS)
    assert {"A-WALL", "A-DOOR", "A-GLAZ", "A-AREA-IDEN", "A-DIMS"} <= used
    labels = [e.text for e in doc.modelspace().query("MTEXT")]
    assert len(labels) == len(b.rooms)
    assert any("مجلس رجال" in t and "36.00" in t for t in labels)
