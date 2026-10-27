"""The collection this repository publishes (`.kraft/collection.json`): the
shipped `config/` as the add-on `kraft-default`, and the add-ons that build on
it. A change to the shipped library that breaks one of them fails here."""

import shutil
from pathlib import Path

import pytest
from cli.test_addon import _run

from kraft.addons import load
from kraft.cli import addon as addon_cli
from kraft.cli.addon import validate
from kraft.progress import implementing_nodes
from kraft.templates.library import TemplateLibrary

REPO = Path(__file__).resolve().parents[2]
CHILDREN = ("kraft-superpowers", "kraft-temper")


def _shipped_config(tmp_path: Path) -> Path:
    config = tmp_path / "config"
    shutil.copytree(REPO / "config", config, ignore=shutil.ignore_patterns(".kraft"))
    return config


def test_the_published_collection_validates_against_the_shipped_config(tmp_path):
    report = validate(REPO, (_shipped_config(tmp_path), tmp_path / "addons"))

    assert report["problems"] == []
    assert {a["name"] for a in report["addons"]} == {"kraft-default", *CHILDREN}


@pytest.fixture
def library(tmp_path, monkeypatch, capsys):
    """An instance seeded from the shipped config with both children installed
    from this working tree."""
    config, run_dir = _shipped_config(tmp_path), tmp_path / "run"
    monkeypatch.setenv("KRAFT_CONFIG_DIR", str(config))
    monkeypatch.setenv("KRAFT_RUN_DIR", str(run_dir))
    monkeypatch.delenv("KRAFT_WORK_ITEM_ID", raising=False)

    async def no_server():
        return {}

    monkeypatch.setattr(addon_cli.client, "reload_addons", no_server)
    assert _run(capsys, "collection", "add", str(REPO))[0] == 0
    for child in CHILDREN:
        assert _run(capsys, "install", f"{child}@kraft-sdlc", "-y")[0] == 0
    return TemplateLibrary.from_yaml_dir(config, addons=load.installed(config, run_dir / "addons"))


@pytest.mark.parametrize("chain", ["default", "quick-task"])
@pytest.mark.parametrize("child", CHILDREN)
def test_a_child_chain_keeps_its_implementing_node(library, child, chain):
    """A method set as `skill:` would make the implementer a judging task, and
    Kraft would tell it implementing is another node's job."""
    assert implementing_nodes(library.resolve_chain(f"{child}:{chain}")) == ["implementation"]
