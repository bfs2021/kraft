# Plan: a repo library is visible only to its own repository's items

Spec: `4-repo-library-scoped-to-its-repo.md` (read its **Decisions** first). Base: the integration branch `ccr-143df22f-uetbpy` (main f024b41 today). This item merges **last** of four (order 1, 3, 2, 4). Read **Coordination** at the end before Task 1: you start in parallel, merge the integration branch in once item 1 has landed (DECISIONS D4), and again before your PR, and you own every cross-item test row (DECISIONS D7).

### Task 0: Set up

```bash
git fetch origin
git switch ccr-143df22f-uetbpy-4-repo-library-scope 2>/dev/null || git switch -c ccr-143df22f-uetbpy-4-repo-library-scope origin/ccr-143df22f-uetbpy
uv tool install rust-just   # just is not preinstalled
just setup                  # uv sync + npm ci (Task 9 needs the frontend)
```

Read `CLAUDE.md`, `docs/testing.md` and CONTRIBUTING's "Removed tests" and "Pull requests and release labels". If your session was given another branch name, use it; it must start from `origin/ccr-143df22f-uetbpy`. Whenever a sibling lands (`git log --oneline origin/ccr-143df22f-uetbpy`), `git merge origin/ccr-143df22f-uetbpy` at the next task boundary and resolve as **Coordination** says.

Ground rules for every task (CLAUDE.md, `docs/testing.md`):

- Tests first. Run a new row and see it fail for the reason the task names before writing the code.
- A fix adds a row (`pytest.param(..., id=...)`), not a function. A new `def test_` is for a new behaviour. Grep `tests/support/` before writing a helper: `support.addons` has `repo_with_library`, `repo_library_files`, `accept_repo_library`, `instance`, `install`, `make_collection`, `chain`, `AGENT`, `pinned_chain`; `support.harness` has `make_repo`, `write`, `git`, `entry_of`, `v1_chain`, `v1_resolved`.
- Mutation check for every new pin: break the line the task names, run that one case with `just test <path> -k '<name> and <id>'`, confirm it fails for that reason, revert. Note each in the PR (see the last task).
- Never raw `pytest`. `just test <paths>`; `just lint` and `just check-tests` before each commit.
- **Line budget** (`dev/check_tests.py`, 800 per test file; DECISIONS D11). Add nothing to: `tests/test_intake_poller.py` (786), `tests/api/test_deps.py` (800), `tests/api/test_repos.py` (792), `tests/addons/test_update.py` (794, and item 2 takes it to 797), `tests/executor/test_dispatch.py` (896 of an allowlisted 898), `tests/adapters/test_agent.py` (855 of 856). Shared files, as they will stand after items 1-3 land: `tests/addons/test_pins.py` ~400 (you add ~110), `tests/addons/test_repo_library.py` ~702 (you add ~45; if `wc -l` would pass 790, put your new test in a new `tests/addons/test_repo_library_scope.py` instead). Run `wc -l` on every test file you grew before each commit.
- Every module under `src/` keeps `from __future__ import annotations`; Python 3.12 floor.
- One commit per task.

Overlaps with the sibling items are in **Coordination** at the end: item 1 (`routes/repos.py`, `repo_library.check`), item 2 (`load.for_item`, `support.addons.installed`, `13.repo-libraries.md`), item 3 (`templates/revision.py`, `tests/addons/test_pins.py`).

---

### Task 1: The scope primitive

Files: `src/kraft/addons/load.py`, `tests/addons/test_load.py`.

Add to `load.py` (leaf module: no top-level import of `kraft.templates` or `kraft.config`):

```python
def scope_message(name: str, repo_id: str) -> str:
    return f"{name} is in {repo_id}'s repo library, visible only to items in {repo_id}"

def out_of_scope(name: object, owner: str | None, repo_ids: Collection[str]) -> str | None:
    """`name` (`<q>:<x>`) names a connected repository's library from outside it."""

def scope_problem(pins: Mapping[str, Mapping[str, str | None]] | None, repo_id: str | None) -> str | None:
    """The first pin `library@repo:Y` with Y != repo_id, as
    f"it reads {scope_message(f'{Y}:', Y)}"; None when every pin is in scope.
    repo_id None (no repository, or an entry with no id) refuses every repo library."""

def scoped(addons: Iterable[InstalledAddon], repo_id: str | None, keep: Collection[str] = ()) -> tuple[InstalledAddon, ...]:
    """`addons` with each repo library that is not repo_id's and whose namespace is
    not in `keep` replaced by a copy with left_out=scope_message(f"{ns}:", ns), quiet=True.
    Never dropped: a missing namespace would be read as another tool's plugin."""
```

Use `InstalledAddon.repo_id` for the pin id (`library@repo:Y`); write one small `_pin_repo(pin) -> str | None` that reuses the same `_REPO` prefix logic rather than a second parser.

Tests first (`tests/addons/test_load.py`, new function `test_scope_problem`, one row each): `own-repo` (None), `another-repo` (message names `other`), `no-repo-id` (refused), `addon-pin-is-not-scoped` (`release@acme` passes), `no-pins` (None). New function `test_scoped_leaves_another_repos_library_out`: rows `another` (left_out set, quiet, still present), `own` (unchanged), `kept` (namespace in `keep` unchanged), `addon` (unchanged).

Mutation: make `scope_problem` compare `!=` to `==`; `another-repo` and `own-repo` fail. Make `scoped` filter instead of replace; `another` fails on presence.

Commands: `just test tests/addons/test_load.py -k 'scope'`, `just lint`, `just check-tests`.

### Task 2: `_pins` reads references, not prose

Files: `src/kraft/templates/library.py` (`_pins`, a helper `_qualified_names(data)` beside `_profile_names`), `tests/addons/test_pins.py`.

Replace the `json.dumps` + regex in `_pins` (`library.py:712-731`). `named` becomes a set of names: the chain `id`; each `references(id)` value with its `<section>.` prefix dropped; every `skill` and `profile` string and every `steering` list item found by walking the dumped chain (this catches task and `fallback:` entries, `judge`, `auto_review`, `escalation`); `_fallback_profiles(data)`. Pin an add-on when `name.partition(":")[0] == addon.namespace` for some name. Drop `import re`/`json` if nothing else in the module uses them.

