# Plan: a file read from an add-on's store is checked against its digest when it is read

Spec: `2-skill-md-checked-at-launch.md` (read its **Decisions** first). Base: the integration branch `ccr-143df22f-uetbpy` (main f024b41 today). This item merges **third** of four (order 1, 3, 2, 4): items 1 and 3 will have landed before your PR merges. Read **Coordination** at the end before Task 1, and again before the final task.

### Task 0: Set up

```bash
git fetch origin
git switch ccr-143df22f-uetbpy-2-store-digest 2>/dev/null || git switch -c ccr-143df22f-uetbpy-2-store-digest origin/ccr-143df22f-uetbpy
uv tool install rust-just   # just is not preinstalled
just setup
```

Read `CLAUDE.md`, `docs/testing.md` and CONTRIBUTING's "Removed tests" and "Pull requests and release labels". If your session was given another branch name, use it; it must start from `origin/ccr-143df22f-uetbpy`.

Ground rules for every task:

- TDD. Write the row first and run it to see it fail for the reason the task fixes, then write the code and run it to see it pass.
- Run tests only through `just test` (path or `-k`), never `pytest`.
- A fix adds a `parametrize` row with an `id`. A new `def test_` is only for the new reader.
- Grep `tests/support/` before writing any helper. `just check-tests` refuses a copied helper body.
- Every module under `src/` keeps `from __future__ import annotations`. The code must run on 3.12.
- **Import `fetch` lazily** (inside the function) from `skill.py`, `templates/environment.py`, `templates/library.py` and `addons/load.py`. `fetch` imports `kraft.config` and `kraft.worker.sandbox` at module level, `kraft.config` imports `templates.environment`, and `load.py` is a leaf on purpose (its docstring says so). `_why_left_out` and `_addon_profiles` already import this way.
- After each task: `just lint`, `just check-tests`, then `just test` with the files that task touched, then commit.
- Mutation check after every pass: apply the mutation the task names, run that one case (`just test <file> -k '<test> and <id>'`), confirm it fails for that reason, revert. Record each for the PR body.
- Line budget (`dev/check_tests.py`, 800 per test file). `tests/addons/test_update.py` is at **794**: Task 7 gets exactly +3 lines there, and item 4 adds none. `tests/addons/test_pins.py` (344) and `tests/addons/test_repo_library.py` (679) are shared with items 1, 3 and 4 (DECISIONS D11): keep your growth near +15 each. `tests/api/test_deps.py` is at 800 and `tests/executor/test_dispatch.py` at 896/898 (allowlisted): add nothing to either.

---

### Task 1: The store reader in `fetch.py`

**Files:** `src/kraft/addons/fetch.py`, `tests/addons/test_fetch.py`, `tests/support/addons.py`

**Code** (next to `digest_manifest`, `fetch.py:340`):

- `class StoreMismatch(AddonRefused)`. The message names the store-relative path and ends with the constant `CHANGED = "the store was changed after it was installed"`.
- `def _lay_out(root: Path, files) -> None`: writes each file and `.kraft-digest` (`digest_manifest(files)`). This is the loop `write_store` has today (`fetch.py:373-378`), without the `chmod`s.
- `def write_scratch(parent: Path, extracted: Extracted) -> Path`: `parent / <digest hex>`, `mkdir(parents=True, exist_ok=True)`, `_lay_out`, writable. It returns the root.
- `@dataclass(frozen=True) class StoreFiles`: `root: Path` and `listed: Mapping[str, tuple[str, str]]` (path to (mode, sha256 hex)).
  - `read(rel, *, optional=False) -> bytes | None`.
    - **Listed:** if `not os.path.lexists(root / rel)`, raise `StoreMismatch(f"{rel} is missing; {CHANGED}")`. Otherwise read it with the existing `read_regular(root / rel, _cap(rel))` (`fetch.py:262`: `O_NOFOLLOW | O_NONBLOCK`, regular files only, capped) -- do not write a second bounded reader. Map its `FetchError` to `StoreMismatch(f"{rel} does not match its digest; {CHANGED}")`. Compare `hashlib.sha256(data).hexdigest()` with the manifest line and raise the same on a mismatch. Return `data`, the bytes hashed.
    - **Not listed:** if `optional` and `not os.path.lexists(root / rel)`, return `None`. Otherwise raise `StoreMismatch(f"{rel} is not in its digest; {CHANGED}")`.
  - `paths(prefix: str) -> list[str]`: the listed paths starting with `prefix`, sorted.
