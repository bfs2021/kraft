# Plan: a minted repository id never takes an add-on's namespace

Spec: `1-repo-id-never-takes-an-addon-namespace.md` (read its **Decisions** first). Base: the integration branch `ccr-143df22f-uetbpy` (main f024b41 today). This item merges **first** of four (order 1, 3, 2, 4); see **Coordination** at the end.

### Task 0: Set up

```bash
git fetch origin
git switch ccr-143df22f-uetbpy-1-repo-id-namespace 2>/dev/null || git switch -c ccr-143df22f-uetbpy-1-repo-id-namespace origin/ccr-143df22f-uetbpy
uv tool install rust-just   # just is not preinstalled
just setup
```

Read `CLAUDE.md`, `docs/testing.md` and CONTRIBUTING's "Removed tests" and "Pull requests and release labels" before the first test. If your session was given another branch name, use it; it must start from `origin/ccr-143df22f-uetbpy`.

Ground rules for every task:

- Tests go through `just test <path> -k '<expr>'`, never raw pytest.
- TDD order: write the row or test, run it and see it **fail for the reason named**, implement, run it and see it pass.
- Mutation check after the pass: apply the mutation, re-run that one case, confirm it fails, then revert. Note each mutation for the PR body.
- `tests/support/` and `docs/intent/` are testmon blind spots. `just test <paths>` reruns the named paths with `--no-testmon` when they differ from `origin/main`. That is expected.
- Before each commit: `just lint` and `just check-tests`. Commit at the end of each task.
- Line budget (`dev/check_tests.py`, 800 per test file): `tests/addons/test_repo_library.py` is at 679 and items 2 and 4 grow it after you, so keep your row to about 8 lines. `tests/api/test_repos.py` is at 792: add nothing there. `tests/api/test_repos_library.py` (130) and `tests/api/test_repos_workspaces.py` (155) have room.

---

### Task 1: One namespace rule in `repo_library`, pending aliases included

**Files**

- `src/kraft/addons/repo_library.py`
- `tests/addons/test_repo_library.py`

**Test first.** Add a row to `test_an_id_that_cannot_be_a_namespace_is_refused` (`tests/addons/test_repo_library.py:225-243`). The test installs `release@acme` itself, so give the parametrize a third column, `prepare`. It is `None` for the three existing rows, and for the new row:

```python
pytest.param(
    "rel", "add-on release@acme", _alias_pending, id="a-pending-alias",
),
```

Here `_alias_pending(home)` is `edit_addons_yaml(home[0], lambda c: c["addons"].update({"release@acme": {"as": "rel"}}))`. That is an `as:` written to `addons.yaml` with no update run, so `addons.lock` still says `release`. Import `edit_addons_yaml` from `support.addons`. In the body, call `prepare(home)` after `install(...)` when it is set. The other three rows keep their ids and assertions unchanged, so no pin moves.

Run it and see it fail: `refused` is not the outcome, because `_id_problem` reads only the lock's namespaces.

```bash
just test tests/addons/test_repo_library.py -k 'test_an_id_that_cannot_be_a_namespace_is_refused'
```

**Implement** (below `_short`, beside `_id_problem`):

- `held_namespaces(config_dir: Path, addons_root: Path) -> dict[str, str]`, mapping namespace to add-on id.
  - Start with `{p.namespace: p.id for p in load.installed(config_dir, addons_root) if p.repo_id is None}`.
  - Then, in a `try` around `AddonsConfig.load(config_dir / AddonsConfig.FILE)`, add each `config.namespace(addon_id)` with `held.setdefault(namespace, addon_id)`.
  - `except ConfigError: pass`, with the comment "`config_problem` says why", as `load._installed` does.
  - Import `AddonsConfig` from `kraft.addons.config`, next to `RESERVED_NAMESPACE`.
- `namespace_problem(repo_id: str, held: Mapping[str, str]) -> str | None` holds the reserved check and the add-on check, moved verbatim from `_id_problem` with the same `fix` text. The add-on message is built from `held[repo_id]`.
- `_id_problem(repo_id, held)` becomes `namespace_problem(repo_id, held)` or the existing `> 64` rule.
- `check` (`:358-360`): keep `loaded = list(load.installed(...))`, since it is still used for `others` and `update.state_of`. Change the call to `_id_problem(repo_id, held_namespaces(config_dir, addons_root))`.

Run it and see all four rows pass: `reserved`, `an-addons-namespace`, `too-long` and `a-pending-alias`.

**Mutations**

- In `held_namespaces`, drop the `AddonsConfig` loop. `[a-pending-alias]` should fail.
- In `namespace_problem`, drop the `RESERVED_NAMESPACE` branch. `[reserved]` should fail.

```bash
just test tests/addons/test_repo_library.py
just lint
```

---

