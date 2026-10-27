"""`dev/check_addon_versions.py`: an add-on of Kraft's own collection that
changed since the latest release has a new `version`, or no installed instance
ever sees the change."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
from support.addons import AGENT, make_collection, publish
from support.harness import git

_SCRIPT = Path(__file__).resolve().parents[1] / "dev" / "check_addon_versions.py"


@pytest.fixture(scope="module")
def cv():
    spec = importlib.util.spec_from_file_location("_dev_check_addon_versions", _SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize(
    ("change", "found"),
    [
        ({}, []),
        ({"library": {"tasks": {"base": AGENT, "more": AGENT}}}, ["release"]),
        ({"library": {"tasks": {"base": AGENT, "more": AGENT}}, "version": "1.1.0"}, []),
        ({"files": {"README.md": "notes\n"}}, []),
    ],
    ids=["unchanged", "changed-same-version", "changed-new-version", "file-kraft-never-reads"],
)
def test_a_changed_addon_needs_a_new_version(cv, tmp_path, change, found):
    repo = make_collection(tmp_path, {"release": {"library": {"tasks": {"base": AGENT}}}})
    git(repo, "tag", "v2.4.0")
    if change:
        publish(repo, "release", **change)

    assert cv.latest_release(repo) == "v2.4.0"
    assert [line.split(":")[0] for line in cv.problems(repo, "v2.4.0")] == found


def test_an_addon_the_release_lacks_is_new(cv, tmp_path):
    repo = make_collection(tmp_path, {"release": {"library": {"tasks": {"base": AGENT}}}})
    git(repo, "tag", "v2.4.0")
    publish(repo, "tools", library={"tasks": {"base": AGENT}})
    (repo / ".kraft/collection.json").write_text(
        (repo / ".kraft/collection.json")
        .read_text()
        .replace('"addons": [', '"addons": [{"name": "tools", "source": "./addons/tools"}, ')
    )

    assert cv.problems(repo, "v2.4.0") == []
