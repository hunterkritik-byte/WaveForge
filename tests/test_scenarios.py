import json

import pytest

from src.scenarios import Scenario, get_preset, load, save


def test_preset_is_valid_and_serializable():
    scenario = get_preset("baseline")
    restored = Scenario.from_dict(scenario.to_dict())
    assert restored == scenario


def test_unknown_field_is_rejected():
    with pytest.raises(ValueError, match="unknown scenario fields"):
        Scenario.from_dict({"name": "x", "unexpected": True})


def test_file_round_trip(tmp_path):
    path = tmp_path / "scenario.json"
    scenario = get_preset("dense-interference")
    save(scenario, path)
    assert load(path) == scenario
    assert json.loads(path.read_text())['name'] == "dense-interference"


def test_invalid_probability_is_rejected():
    with pytest.raises(ValueError):
        Scenario(name="bad", block_probability=1.1)