### Task 2: The repo-library door mints past add-on namespaces and `kraft`

**Files**

- `src/kraft/api/routes/repos.py`
- `tests/api/test_repos_library.py`

**Test first.** Parametrize `test_a_repo_library_is_reviewed_then_accepted` (`tests/api/test_repos_library.py:22-42`):

```python
@pytest.mark.parametrize(
    "name, addon, minted",
    [
        pytest.param("app", False, "app", id="own-name"),
        pytest.param("release", True, "release-2", id="addon-namespace"),
        pytest.param("kraft", False, "kraft-2", id="reserved"),
    ],
)
```

- `_with_library(tmp_path, client, name="app")` passes `name` to `repo_with_library(tmp_path, name)`. Its other callers keep the default.
- When `addon` is set, call `load_release(client, tmp_path)` (from `support.addons`) before connecting.
- Replace each literal `"app"` in the assertions with `minted`. That covers `seen["id"]`, the lock key, `GET /repos`' `id`, and the health key `f"repo library {minted}"`.
- For `[addon-namespace]`, also assert `"add-on release@acme" not in health.get("invalid_templates", {})`.

This test is not pinned in `docs/intent/`, so nothing needs repointing (checked: `grep -rn test_a_repo_library_is_reviewed_then_accepted docs/intent` finds nothing).

See `[addon-namespace]` and `[reserved]` fail: `outcome` is `refused`, not `waiting`, because the minted id is `release` or `kraft`. `[own-name]` passes.

```bash
just test tests/api/test_repos_library.py -k 'test_a_repo_library_is_reviewed_then_accepted'
```

**Implement**

- `_repository_id(entry, repos, held: Mapping[str, str])`. The candidate generator skips a candidate `c` when `c in taken or repo_library.namespace_problem(c, held) is not None`. A carried `entry["id"]` is returned untouched, as now. Update the docstring: "and never `kraft` or an add-on's namespace".
- `_check_library`: `held = repo_library.held_namespaces(st.templates_dir, st.run_dirs.addons)` before the mint, and `_repository_id(entry, repos, held)`. It is sync and reads files only, so it sits before the existing `await`.

See all three rows pass.

**Mutation.** Drop the `namespace_problem` clause from the skip test in `_repository_id`. `[addon-namespace]` and `[reserved]` should fail.

```bash
just test tests/api/test_repos_library.py
just lint
```

---

### Task 3: The workspace-connect door mints past them, and refuses a carried one

**Files**

- `src/kraft/api/routes/repos.py`
- `tests/api/test_repos_workspaces.py`
- `docs/intent/templates-v1.md` (pin repoint)

**Test first (mint).** Parametrize `test_connecting_a_workspace_declares_it_with_its_submodules_as_members` (`tests/api/test_repos_workspaces.py:27-45`):

```python
@pytest.mark.parametrize(
    "folder, addon, member",
    [
        pytest.param("a", False, "a", id="own-name"),
        pytest.param("release", True, "release-2", id="addon-namespace"),
        pytest.param("kraft", False, "kraft-2", id="reserved"),
    ],
)
```

- Use `make_repo_with_submodule(tmp_path, submodule_path=f"libs/{folder}")`.
- When `addon` is set, call `load_release(client, tmp_path)` before the connect.
- Assert `ids == {str(root): "ws", str(root / f"libs/{folder}"): member}`, and that the workspace's `members` is `{member: {"repository": member, "path": f"libs/{folder}"}}`.
- For `[addon-namespace]`, also assert that `release@acme` still loads: `[p.left_out for p in load.installed(templates_dir, client.app.state.run_dirs.addons, verify=True) if p.id == "release@acme"] == [None]`. `verify=True` bypasses the memo. Add `templates_dir` to the signature.

Repoint its pin now, since the bare id no longer collects:

```bash
just intent-repoint tests/api/test_repos_workspaces.py::test_connecting_a_workspace_declares_it_with_its_submodules_as_members 'tests/api/test_repos_workspaces.py::test_connecting_a_workspace_declares_it_with_its_submodules_as_members[own-name]'
```

**Test first (refusal, new behaviour).** Add `test_a_member_whose_id_is_an_addon_namespace_refuses_the_connect(tmp_path, client, templates_dir)` after `test_a_member_connected_before_its_root_is_the_workspace_member`:

