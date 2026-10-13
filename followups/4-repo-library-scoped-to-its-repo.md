# A repo library is visible only to its own repository's items

## Problem

A connected repository's `.kraft/` library loads as `library@repo:<id>` under the namespace `<id>:` (`addons/load.py:277-307`, `_repo_libraries`). It goes into the one instance-wide library (`TemplateLibrary._add_addon`, `templates/library.py:380-415`), so today any configuration can name it:

- another repository's `default_chain` or `steering` (`POST`/`PATCH /api/repos` check neither against scope: `routes/repos.py:233-253`, `_validate_repos`; the Settings draft only checks the chain exists, `drafts/repos.py:219-227`; `tests/api/test_repos_library.py:89-97` files `default_chain: app:ship` on another repo as its setup);
- an intake for another repo, through every intake door: `POST /work-items` (`routes/work_items.py:335`), duplicate (`:652-654`), `POST /triggers` (`:780`), all via `deps.intake_chain_or_422` (`api/deps.py:716-722`); auto-intake (`intake.py:157`, which takes the entry's `default_chain`); a cron schedule or `policy.yaml` trigger (`triggers.py:96`);
- the PATCH chain switch (`routes/work_items.py:1109`, used by `kraft item set-chain` and the MCP `set_chain`);
- `PUT /intake` and `PUT /policy` (`routes/settings.py:604`, `:489`), which validate only the model;
- the operator's own `library.yaml` and `chains/`;
- `harnesses.yaml` fallbacks;
- revisions (`templates/revision.py:376-403`, `_pinned`, `_added_nodes`).

At launch, every unpinned repo library's skills and agent profiles are visible to every item (`load.for_item`, `load.py:431-463`, used by `adapters/agent.py:361-389` and `adapters/profiles.py:47`). The add-ons spec intended the opposite: "its plugins visible only to items in that repository". A repository's library is the repository's own business: what one repo's maintainers put in `.kraft/` must not reach another repo's items, and the instance's own config must not quietly depend on one repo.

`TemplateLibrary._pins` (`library.py:712-731`) also pins any add-on whose `<ns>:` appears anywhere in `json.dumps` of the resolved chain, prompt prose included. A scope check over pins would then refuse a chain whose prompt says `app: ...`.

## Rule

`<repo-id>:x` resolves only for:

- a work item whose repository is `<repo-id>`. For a workspace item, that is the root repository: `chain_template_for` already asks the root (`deps.py:643-651`), and `row.repo` and `body.repo` are the root's path.
- that repository's own `repos.yaml` entry (`default_chain`, `steering`, anything nested under it);
- an `intake.yaml` schedule or `policy.yaml` trigger whose `repo` path is that repository's.

Everywhere else it is refused with one message, built in one place: `<x> is in <repo-id>'s repo library, visible only to items in <repo-id>`. That covers local `library.yaml` and `chains/`, `harnesses.yaml`, other repositories' entries, add-ons, other repo libraries, and drafts.

Add-ons are unchanged and stay instance-wide.

## Choices

1. **Workspaces:** the root's library only. A member's library is not reachable from a workspace item's chain, skills or profiles. A member entry's own `steering:` may still name its own library (it is that entry's configuration, frozen as text at intake by `deps.repository_steering`).
2. **Instance config naming a repo library:** refuse. An instance-wide chain must not silently become repo-only. Refused at every save door; a hand edit is reported (below), not enforced in the resolver.
3. **Copying from a repo library** (`new_chain(from=X:c)`, `copy_component`, `drafts/ops.py:737,978`): refuse. The 409 and `read_only_message` (`templates/catalogue.py:72-77`) say "edit it in that repository's `.kraft/`", not "extend it or copy it to your library".
4. **Templates UI:** keep listing repo-library chains read-only, badged with their repository. The intake pickers (Composer, DraftItemPage, phone NewItem, FirstRun) show only the chosen repo's, filtered client-side from `addon.id` the way the VS Code extension already does (`vscode/src/core/fileWork.ts:81`, `chainsFor`). No new `?repo=` parameter.
5. **Items already filed** with another repo's library pinned: finish on their pins. The configuration that named it is reported invalid by `config_check`, `kraft admin templates lint` and doctor until fixed.
6. **A connected repo id is a reserved namespace from connect onward,** even before its library is accepted. `<id>:skill` is then never handed to the agent as another tool's plugin, so accepting a library never silently captures it. A first accept refuses, naming each reference, when instance config names the id from outside its scope, or an installed add-on's skill names it (`update.referrers`). Today a first accept only lists config references as Reach lines (`repo_library.py:415-421`) and never asks `referrers`.

## Where

### 1. The scope primitive (`addons/load.py`, a leaf module)

- `scope_message(name, repo_id) -> str`: the one message.
- `out_of_scope(name, owner, repo_ids) -> str | None`: `name`'s qualifier is in `repo_ids` and is not `owner`.
- `scope_problem(pins, repo_id) -> str | None`: a pin whose id is `library@repo:Y` with `Y != repo_id`. `repo_id=None` (no repository, or an entry with no `id`) refuses every repo library.

### 2. `_pins` reads references, not prose (`templates/library.py:712-731`)

Pin from: the chain id; `references(id)` (`<section>.<ns>:<name>`); every `skill`, `profile` (task and `fallback:` entries) and `steering` value in the dumped chain; `_fallback_profiles`. Compare qualifiers exactly; drop the `json.dumps` regex. Nothing else reads it: `deps.resolve_chain_or_422`'s regex runs over the error text and is unchanged.

### 3. Item resolution (intake, switch, revision)

- `deps.scoped_chain_or_422(st, entry, name)`: `resolve_chain_or_422` then `scope_problem(chain.addons, entry.id)` as a 422 `chain {name!r}: ...`. `intake_chain_or_422` calls it, so `POST /work-items`, duplicate and `POST /triggers` are covered; duplicate's `chain_template is None` branch uses it too.
- PATCH chain switch (`work_items.py:1109`): the same, with `connected_or_422(st, row["repo"])`.
- Auto-intake (`intake.py:157`) and cron (`triggers.py:96`): `scope_problem` after `resolve_chain`; log and skip, as any refused intake. `triggers.py` checks `connected_or_422` before resolving, to know the id.
- `deps.repository_steering` (`deps.py:999-1021`): a steering name outside its entry's scope raises `SteeringError` (every intake door already turns that into 422 or a logged skip).
- Revision: `revise`, `render`, `artifact_digest` and `drafts/item.evaluate` take `repo_id: str | None = None` (None: no repository, so no repo library; add-ons are never scoped). `_pinned` always scopes the library it resolves against (`library.with_addons(load.scoped(...))`, no disk read when nothing is pinned), and `_added_nodes` runs `scope_problem(resolved.addons, repo_id)`. Callers pass the item's id: `gates.py:129`, `artifacts.py:401,504`, `deps.launch`'s `chain_revision_digest` partial (`deps.py:1047`), `routes/drafts.py:468,536`.
- `TemplateLibrary`'s "extends no X named 'Y:n'" (`library.py:1037-1041`) appends the left-out add-on's reason when `Y` is known but left out, so a scoped-out `extends` says why.

### 4. Launch (`addons/load.py:431-463`, `adapters/agent.py:282-389`)

- `load.scoped(addons, repo_id, keep=())`: each repo library that is not `repo_id`'s and not in `keep` comes back with `left_out=scope_message(...)` and `quiet=True`. Never omitted: a namespace missing from `addon_dirs` is treated as another tool's plugin and gets `PLUGIN_PROMPT` (`skill.py:43,120-123,167-169`); a None entry refuses it.
- `for_item(pins, config_dir, addons_root, *, repo_id)`: the live add-ons through `scoped`, plus one left-out, quiet entry for each connected repo id that has no loaded library (the reservation, Choice 6). Pinned namespaces are kept as today (Choice 5). `repo_id` is required, so every caller decides.
- `harness_table(harnesses, pins=None, repo_id=None)` (`adapters/profiles.py:36-52`) passes it on.
- `resolve_agent_task(..., repo_id=None)`: before reading anything, a task that reads (`_reads_namespace`) an unpinned, scoped-out namespace stops with the scope message: `SkillError` for its skill, `ProfileUnavailable` for a profile or fallback. Both are config stops naming the task path (`dispatch.py:1336-1351`). `skill.py` is not changed.
- `LaunchContext.item_repo_id` (`executor/context.py:133`), set by `deps.launch` from the root entry (every caller passes `row["repo"]`) and kept by `_fan_out`'s `replace`. Dispatch (`dispatch.py:1301,1316`), gate review (`gate_review.py:100,279`), escalation (`escalate.py:532`) and review reply (`review_reply.py:148`) pass `repo_id=launch.item_repo_id`; sessions (`sessions.py:163`) likewise.
- Previews: the steering preview (`settings.py:205-245`) refuses (422) a chain out of the previewed repo's scope, then passes `addons=resolved.addons` and `repo_id=entry.id`. Doctor's cost rows (`doctor.py:773-819`) preview each chain on its own pins (`addons=chain.addons`), build the harness table per chain, and also catch `SkillError`.

### 5. Config files: one static rule

`update.scoped_references(config_dir, repos=None, *, replacing=None)` yields `references()`' four fields plus the owner: a `repos.yaml` entry's `id` for everything under that entry; the `id` of the entry whose path a `schedules[i]` or `triggers[i]` names (path match as `deps._connected`, moved to `config.connected_entry` so both use one rule); None elsewhere. `references()` keeps its signature (five callers). `replacing` maps a file to its unsaved data.

`update.scope_problems(config_dir, ...)`: each reference whose qualifier is a connected repo id (Choice 6) and is not its owner. Called from:

- `config_check`: `_check_chain`, `_check_library`, `_check_repos`, `_check_intake`, `_check_harnesses`, `_check_policy`, each over its candidate file. This covers Settings drafts, `PUT /templates/library|chains`, the VS Code `/check` route and `apply`'s hand-edit report.
- `routes/repos.py` `_validate_repos` (`POST`/`PATCH /api/repos`).
- `PUT /intake`, `PUT /policy` (triggers).
- `drafts/repos.py:219-227` and `drafts/intake.py` `_schedule_problems`: per entry and per schedule, the file-level duplicate filtered as `_SCHEDULE_CRON` already is.
- `config_check.lint_report` (`kraft admin templates lint`, `GET /templates/lint`, and `update.state_of`, where the issues are the same before and after a change and so add no `breaks` line).
- doctor's `repo libraries` row (`doctor.py:618`), which fails listing each.
- First accept (`repo_library.check`, `was is None`): an out-of-scope reference to `repo_id`, or `update.referrers(repo_id, loaded add-ons)`, refuses with each named. References in scope stay Reach lines. Later changes are not refused for someone else's invalid config.

Reserved ids also join `other_namespaces` where an add-on or repo library is checked (`update.py:541-545`, `repo_library.py:358`), so new content cannot name them as a plugin.

The disconnect check (`routes/repos.py:653-672`) is unchanged: it lists every reference, valid or not.

## Requirements

New in `docs/intent/kraft-repo-libraries.md`:

```
## REQ a-repo-library-is-visible-only-to-its-repository
The system SHALL resolve `<repo-id>:<name>` only for a work item whose repository (a workspace's root) is `<repo-id>`, for that repository's own `repos.yaml` entry, and for a schedule or trigger whose `repo` is that repository, and SHALL refuse it everywhere else, naming the repository.

## REQ a-repo-id-is-never-another-tools-plugin
WHILE a repository is connected, the system SHALL NOT hand `<repo-id>:<skill>` to the agent as another tool's plugin, whether or not its library is accepted.
```

Each gets `enforced-by:` rows from the tests below and an `origin:` (`src/kraft/addons/load.py §scope_problem`, `src/kraft/addons/load.py §for_item`).

Unchanged in text: `a-named-repo-library-holds-its-repo` (:69) still holds (a hand-written reference and the repo's own schedule both hold a disconnect); its pin moves to the reworked rows. `a-change-of-shape-waits-for-a-person` (:87) keeps `test_a_local_chain_that_changes_shape_through_the_library_holds` (`tests/addons/test_repo_library.py:498`): its local chain is now an invalid hand edit, and an unattended update is still held for it.

## Tests

- `tests/api/test_repos_library.py:89-97` changes setup: another repo's `default_chain: app:ship` is now refused by `POST /api/repos` (a new row of its own). The disconnect test is parametrized: `its-own-schedule` (an `intake.yaml` schedule for `app`) and `a-hand-edit` (another entry's `default_chain` written to `repos.yaml` on disk).
- One door table, one row each: intake for another repo, duplicate, `POST /triggers`, auto-intake, PATCH switch, schedule and trigger for another repo, `PUT /intake`, `PATCH /api/repos` default_chain and steering, local `library.yaml` extends, local chain, `harnesses.yaml` fallback, draft copy, revision adding another repo's node, launch (a skill from another repo's library is refused, not delegated), a reserved id with no library (refused at launch, not delegated).
- Positive rows: the repo's own item, its own default chain, its own schedule, an item already filed on another repo's pin still launching.
- A workspace item reads its root's library and not a member's.
- `_pins` does not pin on `X:` in prompt text.
- First accept refused while a local chain or an add-on's skill names the id.
- Use `tests/support/addons.py` (`repo_with_library`, `accept_repo_library`, `repo_library_files`) and the repo-library fixtures in `tests/addons/test_repo_library.py`.

## Docs

- `docsite/content/5.reference/03.configuration/13.repo-libraries.md`: :6, :45, :53, :71, :154, :195 now say the content is visible only to that repository; a new "Who can name it" section with the rule and the message.
- `5.reference/07.triggers.md:30`: a schedule's `chain` may name a repo library only when `repo` is that repository.
- `5.reference/01.cli/4.repo.md:80`, `2.concepts/4.vocabulary.md:225-232`, `6.project/1.security.md:529-556`, `3.guides/2.customize/4.share-chains-with-addons.md`: state the scope.
- `4.troubleshooting/4.doctor-failures.md`: the `repo libraries` row's new failure. `4.troubleshooting/1.why-did-my-item-stop.md`: the launch stop.

Label: `release::none`. Repo libraries (#726, #727) are in no release yet (the latest tag, v2.0.0, predates them), so this tightens unreleased behaviour and rides with the release that ships them. If a release goes out first, it becomes `release::minor` and the changelog says which configurations now fail and how to fix them.

## Decisions

- **Static rule, not a resolver rule, for instance config.** Refusing in `resolve_chain` would break revisions (their pseudo-chain is local), blame chains for a `harnesses.yaml` fallback, and flip `breaks`/`_holds` in accept. The static rule names the file and key, and every save door already runs `config_check`.
- **A local chain naming a repo library still resolves for that repo's own items** (no scope breach of the item); it is reported invalid everywhere and refused at every save. Choice 2 is about config, not about the item.
- **Added doors the draft missed:** auto-intake (`intake.py:157`), duplicate, `POST /triggers`, `POST`/`PATCH /api/repos` (`_validate_repos`, not `config_check`), `PUT /intake`, `PUT /policy`, `drafts/intake._schedule_problems`, the steering preview, doctor's cost rows, `harness_table`, and the FirstRun default-chain picker. `dispatch.restore_pins` needs nothing (it reads pinned stores only). MCP `create_work_item`/`set_chain`, `kraft item create|set-chain` and the VS Code extension go through those HTTP doors.
- **`config.schedule_refusals` is not a call site:** it is a pure `Schedule` model check with no `repos.yaml`; doctor and `admin` use it for the 2.0 move. The rule goes in `_check_intake`/`_check_policy` and the drafts instead.
- **`deps.repository_steering` checks names against each entry's own id**, so a workspace member's own steering still freezes (Choice 1 keeps chains, skills and profiles to the root).
- **`references()` is not widened;** a sibling `scoped_references` adds the owner, so its five callers stay as they are.
- **`for_item(..., repo_id)` is required, and None means "no repository"** (fail closed): an unscoped default would silently keep today's leak in any caller that forgot.
- **Revision threads `repo_id`** (`repo_id: str | None = None` on `revise`, `render`, `artifact_digest`, `drafts.item.evaluate`): the snapshot's target id is the constant `"target"` for a single repo (`executor/entry.py:58-70`), so the id cannot be read from the chain. None means "no repository": every repo library is out of scope and add-ons are untouched. That, not the default as such, is why item 3's rows (add-ons and local components only) stay valid without passing it. Every production caller passes the item's id, and a route-level row (`draft-adds-own`) fails if one forgets (DECISIONS D10).
- **Launch refusal lives in `resolve_agent_task`, not `skill.py`:** `addon_dirs` carries no reason, and spec 2 rewrites `skill._addon_path`. `SkillError`/`ProfileUnavailable` give a `{task.path}: ...` config stop instead of "selects harness ... not available".
- **Choice 4 changed:** no `?repo=` query. The extension already filters on `addon.id`; a server filter would be a second rule for a picker convenience the intake doors enforce anyway.
- **Choice 6 sharpened:** the draft said accept "does not run referrers" and cited `repo_library.py:358-370`. Accept already lists config references as Reach (`:415-421`); what is new is refusing out-of-scope ones and asking `referrers` for add-on skills. Only a first accept refuses: blocking every later update over another file's invalid reference punishes the wrong repository.
- **The `_pins` tightening is safe:** `_pins` is the only reader of `json.dumps(data)`. A `model:` or prompt containing `x:` stops pinning a same-named add-on. Nothing launches from prose, and `gc` keeps what is pinned.
- **Intent texts kept** for `a-named-repo-library-holds-its-repo` and `a-change-of-shape-waits-for-a-person`. Both stay true; only their tests' setups change. The draft's instruction to rework the test at `:498` around the repo's own `default_chain` is dropped: that chain is already the library's own and covered by `[a-node-added]`.
- **Citations corrected:** `load.py:277-307` (was 280), `for_item` `:431`, `_add_addon` `library.py:380-415`, `chain_template_for` `deps.py:643-651` (the root note is in its docstring), disconnect `repos.py:653-672`.
- **`for_item` required vs. revision defaulted, and why they differ.** Both read None as "no repository" and fail closed for repo libraries only. `for_item` has four production callers and is where launch reads, so a required keyword makes each decide; the four revision functions have about twenty test call sites that name only add-ons, so a default costs nothing in safety and the route-level row catches a production caller that forgets (DECISIONS D10).
- **Launch stop text is the entry's own `left_out`**, never a rebuilt scope message: after item 2, an own-repo library with an edited store is left out with item 2's digest message, which must not read as a scope breach (DECISIONS D13). Item 4 adds the `own-repo-edited-store` row (D7).
- **Cross-item rows are this item's** (it merges last; DECISIONS D7): the revision adding another repo's component directly (`another-repo-direct`, needs item 3's `QualifiedIdentifier`) and the edited own-repo store (`own-repo-edited-store`, needs item 2). A repo library's default `library.yaml` holds the task `base` and no node, so the direct form is `tasks: [{extends: app:base}]`; `AddedNode(extends="app:base")` would be refused as "a task, not a node".
- **Test placement for the line budget** (DECISIONS D11): the install-side row goes to a new `tests/addons/test_update_repo_ids.py` (`test_update.py` is at 794 and item 2 takes it to 797); `LaunchContext.item_repo_id` rows go to `tests/api/test_deps_repo_library.py` (`test_deps.py` is at 800); nothing goes to `tests/executor/test_dispatch.py` or `tests/adapters/test_agent.py` (allowlisted, at their ceilings). The draft tests are `tests/drafts/test_repos.py` and `tests/drafts/test_intake.py` (the plan had named `tests/api/test_drafts.py`).
- **The disconnect pin is repointed in the task that parametrizes it** (Task 6), not in the docs task: `just intent` fails from the moment the bare id stops collecting.
- **Item 2's reader is `fetch.open_store`/`verify_store`**, and item 2 also changes `load.for_item` (`_launch_problem`), not only `_why_left_out`; the plan's rebase notes said `read_verified` and missed `for_item`. Fixed in the plan's Coordination section.
- **A `## Changelog` line under `release::none`; base and removals against the integration branch** (DECISIONS D8, D9).