- `def open_store(root: Path) -> StoreFiles`: reads `.kraft-digest` with `read_regular(root / DIGEST_FILE, MAX_FILES * 512)` (a missing or refused manifest is a `StoreMismatch` too). Its SHA-256 must equal `root.name`, otherwise `StoreMismatch(f"{DIGEST_FILE} does not hash to the store's name; {CHANGED}")`. It then parses `rel\0mode\0hex\n` lines. Raise `StoreMismatch` on a malformed line, which only a manifest that hashes to the name yet was not written by `digest_manifest` could carry.
- `def verify_store(root: Path) -> Extracted`: `open_store(root)` for the name check, then `extracted = extract_dir(root)`. `digest_manifest(extracted.files)` must equal the bytes `open_store` read, otherwise `StoreMismatch(f"its files do not match its digest; {CHANGED}")`. It returns `extracted`. Keep the raw manifest bytes on `StoreFiles` (e.g. `raw: bytes`) so this compares exact bytes.

**Support** (`tests/support/addons.py`, grep first: `drop_store` is there, and no edit helper exists):

- `edit_store(store: Path, rel: str, text: str) -> None`: makes the file's parent directories and the file writable (`0o755` and `0o644`) and writes `text`. This is what `test_load.py:112-114` does inline.
- `forge_digest(store: Path) -> None`: rewrites `.kraft-digest` as `fetch.digest_manifest(fetch.extract_dir(store).files)`, so the manifest matches an edit but no longer hashes to the directory's name.

**Test first:** `tests/addons/test_fetch.py::test_a_store_file_is_read_only_if_it_matches_its_digest` (new behaviour, new function). It uses `fetch.write_store(addons_dir, _extract(collection, addons_dir))` with a collection whose `release` has a skill `x` and a `chains/ship.yaml`. Parametrize `(damage, rel, optional, expect)` with these ids:

| id | damage | reads | expect |
|---|---|---|---|
| `unchanged-is-read` | none | `skills/x/SKILL.md` | the stored bytes |
| `edited-file-is-refused` | `edit_store` the skill | same | `StoreMismatch`, match `does not match its digest` |
| `edited-digest-manifest-is-refused` | edit + `forge_digest` | same | match `does not hash to the store's name` |
| `unlisted-file-is-refused` | plant `chains/extra.yaml` | `chains/extra.yaml` | match `is not in its digest` |
| `listed-file-gone-is-refused` | delete `chains/ship.yaml` | `chains/ship.yaml` | match `is missing` |
| `optional-absent-is-none` | none | `profiles.yaml`, `optional=True` | `None` |
| `symlink-is-refused` | replace the skill with a symlink to a copy of the same bytes | skill | `StoreMismatch` |

Every refusal row also asserts `fetch.CHANGED in str(exc)`. Keep the file under 800 lines (it is at 263).