1. `root, member = make_repo_with_submodule(tmp_path, submodule_path="libs/a")`.
2. `client.post("/api/repos", json={"path": str(member), "test_command": "make test"})`.
3. `load_release(client, tmp_path)` **before** the hand edit: an install refuses an add-on whose namespace is already a repository id (`load.instance_problem`, `load.py:426-427`, pinned by `test_a_namespace_is_refused[taken-by-repo-id]`), so the other order never installs `release@acme`.
4. Give the member `id: release` by hand: `read_yaml`/`write_yaml` (from `kraft.config`) on `templates_dir / "repos.yaml"`. Then snapshot the file's text.
5. `answer = client.post("/api/repos", json={"path": str(root), "enabled": False})`.
6. Assert `answer.status_code == 422`, and that `"is the namespace of add-on release@acme"` and "set another `id`" are both in `answer.json()["detail"]`.
7. Assert `repos.yaml` reads the same as the snapshot: no root entry and no `workspaces:`.

The docstring states why the code is 422 and not 409: `client.ensure_repo` reads a 409 as "already connected".

See `[addon-namespace]` and `[reserved]` fail with `release` and `kraft` minted, and the new test fail with a 201.

```bash
just test tests/api/test_repos_workspaces.py -k 'declares_it_with_its_submodules or addon_namespace_refuses'
```

**Implement**

- `_declare_workspace(workspaces, repos, root, children, held)`. After `root_id = _repository_id(root, repos, held)` and after each `child_id = ...`, add `if why := repo_library.namespace_problem(<id>, held): raise HTTPException(422, why)`. Do this with a small local helper, `_free_id(entry, repos, held) -> str`, which wraps the two calls, so the check is written once.
- `_add_repo`: build `held = repo_library.held_namespaces(st.templates_dir, st.run_dirs.addons)` immediately after `repos, _ = _editable_repos(st)`. That keeps it in the no-`await` stretch the comment at `:481` guards. Pass it to `_declare_workspace`. Nothing is written before the raise, because `save_repos` comes after.

See all rows and the new test pass, and the other tests in the file still pass.

**Mutations**

- Drop the `raise` in `_free_id`. The new test should fail with a 201.
- Change 422 to 409. The new test should fail. (This also documents the `ensure_repo` constraint.)
- Pass `{}` for `held` in `_add_repo`. `[addon-namespace]` should fail.

```bash
just test tests/api/test_repos_workspaces.py tests/api/test_repos.py
just intent
just lint
```

---

### Task 4: Pins and docs

**Files**

- `docs/intent/kraft-addons.md`
- `docs/intent/kraft-repo-libraries.md`
- `docsite/content/5.reference/03.configuration/02.repos/index.md`
- `docsite/content/5.reference/03.configuration/02.repos/3.workspaces.md`
- `docsite/content/5.reference/03.configuration/13.repo-libraries.md`

**Intent**

- Append the two REQs from the spec's "Requirements" block to the end of `docs/intent/kraft-addons.md`, after `a-directory-collection-catalogue-is-read-bounded`:
  - `a-minted-repository-id-skips-addon-namespaces`
  - `a-workspace-never-names-an-addon-namespace-id`
- Use a blank line between the heading and the sentence, as the file does.
- In `docs/intent/kraft-repo-libraries.md:33-37` (`a-repo-id-must-be-free-to-be-a-namespace`), change "an installed add-on's namespace" to "an add-on's namespace or one a pending `as:` in `addons.yaml` would take". Append `, tests/addons/test_repo_library.py::test_an_id_that_cannot_be_a_namespace_is_refused[a-pending-alias]` to its `enforced-by:`. The id is unchanged, so this is not a removal.
- Confirm the `templates-v1.md:1384` repoint from Task 3 is in place.

```bash
just intent
just test tests/test_intent_origins.py
```

**Docs**

- `02.repos/index.md:52`, the `id` row. Suggested cell text: "The repository id a workspace names this entry by, unique. Connecting a repo with submodules writes one for its root and members, never `kraft` or an add-on's namespace: `release` becomes `release-2`." (About 33 words; the cell limit is 40.) Also check line 108, "Accepting a repo library writes an `id`…", which still reads true.
- `13.repo-libraries.md:55`. Suggested text: "Accepting is refused when the id is `kraft`, is an add-on's namespace (one a pending `as:` would take included), or is longer than 64 characters. The message says to set another `id` on the entry in `repos.yaml`. Accepting writes an `id` when the entry has none, made from its name and never `kraft` or an add-on's namespace."
- `3.workspaces.md`, after the paragraph at :44. Suggested text: "If that entry's `id` is already `kraft` or an add-on's namespace, the connect is refused and names the add-on. Set another `id` on the entry in `repos.yaml`, then connect again."

```bash
uv run python dev/check_docs_walls.py docsite/content/5.reference/03.configuration/02.repos/index.md
uv run python dev/check_docs_walls.py docsite/content/5.reference/03.configuration/02.repos/3.workspaces.md
uv run python dev/check_docs_walls.py docsite/content/5.reference/03.configuration/13.repo-libraries.md
just lint
just check-tests
```

Commit.

---

### Task 5: Final verification and the PR

