# A chain revision can add a node that extends an add-on's component

## Problem

The add-ons spec (Where the type changes) lists "`extends:` in chain revisions (`revision.py:77-95`)" among the fields that become `QualifiedIdentifier`. On main (f024b41) they are still `Identifier`:

- `AddedTask.extends: Identifier` (`src/kraft/templates/revision.py:78`)
- `AddedNode.extends: Identifier | None` (`revision.py:95`)

So a revision can add only nodes and tasks that extend local library components. `release:stage` is refused by the model before resolution, although the resolver already handles it. `_added_nodes` (`revision.py:387`) resolves against the item's pinned library through `_pinned` (`revision.py:376`). `test_a_revision_resolves_against_pinned_addons` (`tests/addons/test_pins.py:322`) reaches an add-on only through a local library node whose task extends it.

Two doors hit the refusal today:

- **The `revise_chain` agent.** The `kraft:chain-review` skill (`src/kraft/skills/chain-review/SKILL.md:63,138`) tells it to add components that `kraft admin templates library` lists. That listing already includes add-on components (`tasks.release:base (release@acme 1.0.0)`, `cli/templates.py:58-66`). A proposal that follows it fails at parse with a pattern error, and the gate says "Cannot be read".
- **The item draft's add-node menu.** `AddNodeMenu` (`frontend/src/ng/item/draft/AddNodeMenu.tsx`) lists every library node through `ExtendMenu`, add-on nodes included under their qualified name. Picking one pre-fills the node id with `release:stage` (`initial={base}`, :37), which `idError` refuses. A person who renames it gets a 422 from `PUT /work-items/{id}/draft`, because `drafts/item.py:49` (`AddNodeOp.node: revision.AddedNode`) is validated by `item.OPS`.

No MCP tool, CLI verb or JSON schema builds a change set. `vscode/schemas/` has no schema for it, and `mcp.py` has no revise tool: the change set is only the `chain_revision` artifact (`revision.parse`) and the item draft's `add_node` op.

## Behaviour

1. `AddedTask.extends` and `AddedNode.extends` accept `<namespace>:<name>` (`QualifiedIdentifier`, `templates/environment.py:52`). `AddedNode.id`, `AddedStep.id` and `AddedTask.id` stay `Identifier`: a revision still declares only bare ids.
2. The synthetic `chain_revision` chain is a local chain (`_added_nodes` → `with_chain`, no `addon=`, so no `qualify`). A bare `extends` stays local and a qualified one names the add-on's component (`a-bare-local-name-is-local`). No resolver change.
3. The added node resolves against the item's pinned versions (`_pinned`). An add-on the item has not read yet resolves at the lock's version and joins the item's pins (`revise`: `addons = {**added_addons, **addons}`, existing pins win). The pin comes from the reference itself (`nodes.release:stage` in `TemplateLibrary.references`), so it survives the reference-only `_pins` that spec 4 proposes.
4. Whatever an add-on may not be used for elsewhere is refused here too, with the resolver's message. That covers a disabled or otherwise left-out add-on, a pinned version whose store is gone, and a component of the wrong kind (`"... which is a task, not a node"`). The refusal reads `add: chain_revision.yaml: <id>: extends no node named 'release:stage'`. At the gate it is "Cannot be applied"; in an item draft it is a problem on that op.
5. The gate artifact names where each added node comes from. `render`'s change line becomes `` - add `x` after `n`, from `release:stage` -- <evidence> ``. For a `tasks` or `steps` node it lists each task's `extends`, in order and without repeats. A local component shows the same way (`from `extra_check``). The "as it will run" block and `revision.diff` are unchanged. `diff` compares resolved chains, which carry no provenance, and the `chain_revised` event already records the authored `changes`, `extends` included. The item draft's own summary already shows the qualified name (`view.ts:20`, `from the library (release:stage)`).
6. The add-node menu pre-fills the id with the bare part of the base (`release:stage` → `stage`), as the chain editor already does (`NodeView.tsx:152`, `BottomPane.tsx:163`).
7. The chain-review skill tells the agent that an add-on's component is named as the listing prints it, `<namespace>:<name>`, and that the `id` it gives is always bare.
8. **Repo libraries (spec 4).** Nothing here scopes them. Until spec 4 lands, `<repo-id>:x` is reachable from a revision the same way an add-on is, and the same way every other door reaches it today. Spec 4 merges after this item (order 1, 3, 2, 4) and adds `load.scope_problem` in `_added_nodes`, which covers both forms (direct and through a local node); it also adds the direct-form test row.

## Where

- `src/kraft/templates/revision.py`
  - :37 import `QualifiedIdentifier`;
  - :78 and :95 switch `extends` to `QualifiedIdentifier`;
  - the `AddedTask` docstring (:72-73, "a library task by name") and `AddedNode` (:88-89) say "a local or add-on library component";
  - `render` (:462): the change line names the source. A small helper `_sources(node: AddedNode) -> list[str]` gives `node.extends`, or each task's `extends` across `tasks`/`steps`, deduplicated in order.