**Mutation check:** comment out the hash comparison in `read`, and `edited-file-is-refused` fails. Drop the `root.name` check in `open_store`, and `edited-digest-manifest-is-refused` fails. Read with `(root / rel).read_bytes()` instead of `read_regular`, and `symlink-is-refused` fails (the link's target has the same bytes, so only the no-follow open refuses it). Apply each, confirm the failure, revert.

**Commands:** `just test tests/addons/test_fetch.py -k read_only_if_it_matches`, `just lint`, `just check-tests`.

---

### Task 2: `write_store` re-checks an existing store, and `_why_left_out` uses `verify_store`

**Files:** `src/kraft/addons/fetch.py` (`write_store`, `:359`), `src/kraft/addons/load.py` (`_why_left_out`, `:325-330`; `gc`, `:608-634`), `tests/addons/test_fetch.py`

**Code:**

- `write_store`:
  1. `final.is_dir()`: try `verify_store(final)` and return `final` if it passes. On `AddonRefused` (which includes `StoreMismatch`) or `OSError`, mark it `stale` and go on.
  2. Build `tmp` in `staging/` with `_lay_out` and the existing `chmod`s.
  3. If `stale`: `final.chmod(0o755)` (macOS will not rename a read-only directory to another parent), then `os.rename(final, staging / f"{tmp.name}.stale")`. Ignore `FileNotFoundError`, because another writer moved it first.
  4. Rename `tmp` into place as today, including the existing branch where another writer won the rename.
  5. Remove the stale copy with the read-only-tree removal `load.gc` does (`load.py:629-632`). Move that loop into `fetch` as `remove_tree(path)` and have `gc` call it, so the body exists once.
- `_why_left_out`: keep the `recorded`/name check for `verify=False` (or use `open_store(root)`). For `verify=True`, replace the inline `digest_manifest(extract_dir(root).files) != recorded` with `fetch.verify_store(root)`. Catch `fetch.StoreMismatch` **before** the broader `AddonRefused` and return the same `mismatch` text, `its files do not match the locked digest`.

**Test first:** parametrize `tests/addons/test_fetch.py::test_a_store_is_addressed_by_its_content` with `damage` and these ids:

- `unchanged-store-is-reused`: today's assertions, plus the inode of `store` is unchanged after the second `write_store`.
- `edited-store-is-rewritten`: `edit_store(store, "library.yaml", "tasks: {}\n")`, then the second `write_store` returns the same path, `(store / "library.yaml").read_bytes()` is the original again, `fetch.verify_store(store)` passes, the file is read-only again, and `staging/` is empty.
- `edited-digest-manifest-is-rewritten`: the same edit plus `forge_digest(store)`, with the same assertions.

The function's id gains brackets. Intent does not pin it (grep: no hit), so `## Removed tests` is not needed. Run `uv run python dev/check_removals.py origin/ccr-143df22f-uetbpy <body file>` in Task 9 to confirm.

**Guarding tests to run:** `tests/addons/test_load.py::test_a_digest_mismatch_leaves_the_addon_out` (its `verify=True` assertion now goes through `verify_store`), the `test_load.py` `gc` tests, and `tests/api/test_deps.py::test_health_names_an_addon_that_did_not_load`.

**Mutation check:** put back `if final.is_dir(): return final`, and both `rewritten` rows fail. Skip the rename-aside step, and `edited-store-is-rewritten` fails on `os.rename` (target exists) or on the stale content.

**Commands:** `just test tests/addons/test_fetch.py tests/addons/test_load.py`, `just test tests/api/test_deps.py -k did_not_load`, `just lint`.

---

### Task 3: Candidates and the test fixture are laid out as stores

This is a refactor with no behaviour change, and it has to come first: Tasks 4-6 make the profile and library readers demand a manifest, and today's candidate scratch directories and `support.addons.installed` have none.

**Files:**

- `src/kraft/addons/update.py:611-615`: `root = fetch.write_scratch(Path(scratch), extracted)`.
- `src/kraft/addons/repo_library.py:399-403`: the same.
- `src/kraft/addons/review.py:169-174`: `root = fetch.write_scratch(Path(tmp), extracted)`.
- `src/kraft/cli/addon.py:48-53` (`_lint`) and `:98-103`: `store = fetch.write_scratch(Path(tmp), extracted)`. Map messages with `m.replace(str(store), str(root))`, not `m.replace(tmp, ...)`, because the scratch root is now `tmp/<digest>`.
- `tests/support/addons.py::installed`: build the file map from `library`, `chains`, `skills`, `profiles` and a new `files: dict[str, str] | None` (raw text by path), then `root = fetch.write_scratch(tmp_path / "store", fetch.Extracted(files))`. `extracted()` in the same module already builds that map (plus an `addon.json`): factor its loop into one private `_layout(library, chains, skills, profiles, files) -> dict` that both call, rather than writing the loop a second time. The root is now `store/<digest>/` and stays writable. Update the docstring. Two `installed()` calls with identical content now share one root: no current caller does that, but a test that edits `addon.root` must not create a second add-on with the same content.
- `tests/templates/test_library_addons.py::test_an_addon_error_names_the_store_file`: pass `files={file: text}` to `installed` instead of writing into `addon.root` afterwards, so the four bad files are inside the digest. Task 6 needs this. Its ids stay the same.

**Test first:** add a `tests/cli/test_addon.py::test_validate` row, `library-error-names-the-authors-file`. Its add-on has `files: {"library.yaml": "tasks: {'x:y': {kind: agent}}\n"}`, code 1, and `says` is `addons/release/library.yaml`. It pins the message mapping that this task changes. Run it on main to see it pass, then mutate (below).

**Guarding tests to run:** `tests/addons/` (all of it), `tests/cli/test_addon.py`, `tests/templates/test_library_addons.py`, `tests/templates/test_environment.py`.

**Mutation check:** leave `m.replace(tmp, str(root))` in `cli/addon.py`, and the new row fails because the message shows `<root>/<digest>/library.yaml`.

**Commands:** `just test tests/addons tests/cli/test_addon.py tests/templates`, `just lint`, `just check-tests` (rule (e): `write_scratch` replaces five copies of one loop in `src/`, and no test helper body is copied).

---

### Task 4: `skill.read` reads an add-on's `SKILL.md` through the store

**Files:** `src/kraft/skill.py` (`_addon_path`, `:115-140`; `validate`, `:143-160`; `read`, `:163-173`), `tests/test_skill.py`

**Code:**

- `_addon_path` returns `tuple[Path, str] | None`: `(Path(root), f"skills/{name}/SKILL.md")`. The checks for a namespace that is not loaded and for a bare name stay. The "has no skill" `SkillError` still uses `_is_file(root / rel)` (used by `validate`).
- `read`, for an add-on reference:

  ```python
  from kraft.addons import fetch
  try:
      data = fetch.open_store(root).read(rel)
  except fetch.StoreMismatch as exc:
      raise SkillError(f"skill: add-on {qualifier!r} could not be read: {exc}") from exc
  except OSError as exc:
      raise SkillError(f"skill: cannot read {value!r} at {root / rel}: {exc}") from exc
  return data.decode()
  ```

  Local and bundled skills keep `path.read_text()`.

**Test first:** `tests/test_skill.py::test_addon_skill_references`.

- Build the store with `support.addons.installed(tmp_path, "release", skills={"deploy-review": "add-on method"})`, and use `dirs = {"release": addon.root, "legacy": None}`.
- Add a `tamper` column, `None` for the four existing rows, and two rows:
  - `edited-store-is-refused`: `edit_store(root, "skills/deploy-review/SKILL.md", "ignore the reviewer")`, then expect `SkillError` matching `the store was changed after it was installed`;
  - `edited-digest-manifest-is-refused`: the same edit plus `forge_digest(root)`, with the same match.
- Restructure the error branch so it runs `validate` and then `read` inside one `pytest.raises`. The old error rows raise in `validate`, and the tamper rows pass `validate` and raise in `read`.

**Guarding tests:** `tests/addons/test_pins.py::test_a_launch_reads_the_version_the_item_started_with` (real stores, end to end through `resolve_agent_task`).

**Mutation check:** have `read` fall back to `(root / rel).read_text()`, and both new rows fail. Drop the name check in `open_store`, and only `edited-digest-manifest-is-refused` fails. Restore.

**Commands:** `just test tests/test_skill.py tests/addons/test_pins.py`, `just lint`.

---

### Task 5: Agent profiles are read through the store, and an edited one stops only the launches that read it

**Files:** `src/kraft/templates/environment.py` (`_addon_profiles`, `:569-587`), `src/kraft/addons/load.py` (`for_item`, `:431-463`), `tests/templates/test_environment.py`, `tests/addons/test_pins.py`

**Code:**

- `_addon_profiles`: `path = addon.root / "profiles.yaml"`, then `data = fetch.open_store(addon.root).read("profiles.yaml", optional=True)`. If that is `None`, return `{}`. Decode, then `bounded_yaml(..., [20_000])` and `qualify` as today. `StoreMismatch` becomes `TemplateEnvironmentError(f"{path}: {exc}")`, which keeps `str(root)` in the message for `_why_left_out`'s attribution at `load.py:357`. `OSError`, `ValueError` and `YAMLError` keep the `cannot read/parse` message.
- `for_item`: after building `(*live, *pinned)`, map each add-on that loads (`left_out is None`) and whose `root.is_dir()` through a new `_launch_problem(addon) -> str | None`, which runs `fetch.open_store(addon.root).read("profiles.yaml", optional=True)`. It returns `str(exc)` on `StoreMismatch` and `f"its store cannot be read: {exc}"` on `OSError`. An add-on with a problem becomes `replace(addon, left_out=why)`. Write a docstring line: this checks the manifest and `profiles.yaml`, which every launch reads. Skills are checked where they are read.

**Test first:**

1. `tests/templates/test_environment.py::test_addon_profiles`: add a `tamper` column (`None` for `qualified` and `fallback-entry`) and two rows.
   - `edited-store-is-refused`: `edit_store(addon.root, "profiles.yaml", yaml.safe_dump({"profiles": {"deep": {"model": {"codex": "evil"}}}}))`.
   - `edited-digest-manifest-is-refused`: the same edit plus `forge_digest`.
   - Both expect `te.TemplateEnvironmentError` matching `the store was changed after it was installed`, with `str(addon.root)` in the message.
2. `tests/addons/test_pins.py::test_a_missing_pin_the_task_does_not_read_does_not_stop_it`: add a `damage` column. The four existing rows are `"gone"`, today's setup with `drop_store` and the zero digest, and their ids are unchanged. Add two rows with `damage = "edited"`, which runs `edit_store(<the pinned store>, "profiles.yaml", ...)` and launches with the real `pins`:
   - `edited-profiles-stop-its-profile`: `{"profile": "release:deep"}`, stops, matching `could not be read: profiles.yaml does not match its digest`;
   - `edited-profiles-spare-an-unrelated-task`: `{"prompt": "unrelated"}`, launches.

**Mutation check:**

- Delete the `for_item` check. The table then raises for every launch: `edited-profiles-spare-an-unrelated-task` fails with `HarnessUnavailable`, and `edited-profiles-stop-its-profile` fails on its `match`.
- Make `_addon_profiles` use `path.read_text()` again, and both `test_environment` rows fail.
- Restore both.

**Guarding tests:** `tests/addons/test_pins.py` (all), `tests/executor/test_dispatch_pins.py`, `tests/api/test_harnesses.py`, `tests/addons/test_load.py`, `tests/test_escalate.py -k pinned`, `tests/test_review_reply.py -k pinned`.

**Commands:** `just test tests/templates/test_environment.py tests/addons/test_pins.py tests/executor/test_dispatch_pins.py tests/addons/test_load.py`, `just lint`.

---

### Task 6: An add-on's `library.yaml` and chains are read through the store

These are re-read after load when a running item's chain is revised (`templates/revision.py:384` `_pinned` → `with_addons(load.for_item(pins))` → `_add_addon`).

**Files:** `src/kraft/templates/library.py` (`_add_addon`, `:380-402`, and a helper beside `_read`, `:210`), `tests/templates/test_library_addons.py`

**Code:**

- `def _read_stored(store, rel: str, path: Path) -> Mapping[str, object]`. It takes the bytes from `store.read(rel)`, decodes them, applies `bounded_yaml(text, [ADDON_YAML_NODES])` and runs the same `None`/mapping checks as `_read`. On `fetch.StoreMismatch`, raise `TemplateLibraryError(f"{path}: {exc}")`, and on parse failures raise the existing `f"{path}: cannot read/parse: {exc}"`. Factor the shared tail (`data is None` → `{}`, not a mapping → error) out of `_read` instead of copying it.
- `_add_addon`: `store = fetch.open_store(addon.root)`, wrapped so a `StoreMismatch` from the manifest becomes `TemplateLibraryError(f"{addon.root / DIGEST_FILE}: {exc}")`. Then:
  - `library.yaml` is read when `store.read(LIBRARY_FILE, optional=True)` is not `None`, which also refuses a planted, unlisted `library.yaml`;
  - the chains are `for rel in store.paths(f"{CHAINS_DIR}/")`, with `addon.root / rel` as the `chain_path`. They come from the manifest, not `glob`.
  - Keep the `ComponentSource` paths as they are (`addon.root / ...`), since error messages and `addon_of` rely on them.

**Test first:** `tests/templates/test_library_addons.py::test_an_addon_error_names_the_store_file`, whose rows already pass their text through `installed(files=...)` after Task 3. Add an `after` column (`None` for the four rows) and a row `edited-after-install`:

- `file="chains/ship.yaml"`, with the fixture created with `files={"chains/ship.yaml": "nodes: []\n"}`;
- `after="nodes: []\n# edited\n"`, written with `edit_store` once the store exists;
- `why="the store was changed after it was installed"`.

The existing `assert str(addon.root / file) in str(exc.value)` holds unchanged.

**Guarding tests:** `tests/addons/test_load.py::test_a_broken_addon_library_affects_only_that_addon` edits `library.yaml` in a real store. It now reaches the digest refusal instead of the parse error. Its assertions (the path is in `left_out`, and the other add-on loads) must still hold, and the parse-error case itself stays pinned by the four rows above. Also run `tests/templates/test_revision.py` and `tests/addons/test_pins.py -k revis`.

**Mutation check:** have `_add_addon` read `library_path`/`glob` directly again, and `edited-after-install` fails. Restore.

**Commands:** `just test tests/templates tests/addons/test_load.py tests/addons/test_pins.py`, `just lint`.

---

### Task 7: A review never compares against an edited installed copy

**Files:** `src/kraft/addons/update.py:588`, `src/kraft/addons/repo_library.py:381`, `tests/addons/test_update.py`, `tests/addons/test_repo_library.py`

**Code:** in both places, `old = fetch.extract_dir(store)` becomes `old = fetch.verify_store(store)`. The surrounding `except Exception` already turns a failure into "could not be read to compare with".

**Test first:**

1. `tests/addons/test_update.py::test_an_installed_copy_that_does_not_read_is_said_in_the_review`: add the row `edited-but-valid`, whose `stored` is a valid `addon.json` for `release` at `1.0.0`. It reads cleanly today, so the row fails before the change. **The file is at 794 of the 800-line budget, and the sum across the batch must fit (item 4 adds nothing here).** Do it in exactly 3 lines: a module constant `VALID_ADDON_JSON = json.dumps(addon_json("release"))` directly above the decorator (`json` and `addon_json` are already imported; the constant and its two blank lines are the +3), then extend the existing one-line lists in place: `[("{", "1.1.0"), ("[]", "1.1.0"), (None, "1.1.0"), ("{", "0.9.0"), (VALID_ADDON_JSON, "1.1.0")]` and `ids=[..., "a-step-back", "edited-but-valid"]`. Both lines stay under ruff's 100 columns, so `ruff format` keeps them on one line. Confirm `wc -l tests/addons/test_update.py` reads 797.
2. `tests/addons/test_repo_library.py::test_a_change_is_reviewed_against_the_accepted_version`: parametrize `edited` and give it these ids:
   - `unchanged`: today's assertions;
   - `store-edited`: after `accept`, `edit_store(<the accepted store>, "library.yaml", ...)`, then assert `found.review.reach[0] == "the accepted version's files could not be read to compare with"`.

**Mutation check:** put back `extract_dir` at each site, and its own row fails. Revert.

**Commands:** `just test tests/addons/test_update.py tests/addons/test_repo_library.py`, `just lint`, `just check-tests` (the line budget).

---

### Task 8: Docs and intent

**Docs** (CONTRIBUTING's table maps `src/kraft/addons/` to these pages):

- `docsite/content/5.reference/03.configuration/12.addons.md` **The digest** (`:402-406`): add that every file Kraft reads from a store after it is written is checked against `.kraft-digest`, and that the manifest must hash to the store's name. That covers a skill and the agent profiles at each launch, and the library and chains when a running item's chain is revised. An edited file stops only a launch that reads it. Writing the same digest again (a restore, or an install of the same content) replaces an edited store. Leave the load-checks list (`:293`) as is.
- `docsite/content/5.reference/03.configuration/13.repo-libraries.md` **Work items, restore and the store** (`:187-191`): one sentence saying the same check applies.
- `docsite/content/6.project/1.security.md` (`:503-504`): change the bullet to "A stored add-on whose files no longer match is not loaded, and a file edited after that is refused when it is read."
- `docsite/content/4.troubleshooting/2.stop-reasons-in-detail.md` `## add-on ... could not be read` (`:50-60`): add a reason bullet, `<file> does not match its digest; the store was changed after it was installed`. The remedy:
  1. Find out what wrote under `run/addons/store/`. `kraft admin doctor` names the add-on.
  2. Delete that `store/<digest>/` directory (`chmod -R u+w` it first, since it is read-only), and the next launch restores the pinned version from its commit.
  3. Run `kraft item retry ID`.
  
  Also note the skill form of the stop, `skill: add-on '<namespace>' could not be read: ...`.

**Intent** (`docs/intent/kraft-addons.md`): add `REQ an-edited-store-file-is-never-read` and `REQ an-edited-store-is-replaced-not-reused` after `an-addon-whose-digest-does-not-match-is-not-loaded` (`:141`), exactly as in the spec's Requirements section. Extend `a-launch-stops-only-for-an-addon-it-reads` (`:357-360`) `enforced-by:` with the two `test_pins` rows from Task 5. Use the format of the surrounding entries: a blank line after the heading, the EARS sentence, then `enforced-by:` and `origin:` lines.

**Commands:** `just intent` (exit 0), `just check-tests`, `just lint`, and `just test` (testmon, everything this branch touched). Then `just test --no-testmon tests/addons tests/templates tests/test_skill.py tests/cli/test_addon.py` for the full add-on tier. Optionally run `just docs` to look at the changed pages.

Commit.

---

### Task 9: Final verification and the PR

1. **Merge the integration branch in:** `git fetch origin && git merge origin/ccr-143df22f-uetbpy`. Items 1 and 3 will usually have landed. Resolve as **Coordination** says, then run the sibling tests it names.
2. **Checks**, on the merged head:

   ```bash
   just lint
   just intent
   just check-tests
   just test tests/addons tests/templates tests/test_skill.py tests/cli/test_addon.py tests/executor/test_dispatch_pins.py tests/api/test_deps.py tests/api/test_harnesses.py tests/api/test_addon_content.py tests/test_escalate.py tests/test_review_reply.py --no-testmon
   just test            # testmon: everything else this branch touched
   uv run python dev/check_docs_walls.py docsite/content/5.reference/03.configuration/12.addons.md docsite/content/5.reference/03.configuration/13.repo-libraries.md docsite/content/6.project/1.security.md docsite/content/4.troubleshooting/2.stop-reasons-in-detail.md
   wc -l tests/addons/test_update.py tests/addons/test_pins.py tests/addons/test_repo_library.py tests/addons/test_fetch.py   # each <= 800; test_update.py 797
   ```

3. Write the PR body to `${TMPDIR:-/tmp}/pr-body-2.md` (outside the worktree), run `uv run python dev/check_removals.py origin/ccr-143df22f-uetbpy "${TMPDIR:-/tmp}/pr-body-2.md"` (exit 0), then `gh pr create --base ccr-143df22f-uetbpy --label release::none --title "A file read from an add-on's store is checked against its digest" --body-file "${TMPDIR:-/tmp}/pr-body-2.md"`.

**PR body:**

- **Base branch:** `ccr-143df22f-uetbpy` (DECISIONS D1), not `main`.
- **Release label: `release::none`.** Add-ons landed in 041216a (#700), and `git tag --contains 041216a` lists no tag: the latest tag is `v2.0.0`, which does not contain it. This hardens a feature that has not shipped yet, so it goes out with that feature's release and adds no weight to the bump. If a release containing #700 is tagged before this merges, use `release::patch` instead.
- **`## Changelog`** (DECISIONS D6/D9: written even under `release::none`, for the final PR to collect): "Kraft checks every file it reads from an add-on's or repo library's store (skills, agent profiles, library and chains) against the store's digest when it reads it, and stops only the launches that read an edited file. Writing the same version again replaces an edited store."
- **`## Removed tests`:** none. No test function or `## REQ` is deleted. `test_a_store_is_addressed_by_its_content` and `test_a_change_is_reviewed_against_the_accepted_version` gain parameter ids, and intent pins neither (checked by grep).
- **`## Test evidence`:** paste the last lines of every command in step 2 and of `check_removals`, as run on the merged head.
- **Mutation table:** one line per task's mutation check, in the form `docs/testing.md` asks for: "mutation: `<change>` kills `<test[id]>`; applied, confirmed failing, reverted".
- **Docs touched:** `12.addons.md`, `13.repo-libraries.md`, `1.security.md`, `2.stop-reasons-in-detail.md`.
- **Coordination:** one line saying which sibling PRs were already in the integration branch when this was verified.

---

## Coordination

Order: 1, 3, **2**, 4. Items 1 and 3 land before you; item 4 lands after you and builds on your code.

- **Item 1 (minted repo ids)** changes `addons/repo_library.py` `check` at `:357-359` (`_id_problem(repo_id, held_namespaces(...))`) and adds a `prepare` column and an `a-pending-alias` row to `tests/addons/test_repo_library.py::test_an_id_that_cannot_be_a_namespace_is_refused`. You change `:381` and `:399-403` of the same function and add a test row lower in the same test file. Textual merge only. After merging, run `just test tests/addons/test_repo_library.py tests/api/test_repos_library.py tests/api/test_repos_workspaces.py`.
- **Item 3 (revision `extends` qualified)** lands before you. It adds `test_the_gate_names_what_an_added_node_comes_from` to `tests/templates/test_revision.py`, built with `support.addons.installed(tmp_path, "release", library=...)`, and re-parametrizes `tests/addons/test_pins.py::test_a_revision_resolves_against_pinned_addons` plus a new `test_a_revision_cannot_add_from_an_addon_that_is_not_loaded` there. All of them reach `_add_addon` (Task 6) and, through `revision._pinned` → `load.for_item`, your `_launch_problem` (Task 5). Your `installed()` change keeps them working only if they pass all content through `installed(...)` arguments (they do). After merging, run `just test tests/templates/test_revision.py tests/addons/test_pins.py tests/api/test_addon_content.py --no-testmon`. Item 3 also edits `12.addons.md` and `1.security.md` (other paragraphs) and adds a REQ after `running-item-keeps-its-addon-versions` in `kraft-addons.md` (you add yours after `an-addon-whose-digest-does-not-match-is-not-loaded`); textual only.
- **Item 4 (repo library scoped to its repo)** lands after you and rewrites `load.for_item` to `for_item(pins, config_dir=None, addons_root=None, *, repo_id)`, adding `scoped(...)` and reserved entries for connected repo ids. To make that composition mechanical:
  - keep your check in its own function, `_launch_problem(addon) -> str | None`, applied by one `replace(addon, left_out=why)` pass at the end of `for_item` over entries with `left_out is None`. Item 4 runs `scoped` first, so an out-of-scope store is never hashed (DECISIONS D13);
  - keep `edit_store` and `forge_digest` in `tests/support/addons.py` with these names: item 4 uses `edit_store` for its cross-item row (an edited own-repo library stops with your digest message, not the scope message). You owe no row for that (DECISIONS D7);
  - item 4 also edits `tests/addons/test_pins.py` (three new tests) and `tests/addons/test_repo_library.py` (a new test), and `13.repo-libraries.md` and `1.security.md` (other paragraphs).
