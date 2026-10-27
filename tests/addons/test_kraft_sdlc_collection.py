"""The collection this repository publishes (`.kraft/collection.json`): the
shipped `config/` as the add-on `kraft-default`, and the add-ons that build on
it. A change to the shipped library that breaks one of them fails here."""

import shutil
from pathlib import Path

from kraft.cli.addon import validate

REPO = Path(__file__).resolve().parents[2]


def test_the_published_collection_validates_against_the_shipped_config(tmp_path):
    config = tmp_path / "config"
    shutil.copytree(REPO / "config", config, ignore=shutil.ignore_patterns(".kraft"))

    report = validate(REPO, (config, tmp_path / "addons"))

    assert report["problems"] == []
    assert {a["name"] for a in report["addons"]} == {
        "kraft-default",
        "kraft-superpowers",
        "kraft-temper",
    }