- `src/kraft/drafts/item.py:49`: nothing to change. It reuses `revision.AddedNode`, and `routes/drafts.py` (`put_item_draft`, `_item_view`, `apply_item_draft`) passes `st.library` to `revise`.
- `src/kraft/api/routes/gates.py` (`_revise`), `executor/gates.py` and `deps.launch` (`artifact_digest`) go through `parse` and `revise`, so nothing changes there. The digest binds the approval to the add-on version shown. If the lock moves an unpinned add-on between render and approval, the existing `StaleRevision` refuses it.
- `frontend/src/ng/item/draft/AddNodeMenu.tsx:37`: `initial={base.split(":").pop()!}`. No other frontend validator restricts `extends` (`types.ts:5` is `extends?: string`).
- `src/kraft/skills/chain-review/SKILL.md`: the `add` bullet (:60-67) and the checklist line (:138).

## Requirement

New in `docs/intent/kraft-addons.md`, after `running-item-keeps-its-addon-versions`:

```
## REQ a-revision-can-add-an-addon-component

WHEN a chain revision or an item draft adds a node, the system SHALL accept `<namespace>:<name>` in the node's and its tasks' `extends`, SHALL resolve it against the add-on versions the item pinned, pinning an add-on it had not read at the lock's version, and SHALL refuse a component of an add-on that is not loaded.
enforced-by: tests/addons/test_pins.py::test_a_revision_resolves_against_pinned_addons[added-node-extends-an-addon], tests/addons/test_pins.py::test_a_revision_resolves_against_pinned_addons[added-task-extends-an-addon], tests/addons/test_pins.py::test_a_revision_resolves_against_pinned_addons[added-task-extends-an-addon-not-touched-yet], tests/addons/test_pins.py::test_a_revision_cannot_add_from_an_addon_that_is_not_loaded[disabled], tests/addons/test_pins.py::test_a_revision_cannot_add_from_an_addon_that_is_not_loaded[pinned-version-gone], tests/api/test_addon_content.py::test_an_item_draft_adds_an_addons_node, tests/templates/test_revision.py::test_anything_but_one_strict_change_set_is_refused[added-node-with-a-qualified-id]
origin: src/kraft/templates/revision.py §AddedNode
```

`running-item-keeps-its-addon-versions` is unchanged. Its existing rows keep their ids.

## Tests

- **`tests/addons/test_pins.py::test_a_revision_resolves_against_pinned_addons`**, re-parametrized on the `AddedNode` the revision adds and the pins expected. The existing ids keep their meaning: the added node extends a local node whose task extends `release:base` or `tools:base`. The local library declares both local nodes. `_release` gains a node `stage` (`{"kind": "exec", "tasks": [{"id": "t", "extends": "base"}]}`). New rows:
  - `added-node-extends-an-addon`: `{"id": "x", "extends": "release:stage"}`, pins `["release"]` at 1.0.0;
  - `added-task-extends-an-addon`: `{"id": "x", "tasks": [{"id": "t", "extends": "release:base"}]}`, pins `["release"]`;
  - `added-task-extends-an-addon-not-touched-yet`: the same with `tools:base`, pins `["release", "tools"]`.

  The existing assertions hold for every row: the 1.0.0 prompt, the pin set, and `release` at 1.0.0.
- **New `test_a_revision_cannot_add_from_an_addon_that_is_not_loaded`** in the same file, with two rows. `disabled`: `tools@acme: false` in `addons.yaml`, added task `tools:base`. `pinned-version-gone`: drop the pinned `release` 1.0.0 store after the lock moved to 1.1.0, added node `release:stage`. Each raises `RevisionError` matching `extends no (node|task) named`.
- **`tests/templates/test_revision.py::test_anything_but_one_strict_change_set_is_refused`** gains `added-node-with-a-qualified-id` (`"id": "release:x"`, match `node\.id`). This pins that ids stay bare.
- **New `tests/templates/test_revision.py::test_the_gate_names_what_an_added_node_comes_from`**, with rows `local-node` (`extra_check`), `addon-node` (`release:stage`) and `addon-tasks` (two tasks extending `release:base` and `check`). It uses a `TemplateLibrary.from_mappings(..., addons=[support.addons.installed(tmp_path, "release", library=...)])`, and asserts the `- add ... from ...` line.
- **New `tests/api/test_addon_content.py::test_an_item_draft_adds_an_addons_node`**: `load_release` with a node `build`, file an item, then `PUT /work-items/{id}/draft` with `add_node` extending `release:build`. It asserts a 200 with no problems and the node in `nodes`. After `POST .../draft/apply`, the stored chain's `addons` names `release`.
- **Frontend** `AddNodeMenu.test.tsx`: "fills the id with the library id" becomes an `it.each` over `security → security` and `release:stage → stage`. The add-on row's library fixture lists `{kind: "nodes", name: "release:stage", ...}`, and the PUT body carries `extends: "release:stage"`.
- **Mutation checks.**
  - Revert the two types to `Identifier`: the three new `test_pins` rows and the API test fail at validation (pydantic `ValidationError`, 422).
  - Make `AddedNode.id` a `QualifiedIdentifier`: the `added-node-with-a-qualified-id` row fails.
  - Drop `if addon.left_out is None` in `TemplateLibrary.with_addons`: `disabled` fails. Its store is still there, so the component resolves.
  - Make `_pinned` return `library` unchanged: `pinned-version-gone` fails, because the node resolves against the lock's 1.1.0. The existing rows' 1.0.0-prompt assertion fails too.
  - Drop the `from ...` part of `render`'s add line: the gate test fails.
  - Revert `AddNodeMenu`'s `initial`: the `release:stage` row fails.