Tests first: parametrize `test_a_chain_that_reads_no_addon_stores_no_pins` (`tests/addons/test_pins.py:195`, no intent pin on it) with `plain` (as today) and `prose-names-a-namespace` (a local chain whose task prompt is `"release: write the notes"` and whose `model:` is `"release:x"`; expect `resolved.addons == {}`). The existing rows of `test_a_resolved_chain_pins_the_addons_it_reads`, `test_a_chain_that_only_extends_an_addon_pins_it...`, `test_a_local_profiles_fallback_pins_the_addon_it_names` and `test_a_chain_through_a_repo_library_pins_its_commit_and_is_restored` must stay green: they are the positive side.

Mutation: put `json.dumps(data)` back into `named`; `prose-names-a-namespace` fails. Drop the `references()` names; `test_a_chain_that_only_extends_an_addon_pins_it...` fails.

Commands: `just test tests/addons/test_pins.py tests/templates/test_library_addons.py`, `just lint`.

### Task 3: Intake doors, the chain switch and repository steering

Files: `src/kraft/api/deps.py`, `src/kraft/api/routes/work_items.py`, `src/kraft/intake.py`, `src/kraft/triggers.py`, `tests/api/test_deps_repo_library.py` (81 lines now; the door table goes here), `tests/test_triggers.py`.

Code:

- `deps.scoped_chain_or_422(st, entry: RepoEntry, name: str | None)`: `resolve_chain_or_422(st, name)`, then `if why := addons_load.scope_problem(chain.addons, entry.id): raise HTTPException(422, f"chain {name or 'default'!r}: {why}")`.
- `intake_chain_or_422` (`deps.py:716-722`) calls it with the `connected_or_422` entry it already has. That covers `POST /work-items` (`work_items.py:335`), duplicate (`:654`) and `POST /triggers` (`:780`).
- Duplicate's `chain_template is None` branch (`work_items.py:649-652`): `deps.scoped_chain_or_422(st, deps.connected_or_422(st, row["repo"]), None)`.
- PATCH switch (`work_items.py:1109`): `deps.scoped_chain_or_422(st, deps.connected_or_422(st, row["repo"]), body.chain_template)`.
- Auto-intake (`intake.py:157`): after `resolve_chain`, `if why := scope_problem(chain.addons, repo.id): logger.warning("auto-intake: %s: %s, skipping", repo.path, why); return None`.
- Cron (`triggers.py:96`): move the `connected_or_422` block above `resolve_chain` and keep the entry; after resolving, `scope_problem(chain.addons, entry.id)` logs `"%s: %s, skipped"` and continues.
- `deps.repository_steering` (`deps.py:999-1021`): before `steering_mod.select`, for each entry and each name, `addons_load.out_of_scope(name, e.id, ids)` where `ids` is every connected entry's `id`; raise `steering_mod.SteeringError(f"repos.yaml: {e.path}: steering {why}")`. Every door already maps that to 422 or a logged skip.

Tests first, in `tests/api/test_deps_repo_library.py`. Setup: two repos with `repo_with_library(tmp_path, "app")` and `make_repo(tmp_path, "web")`, `accept_repo_library(...)` for `app`, connect `web` with an id, `deps._reload_templates(st)`. One table `test_a_repo_library_is_refused_outside_its_repo`:

| id | door | expect |
|---|---|---|
| `create-for-another-repo` | `POST /api/work-items` repo=web, chain `app:ship` | 422, "visible only to items in app" |
| `duplicate-for-another-repo` | file on web via a hand-written row pinned to app (`item_on`/`pinned_chain`), then `POST .../duplicate` | 422 |
| `trigger-route-for-another-repo` | `POST /api/triggers` repo=web, chain `app:ship` | 422 |
| `switch-for-another-repo` | file paused on web with `default`, `PATCH` chain `app:ship` | 422, row unchanged |
| `steering-of-another-repo` | web's entry `steering: [app:tone]` written on disk, `POST /api/work-items` | 422 |

and `test_a_repo_library_is_used_by_its_own_repo` rows: `create-own` (201, `chain_template == "app:ship"`), `default-own` (no chain, entry unset: `app:default` when the library has it), `switch-own` (200).

`tests/test_triggers.py` (299 lines) has no skip table: add a new test `test_a_trigger_naming_another_repos_library_is_skipped_not_the_whole_tick`, modeled on `test_a_trigger_naming_an_unconnected_repo_is_skipped_not_the_whole_tick` (`:214`), parametrized `another-repos-library` (nothing filed, the warning names `app`) and `own-repos-library` (filed). Auto-intake: add the row to `tests/api/test_deps_repo_library.py` calling `intake._start(app, entry_for_web, row)` with web's entry `default_chain: app:ship` written on disk; expect `None` and the warning. Do not touch `tests/test_intake_poller.py` (line budget).

Workspace rows: `root, sub = make_repo_with_submodule(tmp_path, submodule_path="libs/pkg")` (root `ws`, member repo `pkg`); `with_origin(root)` and `with_origin(sub)`, then `repo_library_files(root)` and `repo_library_files(sub)` (each needs an `origin` to push to). Connect `sub` alone, then the root: the root's connect declares the workspace and names `sub`'s entry as its member, as in `tests/api/test_repos_workspaces.py::test_a_member_connected_before_its_root_is_the_workspace_member[member-is-its-origin]`. Read both ids from `GET /api/repos`, `accept_repo_library(st.templates_dir, st.run_dirs.addons, <repo>, <id>)` each, then `deps._reload_templates(st)`. `test_a_repo_library_is_used_by_its_own_repo[workspace-roots-library]`: `POST /api/work-items` on the workspace with chain `<root id>:ship` answers 201. `test_a_repo_library_is_refused_outside_its_repo[workspace-members-library]`: chain `<member id>:ship` answers 422. These two rows need their own setup: make them a separate parametrized setup branch (a `workspace` flag) rather than forcing the two-repo setup onto them.

Mutation: in `scoped_chain_or_422` pass `None` for the id; every `-own` row fails. Delete the PATCH call; `switch-for-another-repo` fails. Delete the trigger check; the trigger row fails.

Commands: `just test tests/api/test_deps_repo_library.py tests/test_triggers.py tests/api/test_duplicate_intake.py tests/api/test_intake_connected.py tests/api/test_repos_workspaces.py`, `just lint`, `just check-tests`.

### Task 4: Revisions resolve in the item's scope

