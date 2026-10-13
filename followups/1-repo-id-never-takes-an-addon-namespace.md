# A minted repository id never takes an add-on's namespace

## Problem

A repository id and an add-on namespace share one name space (a repo library's namespace *is* its repository id). Hand edits are guarded: `config_check._check_repos` reports "would leave add-on X out" (`api/config_check.py:793-813`, the message at `:808`), and an install or update refuses an add-on whose namespace is a repo id (`addons/update.py:539`, through `load.instance_problem`, `addons/load.py:426-427`). The one function that **mints** an id is not guarded:

- `_repository_id` (`api/routes/repos.py:178-188`) builds the id from the entry's `name` and avoids only the other entries' ids.
- It is called from two doors:
  - **Workspace connect.** `POST /repos` (`_add_repo`, `repos.py:438-527`) on a repo with submodules calls `_declare_workspace` (`repos.py:191-208`), which mints the root's id (`:200`) and each member's (`:205`); `save_repos` at `:527`.
  - **Repo library.** `_check_library` (`repos.py:282-303`) mints the entry's id in memory (`:288`) for both `GET /repos/library` and `POST /repos/library`; the accept saves it at `:328`.
- None of these writes goes through `config_check`, and nothing reloads after a connect.

What goes wrong today:

- **Workspace connect** with a submodule (or root) named `release` writes `id: release`. From then on `load.installed` leaves the installed `release@acme` add-on out (`_why_left_out` → `instance_problem`, `load.py:341`, `:426-427`) and health turns degraded at the next reload. Nothing warned the operator.
- **Repo library** for a repo named `release` mints `release`; `repo_library.check` then refuses it through `_id_problem` (`repo_library.py:206-217`, called at `:358-360`), telling the operator to "set another `id`" for a name Kraft chose itself. The same for a repo named `kraft`.
- `_id_problem` reads only the lock's namespaces (`load.installed`). An `as:` changed in `addons.yaml` and not yet applied by an update (a *pending alias*) is not seen, though `update.py:527-541` already treats it as held.

Doors checked and **not** in scope: `PATCH /repos` (`RepoPatch` has no `id` field); `DELETE /repos`; the Settings draft (`drafts/repos.py`: `add_repo` writes no id, `set_repo` can set one, and its publish runs `config_check.check` on `repos.yaml` like a hand edit, `drafts/config.py:84-107`); `kraft repo connect`, `kraft repo library` and MCP `ensure_repo` (all go through the HTTP routes above); `repo_library.check_all` (reads ids, never mints). `_repository_id` is the only id writer in `src/`.

## Behaviour

1. `_repository_id` never mints an id that is `kraft`, the namespace of an add-on `addons.lock` or `addons.yaml` names (disabled and not-yet-installed ones included), or a namespace a pending alias in `addons.yaml` would take. It skips to the next candidate as it does for a taken repo id: `release` becomes `release-2`, `kraft` becomes `kraft-2`.
2. An id the entry already carries (written by hand, or by an earlier Kraft) is not changed.
   - **Workspace connect:** when a workspace would name an entry whose carried id is one of those, the connect is refused with **422** and writes nothing: `repository id 'release' is the namespace of add-on release@acme; set another `id` on the repository's entry in repos.yaml` (the text `_id_problem` already gives, `repo_library.py:208-215`). In practice this is a member that was connected on its own first and given that id by hand.
   - **Repo library:** unchanged path. `repo_library.check` already refuses such an id (outcome `refused`, the message in `problems`), and `POST /repos/library` then answers 409 and saves nothing. The only change is that a pending alias now counts too.
3. Hand edits keep their current behaviour (`config_check` reports it; doctor reports the add-on through `left_out`). No change there.

## Where

- `src/kraft/addons/repo_library.py`:
  - New `held_namespaces(config_dir, addons_root) -> dict[str, str]`: namespace to the add-on id holding it. Built from `load.installed(config_dir, addons_root)` (each entry with `repo_id is None` contributes its `namespace`, which is the lock's), then every `AddonsConfig.load(config_dir / "addons.yaml")` entry's `config.namespace(addon_id)` (its pending alias), `setdefault` so the lock's holder wins. A broken `addons.yaml` contributes nothing (`config_check` says why), as `load._installed` does.
  - New `namespace_problem(repo_id, held) -> str | None`: the `kraft` and add-on-namespace halves of `_id_problem`, same messages.
  - `_id_problem(repo_id, held)` becomes `namespace_problem(...)` or the >64-characters rule. `check` passes `held_namespaces(config_dir, addons_root)` in place of the `loaded` list. One copy of the rule.
- `src/kraft/api/routes/repos.py`:
  - `_repository_id(entry, repos, held)`: a candidate is skipped when it is taken *or* `repo_library.namespace_problem(candidate, held)` is not None. A carried id is returned as is.
  - `_declare_workspace(workspaces, repos, root, children, held)`: after each `_repository_id` call, `if why := repo_library.namespace_problem(id, held): raise HTTPException(422, why)`. Only a carried id can trip it.
  - `_add_repo`: `held = repo_library.held_namespaces(st.templates_dir, st.run_dirs.addons)`, computed in the sync stretch before `_editable_repos` (no `await` between it and the save), passed to `_declare_workspace`.
  - `_check_library`: the same `held`, passed to `_repository_id`.
- Doctor, `config_check`, `update.py` and `load.py`: no change.

## Requirements

New in `docs/intent/kraft-addons.md` (supersedes the spec-only REQ `a-repository-id-cannot-take-a-plugin-namespace`, which never landed), split in two because EARS takes one behaviour per sentence:

```
## REQ a-minted-repository-id-skips-addon-namespaces

WHEN Kraft writes a repository id for an entry that has none, the system SHALL NOT choose `kraft`, the namespace of an add-on `addons.yaml` or `addons.lock` names, or a namespace an `as:` in `addons.yaml` would take.
enforced-by: tests/api/test_repos_workspaces.py::test_connecting_a_workspace_declares_it_with_its_submodules_as_members[addon-namespace], tests/api/test_repos_workspaces.py::test_connecting_a_workspace_declares_it_with_its_submodules_as_members[reserved], tests/api/test_repos_library.py::test_a_repo_library_is_reviewed_then_accepted[addon-namespace], tests/api/test_repos_library.py::test_a_repo_library_is_reviewed_then_accepted[reserved]
origin: src/kraft/api/routes/repos.py §_repository_id

## REQ a-workspace-never-names-an-addon-namespace-id

IF connecting a repository would declare a workspace naming an entry whose `id` is `kraft` or an add-on's namespace, THEN the system SHALL refuse the connect, name the add-on, and write nothing.
enforced-by: tests/api/test_repos_workspaces.py::test_a_member_whose_id_is_an_addon_namespace_refuses_the_connect
origin: src/kraft/api/routes/repos.py §_declare_workspace
```

Changed in `docs/intent/kraft-repo-libraries.md`: `a-repo-id-must-be-free-to-be-a-namespace` (:33) reads "an add-on's namespace, or one a pending `as:` would take," and gains `tests/addons/test_repo_library.py::test_an_id_that_cannot_be_a_namespace_is_refused[a-pending-alias]`.

Repointed: `docs/intent/templates-v1.md:1385` pins `test_connecting_a_workspace_declares_it_with_its_submodules_as_members`, which becomes parametrized. Repoint it to `[own-name]` (`just intent-repoint`).

## Tests

A fix adds rows where a test already covers the door:

- `tests/api/test_repos_workspaces.py::test_connecting_a_workspace_declares_it_with_its_submodules_as_members`: parametrize over the submodule path and what is installed. `[own-name]` is `libs/a` → `a` (today's case). `[addon-namespace]` is `libs/release` with `release@acme` installed (`support.addons.load_release`) → `release-2`, and `release@acme` still has `left_out is None` in `load.installed(templates_dir, st.run_dirs.addons)`. `[reserved]` is `libs/kraft` → `kraft-2`.
- `tests/api/test_repos_library.py::test_a_repo_library_is_reviewed_then_accepted`: parametrize over the repo's name. `[own-name]` is `app` → `app`; `[addon-namespace]` is `release` with `release@acme` loaded → `release-2`; `[reserved]` is `kraft` → `kraft-2`. `_with_library` takes `name`.
- `tests/addons/test_repo_library.py::test_an_id_that_cannot_be_a_namespace_is_refused`: a row `[a-pending-alias]`. `release@acme` is installed, then `addons.yaml` gives it `as: rel` (`support.addons.edit_addons_yaml`) with no update, and repo id `rel` is refused naming `add-on release@acme`.
- New behaviour, new test: `tests/api/test_repos_workspaces.py::test_a_member_whose_id_is_an_addon_namespace_refuses_the_connect`. The member `pkg` is connected alone, `release@acme` is loaded, and then the member is given `id: release` in `repos.yaml` by hand (in that order: an install refuses an add-on whose namespace is already a repository id). Connecting the root then answers 422 naming `add-on release@acme`, and `repos.yaml` is unchanged.

Fixtures that exist: `support.addons.load_release(client, tmp_path)` (installs and loads `release@acme` into the test server), `repo_with_library(tmp_path, name)`, `make_collection`, `install`, `edit_addons_yaml`; `support.harness.make_repo_with_submodule(tmp_path, submodule_path=...)` (root `ws`, submodule repo `pkg`); `tests/addons/test_repo_library.py`'s `app` and `home` fixtures.

## Docs

- `docsite/content/5.reference/03.configuration/02.repos/index.md:52` (the `id` row): an id Kraft writes is never `kraft` or an add-on's namespace (`release` becomes `release-2`). Keep the cell at 40 words or fewer.
- `docsite/content/5.reference/03.configuration/13.repo-libraries.md:55`: "Accepting writes an `id` when the entry has none" gains: made from its name, skipping one that is taken, `kraft`, or an add-on's namespace. The refusal sentence also covers a pending `as:`.
- `docsite/content/5.reference/03.configuration/02.repos/3.workspaces.md` (near :44, the connected-member paragraph): a member whose `id` is already an add-on's namespace refuses the connect until you set another `id`.

## Release

`release::none`. Add-ons (#700) and repo libraries (#726, #727) both postdate the latest tag, v2.0.0. No released Kraft can hit the collision, so this fix ships with the release that first ships add-ons. `## Changelog` carries the line below anyway, for the batch's final PR to collect (DECISIONS D6, D9). If a release goes out first, it becomes `release::patch` with the line "Connecting a repo with submodules, or taking a repo library, no longer gives a repository an add-on's namespace as its id."

## Decisions

- **422, not 409, for the workspace-connect refusal.** `client.ensure_repo` (`client/actions.py:172`) reads any 409 from `POST /repos` as "already connected" and returns success, so a 409 would be swallowed by `kraft repo connect` and MCP `ensure_repo`. 422 is what `_validate_repos` already uses for a `repos.yaml` the loader would refuse.
- **The repo-library door gets no new refusal.** `repo_library.check` already refuses a carried colliding id with `_id_problem`'s message, and `POST` saves nothing unless the outcome is `waiting`. Adding a second refusal would be a second copy of the rule.
- **The 409 text of `POST /repos/library` ("not the one you reviewed") is left alone.** `kraft repo library` posts only a `waiting` candidate, and its GET already shows the real reason. Out of scope.
- **Shared rule split as `namespace_problem` + `_id_problem`.** Using `_id_problem` whole as the mint's skip test would loop forever on a name longer than 64 characters (every suffixed candidate is still too long). It would also make a workspace connect refuse long ids it accepts today.
- **Minted ids are not truncated to 64 characters.** That is an existing, separate limit, which the repo-library check reports. Out of scope.
- **Disabled and not-yet-installed add-ons hold their namespace.** `load.installed` lists them, and re-enabling or installing one would otherwise collide. This matches `_id_problem`, which never filtered on `left_out`.
- **Pending alias = `AddonsConfig.namespace(id)` for every `addons.yaml` entry**, the same set `update.py:527-541` treats as held.
- **The helpers live in `repo_library`, not `load`.** `routes/repos.py` already imports `repo_library`, and `_id_problem` lives there. Sibling spec 4 adds connected repo ids as reserved namespaces on the plugin side (`skill.py`). It does not touch this set, so the two compose.
- **Rows, not functions,** for the mint (the existing door tests assert the minted id). A new function only for the refusal, which is a new behaviour.
- **Refusal test: install first, hand-edit the id second.** `update.update` refuses an add-on whose namespace is already a repository id (`load.instance_problem`, `load.py:426-427`); the plan had the order reversed, so `load_release` would never have installed `release@acme`.
- **A `## Changelog` line under `release::none`.** DECISIONS D9: the final PR to main collects the children's lines, so an empty section would drop this one.
- **Base and removals against the integration branch.** The PR targets `ccr-143df22f-uetbpy` (D1), so `check_removals` compares against `origin/ccr-143df22f-uetbpy`, not `origin/main` (D8).
- **No cross-item row is owed by this item.** It merges first; item 4's reserved repo ids and this item's held add-on namespaces are separate sets, and item 4 (merging last) owns any row that needs both (D7).