## Docs

- `docsite/content/5.reference/03.configuration/04.library-and-chains.md` §Qualified names (:90): `extends` takes a qualified name, including on a node a chain revision or an item draft adds.
- `docsite/content/5.reference/03.configuration/12.addons.md`:
  - the qualified-reference table (:163), row "A task, step or node": also a chain revision's or an item draft's added node;
  - §What a work item pins (:387): a chain revision may add a node from an add-on, and an add-on the item had not read joins its pins at the lock's version.
- `docsite/content/2.concepts/1.how-a-work-item-runs.md` §Chain revision (:152): "add one built from library components, yours or an installed add-on's"; the gate names the component each added node comes from.
- `docsite/content/5.reference/08.http-api/8.draft-ops.md` §`add_node` on an item draft (:604-608): `extends` may be `<namespace>:<name>`, and `id` is bare.
- `docsite/content/6.project/1.security.md` §Kraft add-ons, "Nothing changes without a review" list (:503-507): a chain revision or item draft can add an installed add-on's component to a running item, only through the revision gate or a person's own draft, and the item then pins that version.
- No web-UI page names the add-node menu (`git grep -i "library node" docsite/content` finds none), so no screen page changes.

## Decisions

- **Ids stay bare, `extends` alone is qualified.** This matches `a-local-declaration-is-bare`, and it keeps canonical paths free of `:`.
- **The gate shows the source on the change line, and `diff` is unchanged.** Resolved nodes carry no provenance. The authored `changes` already reach the `chain_revised` event, and changing `diff` lines would ripple into draft apply payloads for nothing.
- **A refusal reuses the resolver's message** rather than adding a revision-specific add-on check. There is one source of truth, and it is the message intake and lint already print.
- **New REQ in `kraft-addons.md`** rather than rows on `running-item-keeps-its-addon-versions`. That REQ is about skills and profiles at launch. This one is about what a revision may name.
- **Add-on components count as "work an administrator already wrote."** A person accepted the add-on's review at install, and every add still stops at the revision gate or is a person's own draft. The security page says so.
- **No repo-library scoping here.** Spec 4 owns it, at `_added_nodes`. The merge order is fixed (1, 3, 2, 4), so this item lands before item 4, and item 4 adds the direct-form row, `AddedNode(id="x", tasks=[{"id": "t", "extends": "app:base"}])` (a repo library's default `library.yaml` holds a task `base`, no node), alongside its through-a-local-node row (DECISIONS D7).
- **The skill text changes, with no new skill test.** The existing example tests (`tests/skills/test_chain_review.py`) still hold, and a test that pins prose would prove nothing a mutation can break.
- **Release label `release::none`.** Add-ons (#700, 041216a) are in no tag (`git tag --contains 041216a` is empty; the latest is v2.0.0), so this completes unreleased behaviour. If a release ships add-ons first, it becomes `release::minor`.
- **Item 4's `repo_id=None` default does not touch these rows.** None puts every repo library out of scope and leaves add-ons alone, and every row here names only add-ons and local components (DECISIONS D10). Item 4 also appends a left-out reason to the "extends no X named" message, so the refusal rows match with a search, never an anchored regex.
- **The gate test lays its add-on out only through `installed(...)` arguments.** Item 2 (merging after this) turns `installed()` into a digest-checked store, so a file written into `addon.root` afterwards would be refused as edited.
- **`LIBRARY`'s mapping is hoisted to `_LOCAL`** so the gate test can build the same local library with an add-on layer, instead of copying the mapping.
- **The parse-row for a qualified id is written as an `_artifact(...)` text**, because `test_anything_but_one_strict_change_set_is_refused` takes `(text, match)`, not a change dict.
- **A `## Changelog` line under `release::none`; base and removals against the integration branch** (DECISIONS D8, D9).
