"""Fail if an add-on of Kraft's own collection changed since the latest release
and kept its released `version`.

An instance takes an add-on's update only when its `version` changes, so a
change to `config/library.yaml`, `config/chains/` or an add-on under `addons/`
that keeps the released version never reaches anyone who installed it. This
compares each add-on `.kraft/collection.json` lists with the latest release
tag's: when the files Kraft reads from it differ, its `version` must too. An
add-on the tag lacks is new and passes. One raise covers every later change
until the next release.

    uv run python dev/check_addon_versions.py

Needs the repository's tags (CI's lint job checks out with fetch-depth 0).
Exits 1 on any finding.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from kraft.addons import fetch, manifest

ROOT = Path(__file__).resolve().parents[1]
_STABLE_TAG = re.compile(r"^v\d+\.\d+\.\d+$")


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def latest_release(root: Path) -> str | None:
    tags = [t for t in _git(root, "tag", "--list").split() if _STABLE_TAG.match(t)]
    return max(tags, key=lambda t: tuple(int(n) for n in t[1:].split(".")), default=None)


def _version(files) -> str:
    return json.loads(files[manifest.ADDON_JSON][1])["version"]


def problems(root: Path, tag: str) -> list[str]:
    git_dir = Path(_git(root, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    commit = _git(root, "rev-parse", "--verify", f"{tag}^{{commit}}")
    listed = json.loads((root / manifest.COLLECTION_JSON).read_text())["addons"]
    found = []
    for entry in listed:
        source = entry["source"]
        now = fetch.extract_dir(root / source.removeprefix("./")).files
        try:
            then = fetch.extract_git(git_dir, commit, source).files
        except (fetch.FetchError, fetch.AddonRefused):
            continue  # not in the release: new
        if manifest.ADDON_JSON not in then or fetch.digest(now) == fetch.digest(then):
            continue
        if _version(now) == _version(then):
            found.append(
                f"{entry['name']}: changed since {tag} but still version {_version(now)}; "
                f"raise `version` in {source.removeprefix('./')}/{manifest.ADDON_JSON}"
            )
    return found


def main() -> int:
    tag = latest_release(ROOT)
    if tag is None:
        print("no vX.Y.Z release tag in this clone: git fetch --tags", file=sys.stderr)
        return 1
    found = problems(ROOT, tag)
    for line in found:
        print(line)
    if not found:
        print(f"ok: every add-on that changed since {tag} has a new version")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
