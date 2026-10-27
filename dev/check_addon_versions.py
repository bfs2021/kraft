"""Fail if an add-on of Kraft's own collection changed and kept its `version`.

An instance takes an add-on's update only when its `version` changes, and the
collection is installed from the default branch, so every change that reaches
`main` must carry its own raise: one to `config/library.yaml`, `config/chains/`
or an add-on under `addons/` that keeps the version never reaches an instance
that already took that version. This compares each add-on
`.kraft/collection.json` lists, as the working tree has it, with the base: the
merge base with `origin/main`, or the commit before when that is this one (a
push to `main`). When the files Kraft reads from an add-on differ, its
`version` must too. An add-on the base lacks is new and passes.

    uv run python dev/check_addon_versions.py

Needs `origin/main` (CI's lint job checks out with fetch-depth 0).
Exits 1 on any finding.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from kraft.addons import fetch, manifest

ROOT = Path(__file__).resolve().parents[1]


def _git(root: Path, *args: str) -> str | None:
    done = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else None


def base_commit(root: Path, upstream: str = "origin/main") -> str | None:
    """What this change is measured against; None when there is nothing before it."""
    base = _git(root, "merge-base", "HEAD", upstream)
    if base is not None and base == _git(root, "rev-parse", "HEAD"):
        return _git(root, "rev-parse", "--verify", "--quiet", "HEAD^1")
    return base


def _version(files) -> str:
    return json.loads(files[manifest.ADDON_JSON][1])["version"]


def problems(root: Path, base: str) -> list[str]:
    git_dir = Path(_git(root, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    listed = json.loads((root / manifest.COLLECTION_JSON).read_text())["addons"]
    found = []
    for entry in listed:
        source = entry["source"]
        now = fetch.extract_dir(root / source.removeprefix("./")).files
        try:
            then = fetch.extract_git(git_dir, base, source).files
        except fetch.FetchError:
            continue  # no such directory at the base: new
        if manifest.ADDON_JSON not in then:
            continue  # a directory, but not yet an add-on: new
        if fetch.digest(now) != fetch.digest(then) and _version(now) == _version(then):
            found.append(
                f"{entry['name']}: changed since {base[:12]} but still version {_version(now)}; "
                f"raise `version` in {source.removeprefix('./')}/{manifest.ADDON_JSON}"
            )
    return found


def main() -> int:
    base = base_commit(ROOT)
    if base is None:
        print("no merge base with origin/main: git fetch origin main", file=sys.stderr)
        return 1
    try:
        found = problems(ROOT, base)
    except fetch.AddonRefused as exc:
        found = [f"an add-on at {base[:12]} is one Kraft refuses: {exc}"]
    for line in found:
        print(line)
    if not found:
        print(f"ok: every add-on that changed since {base[:12]} has a new version")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