Files: `src/kraft/templates/revision.py`, `src/kraft/templates/library.py` (`_Resolution._parent`), `src/kraft/drafts/item.py`, `src/kraft/api/routes/gates.py`, `src/kraft/api/routes/artifacts.py`, `src/kraft/api/routes/drafts.py`, `src/kraft/api/deps.py` (`launch`), `tests/addons/test_pins.py` or `tests/templates/test_revision.py`.

Code:

- `revise(chain, changes, *, at, library, repo_id: str | None = None)`; pass it on in the recursive call (`revision.py:349`), and from `render(..., repo_id=None)` and `artifact_digest(..., repo_id=None)`. None means "no repository": every repo library is out of scope for an added node; add-ons are never scoped (DECISIONS D10). That is why item 3's rows, which name only add-ons and local components, need no `repo_id`: not because of the default. Every production caller below passes the item's id explicitly; check with `grep -rn "revision.revise(\|revision.render(\|artifact_digest\|item.evaluate(" src` that each hit passes `repo_id=`.
- `render`: item 3 has already changed its add line to name the source (`` from `release:stage` ``, `_sources`). Change only the signature and the `revise` call; keep that line.
- `_pinned(library, chain, repo_id)`: `None` for no library; otherwise `library.with_addons(load.scoped(<addons>, repo_id, keep=pins))`, where `<addons>` is `load.for_item(pins, ..., repo_id=repo_id)` when the chain has pins (today's path; pass `config_dir=library.library_path.parent` when `library_path` is set, so a test never reads the developer's home) and `library.addons` when it has none. Skip the rebuild when no addon in `library.addons` would change (no pins and no out-of-scope repo library).
- `_added_nodes(adds, library, repo_id)`: after `resolve_chain`, `if why := load.scope_problem(resolved.addons, repo_id): raise RevisionError(f"add: {why}")`.
- `_Resolution._parent` (`library.py:1037-1041`): when `":" in name` and the qualifier is a known left-out addon of `self._library.addons`, append `f"; {addon.left_out}"`. That is how a scoped-out `extends` says why.
- `drafts/item.evaluate(..., repo_id)`; callers `routes/drafts.py:468,536` pass the item's id.
- Callers pass the item's id: `gates.py:129`, `artifacts.py:401,504`. Add `deps.item_repo_id(st, row) -> str | None` (`_connected(load_repos, row["repo"])`, None on a `ConfigError` or no entry) and use it in all four; `deps.launch` binds `repo_id=entry.id` into its `chain_revision_digest` partial (`deps.py:1047`).

Tests first, in `tests/addons/test_pins.py` (it stays far under 800). A repo library's default `library.yaml` (`repo_library_files`) holds a task `base` and no node, so every row extends the task `app:base`. Use `accept_repo_library(config_dir, addons_dir, repo_with_library(tmp_path), "app")` inside the test, after the `home` fixture, as `test_a_chain_through_a_repo_library_pins_its_commit_and_is_restored` does, and write a second entry `{"path": "/web", "id": "web"}` into `repos.yaml`. New test `test_a_revision_adds_only_from_the_items_own_repo_library`, rows:

| id | added node | `repo_id` | expect |
|---|---|---|---|
| `own-repo` | through a local node: `library.yaml` node `via_app` whose task extends `app:base`; `AddedNode(id="x", extends="via_app")` | `"app"` | revised; `revised.chain.addons` gains `app` |
| `another-repo` | the same local node | `"web"` | `RevisionError` matching `visible only to items in app` |
| `another-repo-direct` | `AddedNode(id="x", tasks=[{"id": "t", "extends": "app:base"}])` (needs item 3's `QualifiedIdentifier`, landed before you: the cross-item row, DECISIONS D7) | `"web"` | the same |
| `no-repo` | the direct form | `None` | the same |

And one route-level row so a production caller that forgets `repo_id` fails: in `tests/api/test_deps_repo_library.py`, `test_a_repo_library_is_used_by_its_own_repo[draft-adds-own]`: an item filed paused on `app`, then `PUT /api/work-items/{id}/draft` with `{"op": "add_node", "after": "verification", "node": {"id": "x", "tasks": [{"id": "t", "extends": "app:base"}]}}` answers 200 with `problems == []` (the body shape is `tests/api/test_item_drafts.py`'s `ADD`).

Mutation: drop the `scope_problem` call and make `_pinned` return `library` unchanged; `another-repo` and `another-repo-direct` fail. Revert only the `_parent` suffix; `another-repo` asserts the left-out reason in the message, so it fails too. Drop `repo_id=` at `routes/drafts.py:468`; `draft-adds-own` fails.

Commands: `just test tests/addons/test_pins.py tests/templates/test_revision.py tests/api/test_chain_revision_gate.py tests/api/test_item_drafts.py tests/drafts/test_item.py tests/executor/test_walk_revised.py tests/api/test_deps_repo_library.py`, `just lint`.

### Task 5: Launch sees only its own repository's library

Files: `src/kraft/addons/load.py` (`for_item`), `src/kraft/adapters/profiles.py` (`harness_table`), `src/kraft/adapters/agent.py` (`resolve_agent_task`), `src/kraft/executor/context.py` (`LaunchContext`), `src/kraft/api/deps.py` (`launch`), `src/kraft/executor/dispatch.py`, `src/kraft/gate_review.py`, `src/kraft/escalate.py`, `src/kraft/review_reply.py`, `src/kraft/api/routes/sessions.py`, `src/kraft/api/routes/settings.py` (steering preview), `src/kraft/doctor.py` (`_cost_checks`), `tests/addons/test_pins.py`.

Code:

- `for_item(pins, config_dir=None, addons_root=None, *, repo_id: str | None)` (required keyword): `live = scoped(installed(...) minus pinned namespaces, repo_id)`. If item 2 has landed, its `_launch_problem` pass (an edited store's `left_out`) must run **after** `scoped`, over entries still loading, so an out-of-scope store is never hashed (DECISIONS D13). Then, reading `repos.yaml` from the same `config_dir` (`read_yaml`, nothing on a `ConfigError`), one `InstalledAddon(repo_library_id(id), "library", id, "", store / "not-accepted", left_out=f"repository {id!r} has no accepted repo library", quiet=True)` for each connected id that no live or pinned entry already has as its namespace. That is the reservation (`REQ a-repo-id-is-never-another-tools-plugin`). Pinned entries are unchanged.
- Update every caller (`grep -rn "for_item(" src tests | grep -v progress_mod`): `dispatch.restore_pins` (`dispatch.py:470`, `repo_id=None` is fine, it keeps pinned only), `revision._pinned` (Task 4), `profiles.harness_table` (`profiles.py:47`), `agent.resolve_agent_task` (`agent.py:362`), `tests/addons/test_pins.py:150`. The `harness_table` callers that pass no pins (`profiles.py:59`, `policy.py:294`, `doctor.py:792`) get `repo_id=None`: an instance-wide table never includes a repo library's profiles.
- `harness_table(harnesses, pins=None, repo_id=None)` passes `repo_id` to `for_item`.
- `resolve_agent_task(..., repo_id: str | None = None)`: pass it to `harness_table` and `for_item`. Extend the loop at `agent.py:362-370`: for an addon not in `pins`, with `repo_id is not None` set on it (a repo library) and `left_out` set, that `_reads_namespace(task, table, ns)`: raise `_skill.SkillError(f"{task.skill}: {addon.left_out}")` when `task.skill` is in that namespace, else `ProfileUnavailable(f"{<the profile or fallback profile>}: {addon.left_out}")`. Use the entry's own `left_out` in every case, never a rebuilt scope message: `scoped` and the reservation already put the scope text there, and after item 2 an own-repo library whose store was edited carries item 2's digest message instead, which must not read as "visible only to items in ..." (DECISIONS D13). The `addon_dirs` None entry stays as the second guard.
- `LaunchContext.item_repo_id: str | None = None`; `deps.launch` sets it from the entry it finds (None on the poisoned path); `_fan_out`'s `replace(base, repo_entry=entry)` keeps it.
- Pass `repo_id=launch.item_repo_id if launch else None` at `dispatch.py:1301` (to `harness_table`) and `:1316`, `gate_review.py:100` (thread the id in beside `pins`) and `:279`, `escalate.py:532`, `review_reply.py:148`, `sessions.py:163`.
- Steering preview (`settings.py:205-245`): after finding `entry`, `if why := scope_problem(resolved.addons, entry.id): raise HTTPException(422, f"{chain}: {why}")`; then pass `addons=resolved.addons, repo_id=entry.id`.
- Doctor `_cost_checks` (`doctor.py:773-819`): per chain, `table = agent.harness_table(harnesses, chain.addons)[0]` (not one shared table) and `resolve_agent_task(c, None, None, harnesses=harnesses, steering=chain.steering, addons=chain.addons)`; catch `skill_mod.SkillError` with the other two.

Tests first, in `tests/addons/test_pins.py` (never `tests/adapters/test_agent.py`, at 855 of 856). The `home` fixture plus `accept_repo_library` for `app` (a repo built with `repo_with_library(tmp_path, skills={"notes": "the app method"}, extra={".kraft/profiles.yaml": yaml.safe_dump({"profiles": {"deep": {"model": {"codex": "gpt-5"}}}})})`), plus a second connected repo `web` with an id and no library. One test `test_a_launch_reads_only_its_own_repos_library`:

| id | task | pins | repo_id | expect |
|---|---|---|---|---|
| `own-repo-skill` | `skill: app:notes` | none | `app` | method text read from app's store |
| `another-repos-skill` | `skill: app:notes` | none | `web` | `SkillError`, "visible only to items in app"; never `PLUGIN_PROMPT` |
| `another-repos-profile` | `profile: app:deep` | none | `web` | `ProfileUnavailable`, same words |
| `pinned-before-the-change` | `skill: app:notes` | app's pin | `web` | read (Choice 5) |
| `reserved-id-not-delegated` | `skill: web:notes` | none | `app` | `SkillError`; never `PLUGIN_PROMPT` |
| `another-tools-plugin` | `skill: superpowers:brainstorm` | none | `app` | `PLUGIN_PROMPT` (unchanged) |
| `own-repo-edited-store` | `profile: app:deep` | none | `app` | after `edit_store(<app's store>, "profiles.yaml", ...)` (item 2's helper): stops with `does not match its digest`, and `visible only` is not in the message. The cross-item row (DECISIONS D7); write it once item 2 has landed |

`LaunchContext.item_repo_id`: a new test in `tests/api/test_deps_repo_library.py` (not `tests/api/test_deps.py`, which is at 800), `test_a_launch_carries_its_items_repository_id`, rows `single-repo` (`deps.launch(st, str(app)).item_repo_id == "app"`) and `poisoned-repos-yaml` (an unreadable `repos.yaml`: `None`). The fan-out keeps it by `dataclasses.replace`; if you pin that, put the row in `tests/executor/test_dispatch_pins.py` (38 lines), never `tests/executor/test_dispatch.py` (896 of an allowlisted 898).

Mutation: make `scoped` keep every repo library loaded; `another-repos-skill` fails (it reads app's text). Drop the reservation loop; `reserved-id-not-delegated` returns `PLUGIN_PROMPT` and fails. Make `scoped` drop instead of replace; `another-repos-skill` fails with `PLUGIN_PROMPT`. Raise a rebuilt `scope_message` instead of `addon.left_out`; `own-repo-edited-store` fails.

Commands: `just test tests/addons/test_pins.py tests/test_skill.py tests/test_doctor_addons.py tests/api/test_settings_templates.py tests/api/test_deps_repo_library.py tests/api/test_harnesses.py tests/test_escalate.py tests/test_review_reply.py tests/executor`, `just lint`, `just check-tests`.

### Task 6: The static rule over config files

Files: `src/kraft/config.py` (`connected_entry`), `src/kraft/api/deps.py` (`_connected` delegates), `src/kraft/addons/update.py` (`scoped_references`, `scope_problems`), `src/kraft/api/config_check.py`, `src/kraft/api/routes/repos.py` (`_validate_repos`), `src/kraft/api/routes/settings.py` (`put_intake`, `put_policy`), `src/kraft/drafts/repos.py`, `src/kraft/drafts/intake.py`, `src/kraft/doctor.py` (`_repo_libraries_check`, `_addon_checks`), tests in `tests/api/test_config_check.py`, `tests/api/test_repos_library.py`, `tests/drafts/test_repos.py` (205 lines) and `tests/drafts/test_intake.py` (195 lines), `tests/test_doctor_addons.py`, `docs/intent/kraft-repo-libraries.md` (the repoint below).

Code:

- `config.connected_entry(repos, path)`: the body of `deps._connected` (`deps.py:733-751`); `_connected` calls it. One path rule.
- `update.scoped_references(config_dir, repos=None, *, replacing=None)`: the walk of `references()` with a fifth field, the owner. For `repos.yaml`, walk each `repos[i]` entry on its own with owner `entry.get("id")`; for `intake.yaml` `schedules[i]` and `policy.yaml` `triggers[i]`, owner is `connected_entry(<repos>, item["repo"]).id`; elsewhere None. `replacing: Mapping[str, object]` is parsed data to read in place of a file. `references()` becomes `((w, k, kind, v) for w, k, kind, v, _ in scoped_references(...))`, signature unchanged.
- `update.scope_problems(config_dir, repos=None, *, replacing=None) -> list[tuple[str, str]]`: `(rel, f"{where}: {key} {why}")` for each reference where `load.out_of_scope(value, owner, ids)` is set, `ids` being every connected entry's `id` in the (candidate) `repos.yaml`.
- `config_check`: a helper `_scope_issues(path, rel, data, ctx)` returning `TemplateIssue(path, chain_or_None, message)` for problems in `rel` only, with `replacing={rel: data}`; call it at the end of `_check_chain` (rel `chains/<id>.yaml`, chain id set), `_check_library`, `_check_repos` (also pass `repos=data`), `_check_intake`, `_check_harnesses`, `_check_policy`. `lint_report` appends every problem (chain issues named by their chain so `chains` drops them).
- `_validate_repos` (`routes/repos.py:233-253`): `scope_problems(st.templates_dir, repos={"repos": repos, "workspaces": workspaces})`, 422 on the first, only for entries of `repos.yaml` (so a disconnect is not refused by someone else's file). `steering=False` callers (disconnect) skip it.
- `put_intake`, `put_policy`: the same over the candidate data before saving; 422.
- `drafts/repos.py` `resolve` (`:207-228`): a per-entry `_problem(entry.path, "default_chain"|"steering", why)` from the rule, and drop config_check's identical file-level message. `drafts/intake.py` `_schedule_problems`: a `chain` problem from the rule; widen `_SCHEDULE_CRON` to `schedules\.\d+\.(cron|chain)` and give the config_check issue that loc.
- Doctor: `_repo_libraries_check` takes the problems (`update.scope_problems(templates)`) and fails listing each, ahead of its other faults; `_addon_checks` passes them. Keep every row emitted on every path (the comment at `doctor.py:246-251`).

Tests first:

- `tests/api/test_config_check.py`: one table `test_a_repo_library_is_named_only_from_its_repo` over `config_check.check(rel, text, ctx)`, rows `local-chain-extends` (`chains/mine.yaml` extends `app:base`), `library-extends`, `harnesses-fallback` (`profiles.fast.fallback[0].profile: app:deep`), `another-repos-default-chain`, `another-repos-steering`, `intake-schedule-for-another-repo`, `policy-trigger-for-another-repo`, `reserved-id-with-no-library` (`skill: web:x` in a local chain, `web` connected), and in-scope rows `own-default-chain`, `own-steering`, `own-schedule`, `addon-reference` (no issue). Expect the message tail "visible only to items in app".
- `tests/api/test_repos_library.py`: new test `test_another_repos_entry_may_not_name_a_repo_library` with rows `post-default-chain`, `patch-default-chain`, `patch-steering` (422, file unchanged). Parametrize `test_disconnect_is_refused_while_something_names_the_library` (`:89-97`): `its-own-schedule` (write `intake.yaml` with a schedule `repo: <app>`, `chain: app:ship`) and `a-hand-edit` (write another entry's `default_chain: app:ship` into `repos.yaml` on disk, bypassing the route). Both still 409 naming the reference.
- Drafts: one row each in `tests/drafts/test_repos.py` and `tests/drafts/test_intake.py`, problem on the entry / schedule, not duplicated at file level.
- Parametrizing `test_disconnect_is_refused_while_something_names_the_library` stops its bare id from collecting, and `docs/intent/kraft-repo-libraries.md:72` (`a-named-repo-library-holds-its-repo`) pins it bare. Repoint in this task, or `just intent` fails: `just intent-repoint tests/api/test_repos_library.py::test_disconnect_is_refused_while_something_names_the_library 'tests/api/test_repos_library.py::test_disconnect_is_refused_while_something_names_the_library[its-own-schedule]'`, then add `…[a-hand-edit]` to the same `enforced-by:` line by hand.
- `tests/test_doctor_addons.py::test_the_repo_libraries_row`: a `named-from-outside` row (fails, names the file and key).
- `kraft admin templates lint`: a row in `tests/api/test_templates_inspection.py` (its `lint_report` test) that the local chain is an issue.

Mutation: make `out_of_scope` return None when `owner is None`; every outside row fails. Drop the owner for `repos.yaml` entries; `own-default-chain` fails. Remove the `_validate_repos` call; `post-default-chain` fails. Remove the doctor wiring; `named-from-outside` fails.

Commands: `just test tests/api/test_config_check.py tests/api/test_repos_library.py tests/drafts/test_repos.py tests/drafts/test_intake.py tests/api/test_settings_intake.py tests/api/test_templates_inspection.py tests/test_doctor_addons.py tests/addons/test_update.py tests/api/test_repos.py tests/api/test_repos_workspaces.py`, `just intent`, `just lint`, `just check-tests`.

### Task 7: A first accept, and reserved ids in add-on checks

Files: `src/kraft/addons/repo_library.py` (`check`), `src/kraft/addons/update.py` (install's `others`, `:541-545`), `tests/addons/test_repo_library.py`, `tests/addons/test_update.py`.

Code:

- `repo_library.check`, where `was is None` (`repo_library.py:415-421`): split `update.scoped_references(config_dir, repos=repos)` with qualifier `repo_id`: owner `repo_id` stays a Reach line (as today); any other is a problem. Add `update.referrers(repo_id, [p for p in loaded if p.repo_id is None])`. Any problem: `return replace(refused(*problems, "change those first"), review=reviewed)`.
- `others` in `repo_library.check` (`:358`) and in the add-on install (`update.py:541-545`) gain every connected repo id (read from `repos.yaml`, the candidate `repos` when given). Adjust the skill message in `update.problems` (`:184-189`) so a repo id reads as "names repository <id>'s repo library namespace", not "another installed Kraft add-on".

Tests first (`tests/addons/test_repo_library.py`: 679 on main, ~702 after items 1 and 2; if your test would take it past 790, put it in a new `tests/addons/test_repo_library_scope.py`):

- New test `test_a_first_accept_is_refused_while_something_outside_names_it`, rows `local-chain` (write `chains/mine.yaml` extending `app:base` before the first check), `another-repos-entry` (a second entry with `default_chain: app:ship`), `an-addons-skill` (install an add-on whose task has `skill: app:notes`, by `install`/`make_collection`; it must be installed before `app` is connected, or Task 7's own install check refuses it: write `repos.yaml` after the install). Expect `outcome == "refused"`, each named.
- Positive row `its-own-entry` (`default_chain: app:ship` on app's own entry): `waiting`, and the Reach line "is now read from this repo library" present.
- `test_a_local_chain_through_the_library_is_in_the_review` (`:246`) and `test_a_local_chain_that_changes_shape_through_the_library_holds` (`:498`) write their local chain after the first accept: they must stay green unchanged (a later change is not refused).
- The install-side check is a new behaviour (a connected repo id is now a reserved namespace for add-on skills). `tests/addons/test_update.py` is at 794 and item 2 takes it to 797, so do not add there: create `tests/addons/test_update_repo_ids.py` (a sibling, as `tests/api/test_repos_library.py` is to `routes/repos.py`) with `test_an_addon_skill_may_not_name_a_connected_repository`, rows `connected-id` (refused, `update.update` result problems name the repository's namespace) and `unconnected-name` (applied). Build it with `support.addons` (`make_collection`, `instance`) and the `update.update(...)` call pattern of `tests/addons/test_pins.py::_update`; do not copy `test_update.py`'s private `_run` (`just check-tests` refuses a copied helper body).

Mutation: drop the `owner != repo_id` split; `its-own-entry` is refused and fails. Drop `referrers`; `an-addons-skill` passes the accept and fails.

Commands: `just test tests/addons/test_repo_library.py tests/addons/test_update.py tests/addons/test_update_repo_ids.py tests/cli/test_repos_library.py tests/api/test_repos_library.py`, `just lint`, `just check-tests`.

### Task 8: A repo library's content is edited in its repository

Files: `src/kraft/templates/catalogue.py` (`read_only_message`, `addon_view`), `src/kraft/drafts/ops.py` (`new_chain`, `copy_component`), `tests/templates/test_catalogue.py`, `tests/api/test_addon_content.py` (the `copy_component` and `new_chain(from=...)` tests).

Code: for an addon with `repo_id`, `read_only_message` says `f"{name} comes from {repo}'s repo library; edit it in that repository's .kraft/"`. `addon_view` adds `"repo": addon.repo_id` (None for an add-on). `new_chain(from=Y:c)` and `copy_component` refuse a repo library's chain or component with `OpError(f"{scope_message(name, repo)}; edit it in that repository's .kraft/")`.

Tests first: rows `repo-library-chain` and `repo-library-component` on the existing copy tests (refused, message names the repository), and a `read_only_message` row. The add-on rows stay as they are.

Mutation: drop the `repo_id` branch in `copy_component`; `repo-library-component` copies and fails.

Commands: `just test tests/templates/test_catalogue.py tests/api/test_addon_content.py tests/api/test_templates_library.py`, `just lint`. Then `just schemas` if `addon_view`'s shape is in the generated VS Code schemas (`git status vscode/schemas` after it).

### Task 9: Pickers show only the chosen repo's library

Files: `frontend/src/types/settings.ts` (`Addon.repo?: string | null`), a helper next to the board's testkit or `frontend/src/ng/library/types.ts` (`chainsForRepo(chains, repo)`, the same rule as `vscode/src/core/fileWork.ts:81` `chainsFor`, reading `addon.repo` with a fallback to the `library@repo:` prefix), `frontend/src/ng/board/Composer.tsx`, `frontend/src/ng/board/draft/DraftItemPage.tsx`, `frontend/src/ng/phone/new/NewItem.tsx`, `frontend/src/ng/shell/FirstRun.tsx` (its default-chain picker), `frontend/src/ng/library/types.ts` (`addonLabel`: `repo library <id>` for one), `frontend/src/ng/templates/addon.tsx` (badge title "From <id>'s repo library: read-only").

Tests first (vitest, `it.each`): `chainsForRepo` rows `own-library-listed`, `another-repos-hidden`, `addon-listed`, `local-listed`, `repo-without-id-hides-every-repo-library`; one Composer test (its testkit) that switching the repo changes the list; `addonLabel` row. The Templates screens keep listing every chain.

Mutation: return `chains` unfiltered; `another-repos-hidden` fails.

Commands: `just test-ui`. Check `frontend/README.md` for whether a picker change also needs `just ui-contract` (the UI contract mocks `/templates/chains`; add `repo` to its fixture if it asserts the shape).

### Task 10: Docs and intent

Files: `docs/intent/kraft-repo-libraries.md`, the docsite pages.

Intent (`docs/intent/kraft-repo-libraries.md`), appended:

```
## REQ a-repo-library-is-visible-only-to-its-repository

The system SHALL resolve `<repo-id>:<name>` only for a work item whose repository (a workspace's root) is `<repo-id>`, for that repository's own `repos.yaml` entry, and for a schedule or trigger whose `repo` is that repository, and SHALL refuse it everywhere else, naming the repository.
enforced-by: tests/addons/test_load.py::test_scope_problem[another-repo], tests/addons/test_load.py::test_scope_problem[no-repo-id], tests/api/test_deps_repo_library.py::test_a_repo_library_is_refused_outside_its_repo[create-for-another-repo], tests/api/test_deps_repo_library.py::test_a_repo_library_is_refused_outside_its_repo[switch-for-another-repo], tests/api/test_deps_repo_library.py::test_a_repo_library_is_refused_outside_its_repo[workspace-members-library], tests/api/test_deps_repo_library.py::test_a_repo_library_is_used_by_its_own_repo[create-own], tests/api/test_deps_repo_library.py::test_a_repo_library_is_used_by_its_own_repo[workspace-roots-library], tests/api/test_deps_repo_library.py::test_a_repo_library_is_used_by_its_own_repo[draft-adds-own], tests/api/test_config_check.py::test_a_repo_library_is_named_only_from_its_repo[local-chain-extends], tests/api/test_config_check.py::test_a_repo_library_is_named_only_from_its_repo[own-default-chain], tests/api/test_repos_library.py::test_another_repos_entry_may_not_name_a_repo_library[patch-default-chain], tests/addons/test_pins.py::test_a_launch_reads_only_its_own_repos_library[own-repo-skill], tests/addons/test_pins.py::test_a_launch_reads_only_its_own_repos_library[another-repos-profile], tests/addons/test_pins.py::test_a_revision_adds_only_from_the_items_own_repo_library[another-repo], tests/addons/test_pins.py::test_a_revision_adds_only_from_the_items_own_repo_library[another-repo-direct], tests/addons/test_pins.py::test_a_revision_adds_only_from_the_items_own_repo_library[own-repo], tests/addons/test_repo_library.py::test_a_first_accept_is_refused_while_something_outside_names_it[local-chain]
origin: src/kraft/addons/load.py §scope_problem

## REQ a-repo-id-is-never-another-tools-plugin

WHILE a repository is connected, the system SHALL NOT hand `<repo-id>:<skill>` to the agent as another tool's plugin, whether or not its library is accepted.
enforced-by: tests/addons/test_pins.py::test_a_launch_reads_only_its_own_repos_library[another-repos-skill], tests/addons/test_pins.py::test_a_launch_reads_only_its_own_repos_library[reserved-id-not-delegated], tests/api/test_config_check.py::test_a_repo_library_is_named_only_from_its_repo[reserved-id-with-no-library], tests/addons/test_update_repo_ids.py::test_an_addon_skill_may_not_name_a_connected_repository[connected-id], tests/addons/test_repo_library.py::test_a_first_accept_is_refused_while_something_outside_names_it[an-addons-skill]
origin: src/kraft/addons/load.py §for_item
```

Every pin above names a test this plan creates (Tasks 1, 3-7). If you moved a test to a sibling file for the line budget (Task 7's `test_repo_library_scope.py`), change its path here. Confirm the ids as collected (`just test <file> --collect-only -q`). The `a-named-repo-library-holds-its-repo` repoint was done in Task 6. Leave `a-change-of-shape-waits-for-a-person` as it is. No other item adds a REQ to this file; item 1 edits the text and pins of `a-repo-id-must-be-free-to-be-a-namespace` (`:33`), which you leave alone. Run `just intent` and `just test tests/test_intent_origins.py`.

Docs (read each page; 80-word paragraph limit, no `#` in shell blocks, no new headings without a landing check):

- `docsite/content/5.reference/03.configuration/13.repo-libraries.md`: :6 (offered to every instance; loaded only for that repository's items), :45 (names), :53 (a connected id is a namespace even with no library), :71 bullet list unchanged, :154 table (the intake callers refuse another repo's), :195 (disconnect lists invalid references too). A new section "Who can name it" with the rule, the message, the workspace root rule and the first-accept refusal. If a heading is renamed, add a `redirects.yml` entry.
- `5.reference/07.triggers.md:30`: `chain` may name a repo library only when `repo` is that repository.
- `5.reference/01.cli/4.repo.md:80` and the "Take a repo's library" section: the first-accept refusal.
- `2.concepts/4.vocabulary.md:225-232`: "loads ... for that repository's items".
- `6.project/1.security.md:529-556`: a bullet, "A repo library reaches only its own repository's items".
- `3.guides/2.customize/4.share-chains-with-addons.md` (the repo-library steps): the scope.
- `4.troubleshooting/4.doctor-failures.md`: the `repo libraries` row's new message. `4.troubleshooting/1.why-did-my-item-stop.md`: the launch stop's message.
- `5.reference/00.web-ui/` and `3.guides/1.day-to-day/3.file-a-work-item.md`: the composer lists only the repo's own library chains.

Commands: `uv run python dev/check_docs_walls.py <page>` for each page, then the other docs checks CI runs (`just lint` is ruff only): `uv run python dev/check_docs_redirects.py`, `uv run python dev/check_docs_landings.py`, `uv run python dev/check_docs_shell.py`, `uv run python dev/check_docs_coverage.py`. Then `just intent`, `just check-tests`, and commit.

### Task 11: Final verification and the PR

1. **Merge the integration branch in:** `git fetch origin && git merge origin/ccr-143df22f-uetbpy`. By now items 1, 3 and 2 have landed. Resolve every conflict as **Coordination** says, and make sure the cross-item rows (`another-repo-direct`, `own-repo-edited-store`) are written and green.
2. **Checks**, on the merged head:

   ```bash
   just lint
   just intent
   just check-tests
   just test tests/addons tests/templates tests/api/test_deps_repo_library.py tests/api/test_repos_library.py tests/api/test_repos_workspaces.py tests/api/test_repos.py tests/api/test_config_check.py tests/api/test_addon_content.py tests/api/test_item_drafts.py tests/api/test_chain_revision_gate.py tests/api/test_templates_inspection.py tests/api/test_settings_intake.py tests/drafts tests/test_triggers.py tests/test_doctor_addons.py tests/test_skill.py tests/executor --no-testmon
   just test            # testmon: everything else this branch touched
   just test-ui
   wc -l tests/addons/test_pins.py tests/addons/test_repo_library.py tests/addons/test_update.py tests/api/test_deps_repo_library.py tests/api/test_config_check.py tests/addons/test_load.py   # each <= 800
   ```

3. Write the PR body to `${TMPDIR:-/tmp}/pr-body-4.md` (outside the worktree), run `uv run python dev/check_removals.py origin/ccr-143df22f-uetbpy "${TMPDIR:-/tmp}/pr-body-4.md"` (exit 0), then `gh pr create --base ccr-143df22f-uetbpy --label release::none --title "A repo library is visible only to its own repository's items" --body-file "${TMPDIR:-/tmp}/pr-body-4.md"`.

**PR body:**

- Base branch: `ccr-143df22f-uetbpy` (DECISIONS D1), not `main`.
- Label: `release::none`. Repo libraries (#726, #727) are in no release (the latest tag, v2.0.0, predates them); this tightens unreleased behaviour. If a release ships them first, relabel `release::minor` and list in the changelog the configurations that now fail.
- `## Changelog` (written even under `release::none`, for the final PR to collect; DECISIONS D6/D9): "A repo library is now visible only to its own repository's items. Another repository's entry, a local chain or library component, `harnesses.yaml`, and schedules for another repository can no longer name it, and a connected repository's id is never handed to an agent as another tool's plugin."
- `## Removed tests`: none expected. `test_disconnect_is_refused_while_something_names_the_library` and `test_a_chain_that_reads_no_addon_stores_no_pins` gain parameters and keep their names. If any test is renamed, moved or folded, list it.
- `## Removed requirements`: none. Name the repoint: `a-named-repo-library-holds-its-repo` → `[its-own-schedule]`, `[a-hand-edit]`.
- `## Test evidence`: paste the last lines of every command in step 2 and of `check_removals`, as run on the merged head.
- A mutation table: one line per task's mutation above, "applied, confirmed failing, reverted".
- Coordination: the sibling PRs (items 1, 3, 2) this was merged onto, and the two cross-item rows this PR adds.

---

## Coordination

Order: 1, 3, 2, **4**. Everything else lands before you. Merge `origin/ccr-143df22f-uetbpy` in after item 1 lands (DECISIONS D4) and again before Task 11; after each merge run the sibling tests named below. You own every row that needs another item's code (DECISIONS D7).

- **Item 1 (minted repo ids never take an add-on namespace)**:
  - `api/routes/repos.py`: it adds a `held` argument to `_repository_id(entry, repos, held)` and `_declare_workspace(..., held)`, a `_free_id` helper that raises 422, and computes `held = repo_library.held_namespaces(...)` in `_add_repo` right after `_editable_repos` and in `_check_library`. Task 6 touches only `_validate_repos`; keep item 1's `held` computed before your `_validate_repos` call in `_add_repo`. Your 422 for a scope breach and item 1's 422 for a namespace id are separate checks; neither replaces the other.
  - `addons/repo_library.py` `check`: item 1 replaces `_id_problem(repo_id, loaded)` with `_id_problem(repo_id, held_namespaces(config_dir, addons_root))` at `:357-359` and adds `held_namespaces`/`namespace_problem`. Task 7 adds connected repo ids to `others` (`:371`) two lines below: textual merge. Keep the two sets separate (spec 1: an id never takes an add-on namespace; yours: an add-on or config never takes a repo id).
  - `tests/api/test_repos_library.py`: item 1 parametrizes `test_a_repo_library_is_reviewed_then_accepted` (ids `own-name`, `addon-namespace`, `reserved`) and gives `_with_library(tmp_path, client, name="app")` a `name` parameter. Your new test and the disconnect rows call it with the default. Its `[addon-namespace]` row connects a repo named `release` that gets id `release-2`; your `_validate_repos` scope check must not refuse that connect (it names no repo library). Re-run the file after merging.
  - `tests/addons/test_repo_library.py`: item 1 adds a `prepare` column and `a-pending-alias` row to `test_an_id_that_cannot_be_a_namespace_is_refused`.
  - `13.repo-libraries.md`: item 1 edits the `id` sentences near :55; you edit :6/:45/:53 and add a section. `docs/intent/kraft-repo-libraries.md`: item 1 edits `a-repo-id-must-be-free-to-be-a-namespace`; you append two REQs and repoint another. Textual only.
  - After merging: `just test tests/api/test_repos_library.py tests/api/test_repos_workspaces.py tests/addons/test_repo_library.py`.
- **Item 3 (revision `extends` qualified)** changes `AddedTask.extends`/`AddedNode.extends` to `QualifiedIdentifier`, adds `_sources` and a `from ...` part to `render`'s add line, re-parametrizes `tests/addons/test_pins.py::test_a_revision_resolves_against_pinned_addons` (ids `through-a-pinned-addon`, `through-an-addon-not-touched-yet`, `added-node-extends-an-addon`, `added-task-extends-an-addon`, `added-task-extends-an-addon-not-touched-yet`) and adds `test_a_revision_cannot_add_from_an_addon_that_is_not_loaded` (`disabled`, `pinned-version-gone`) and `tests/templates/test_revision.py::test_the_gate_names_what_an_added_node_comes_from`.
  - Task 4 changes `revise`/`render`/`artifact_digest`/`_pinned`/`_added_nodes` signatures in the same file; keep item 3's add line and `_sources` as they are.
  - `repo_id=None` puts only repo libraries out of scope, so item 3's rows (add-ons and local components only) stay valid without passing it (DECISIONS D10). Do not make `repo_id` required on these four functions.
  - Your `_parent` suffix changes the text of item 3's refusals; they match with `extends no (node|task) named` as a search, so they still pass. Your `_pins` rewrite must keep item 3's pin sets: they come from `references(id)` (`nodes.release:stage`, `tasks.release:base`).
  - The direct-form cross row `another-repo-direct` (Task 4) is yours.
  - After merging: `just test tests/addons/test_pins.py tests/templates/test_revision.py tests/api/test_addon_content.py tests/api/test_item_drafts.py --no-testmon`, and `just test-ui` (item 3 changed `AddNodeMenu.tsx`; Task 9 changes other pickers).
- **Item 2 (store reads checked against the digest)**:
  - `addons/load.py` `for_item`: item 2 adds `_launch_problem(addon)` (hashes `.kraft-digest` and `profiles.yaml`) applied to every entry still loading at the end of `for_item`. Your rewrite keeps it and applies it **after** `scoped(...)` and the reservation, so an out-of-scope or reserved entry is never hashed (DECISIONS D13). It also changes `_why_left_out` and moves `gc`'s removal loop to `fetch.remove_tree`; you touch neither.
  - `agent.resolve_agent_task`: your scope stop uses the entry's own `left_out` (Task 5), so an own-repo library with an edited store stops with item 2's `does not match its digest` text. The cross row `own-repo-edited-store` is yours, using item 2's `support.addons.edit_store`.
  - Item 2 reads stores through `fetch.open_store(root)` and `verify_store`, not `read_verified`. `skill.py` is rewritten by item 2 and untouched by you: your launch refusal sits in `resolve_agent_task` before `skill.read`.
  - `support.addons.installed()` now writes `store/<digest>/` with a manifest. Your `test_scoped_leaves_another_repos_library_out` builds `InstalledAddon` values in memory and reads no store, so it is unaffected; anything that reads a store must lay it out through `installed(...)`, `install(...)` or `accept_repo_library(...)`, never write into it afterwards.
  - `addons/repo_library.py` `check`: item 2 replaces `fetch.extract_dir(store)` at `:381` with `fetch.verify_store(store)` and the scratch-write loop at `:399-403` with `fetch.write_scratch`; your Task 7 edits the `was is None` block at `:415-421` inside the same `with tempfile.TemporaryDirectory()`. Keep both of item 2's calls.
  - `13.repo-libraries.md` and `1.security.md`: item 2 edits other paragraphs. Textual only.
  - After merging: `just test tests/addons tests/templates tests/test_skill.py tests/executor/test_dispatch_pins.py --no-testmon`.