**Merge the integration branch in** (nothing should have landed before you, but check): `git fetch origin && git merge origin/ccr-143df22f-uetbpy`. If a sibling has landed, resolve as **Coordination** says.

```bash
just lint
just intent
just check-tests
just test tests/addons/test_repo_library.py tests/api/test_repos_library.py tests/api/test_repos_workspaces.py tests/api/test_repos.py tests/addons/test_update.py tests/api/test_config_check.py tests/test_intent_origins.py
just test            # testmon: everything else this branch touched
wc -l tests/addons/test_repo_library.py tests/api/test_repos_library.py tests/api/test_repos_workspaces.py   # each <= 800
```

Write the PR body to a file outside the worktree (`${TMPDIR:-/tmp}/pr-body-1.md`), then `uv run python dev/check_removals.py origin/ccr-143df22f-uetbpy "${TMPDIR:-/tmp}/pr-body-1.md"` (exit 0). Open it with `gh pr create --base ccr-143df22f-uetbpy --label release::none --title "A minted repository id never takes an add-on's namespace" --body-file "${TMPDIR:-/tmp}/pr-body-1.md"`.

**PR body**

- Base branch: `ccr-143df22f-uetbpy` (the batch's integration branch, DECISIONS D1), not `main`.
- Label: `release::none`.
  - Why: add-ons (#700) and repo libraries (#726, #727) are both after v2.0.0, the latest tag. No released Kraft has an add-on namespace that a minted id could take, so the fix ships inside the release that first ships add-ons. Workspace id minting did ship in v2.0.0, but with nothing to collide with.
  - If a release is cut before this merges, it becomes `release::patch`.
- `## Changelog` (DECISIONS D6/D9: the final PR collects it): "Connecting a repo with submodules, or taking a repo library, no longer gives a repository an add-on's namespace (or `kraft`) as its id; such an id now becomes `<name>-2`."
- `## Removed tests`: none. Parametrizing keeps each function's id, and no case is dropped.
- `## Removed requirements`: none. Two REQs are added and one has its text extended. Mention the repointed pin: `templates-v1.md`, `…as_members` → `…as_members[own-name]`.
- `## Test evidence`: paste the last lines of each command above (`just lint`, `just intent`, `just check-tests`, both `just test` runs, `check_removals`), as run on the merged head.
- Mutations table, one row per mutation above ("applied, confirmed failing, reverted"):

  | Mutation | Kills |
  |---|---|
  | No `AddonsConfig` loop in `held_namespaces` | `test_repo_library.py::…[a-pending-alias]` |
  | No reserved branch in `namespace_problem` | `[reserved]` rows |
  | No `namespace_problem` skip in `_repository_id` | `test_repos_library.py::…[addon-namespace]`, `[reserved]` |
  | `held={}` in `_add_repo` | `test_repos_workspaces.py::…[addon-namespace]` |
  | No raise in `_free_id` | `…refuses_the_connect` |
  | 422 → 409 | `…refuses_the_connect` |

- Docs pages touched: the three under Task 4. They fall under CONTRIBUTING's `repos.yaml` field row and its repo-library row.

---

## Coordination

Four items are built in parallel off `ccr-143df22f-uetbpy` and merge in the order 1, 3, 2, 4. You merge first, so you rebase onto nothing, but keep these stable for the others:

- **Item 4 (repo libraries scoped to their repo) merges after you** and edits the same files:
  - `api/routes/repos.py`: it adds a scope check inside `_validate_repos` (called from `_add_repo` after your `_declare_workspace` and from `repo_library_accept`). Do not move or rename `_validate_repos`; your `held` must stay computed before it in `_add_repo`.
  - `addons/repo_library.py` `check`: it adds every connected repo id to `others` (`:371`), two lines below your `_id_problem(repo_id, held_namespaces(...))` call. Keep `loaded = list(load.installed(...))` where it is: item 4 also reads it.
  - `tests/api/test_repos_library.py`: it parametrizes `test_disconnect_is_refused_while_something_names_the_library` and adds `test_another_repos_entry_may_not_name_a_repo_library`, both through `_with_library`/`_accepted`. Keep `_with_library(tmp_path, client, name="app")`'s default so their calls are unchanged.
  - `docsite/.../13.repo-libraries.md`: it edits :6/:45/:53 and adds a section; you edit the `id` lines near :55. Textual only.
  - Item 4 reserves every connected repo id as a namespace on the plugin side; your `held_namespaces` is the add-on side. They compose and neither reads the other's set (spec 1 Decisions). No cross-item test row is owed by you.
- **Item 2 (store reads checked against the digest)** edits `repo_library.check` at `:381` and `:399-403` and adds a row to `tests/addons/test_repo_library.py::test_a_change_is_reviewed_against_the_accepted_version`. No overlap with your lines.
- **Item 3** touches nothing you do.
