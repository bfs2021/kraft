# Plan: a chain revision can add a node that extends an add-on's component

Spec: `3-revision-extends-qualified.md` (read its **Decisions** first). Base: the integration branch `ccr-143df22f-uetbpy` (main f024b41 today). This item merges **second** of four (order 1, 3, 2, 4); item 1 may land before you. See **Coordination** at the end.

### Task 0: Set up

```bash
git fetch origin
git switch ccr-143df22f-uetbpy-3-revision-extends 2>/dev/null || git switch -c ccr-143df22f-uetbpy-3-revision-extends origin/ccr-143df22f-uetbpy
uv tool install rust-just   # just is not preinstalled
just setup                  # uv sync + npm ci (Task 6 needs the frontend)
```

Read `CLAUDE.md`, `docs/testing.md` and CONTRIBUTING's "Removed tests" and "Pull requests and release labels". If your session was given another branch name, use it; it must start from `origin/ccr-143df22f-uetbpy`.

Ground rules:
- Go through `just test` (never raw pytest): `just test <file> -k '<expr>'`.
- Tests come first in every task: write the rows, watch them fail for the stated reason, then change the code.
- Every new pin gets the mutation the spec names. Apply it, run that one case (`just test <file> -k '<test> and <id>'`), confirm it fails, revert it, and note it in the commit message and the PR's mutation table.
- Before each commit: `just lint` and `just check-tests`. Commit at the end of each task.
- Line budget (`dev/check_tests.py`, 800 per test file): `tests/addons/test_pins.py` is at 344 and items 2 and 4 grow it too (DECISIONS D11): keep your growth near +45. `tests/templates/test_revision.py` (559) and `tests/api/test_addon_content.py` (206) have room.

### Task 1: Rows that need a qualified `extends` (test_pins), red first

Files: `tests/addons/test_pins.py`.

1. Add a node to `_release`'s library: `"nodes": {"stage": {"kind": "exec", "tasks": [{"id": "t", "extends": "base"}]}}`. The add-on's bare `base` is qualified on load (`addons.load.qualify`).
2. Re-parametrize `test_a_revision_resolves_against_pinned_addons` on `(added, pinned)`. `added` is the `AddedNode` kwargs.
   - The local `library.yaml` declares two nodes: `via_release` (task extends `release:base`) and `via_tools` (task extends `tools:base`).
   - **Keep the two existing ids, with the same meaning**: `through-a-pinned-addon` is `{"id": "x", "extends": "via_release"}` with `["release"]`, and `through-an-addon-not-touched-yet` is `{"id": "x", "extends": "via_tools"}` with `["release", "tools"]`. `docs/intent/kraft-addons.md:270` pins both ids.
   - New rows:
     - `added-node-extends-an-addon`: `{"id": "x", "extends": "release:stage"}` with `["release"]`;
     - `added-task-extends-an-addon`: `{"id": "x", "tasks": [{"id": "t", "extends": "release:base"}]}` with `["release"]`;
     - `added-task-extends-an-addon-not-touched-yet`: the same with `tools:base`, giving `["release", "tools"]`.
   - Build the node with `AddedNode.model_validate(added)`. The body and assertions are unchanged: `nodes[1].tasks[0].prompt == AGENT["prompt"]` (1.1.0's `base` prompt differs), the sorted pins, and `release` at `1.0.0`.
3. New `test_a_revision_cannot_add_from_an_addon_that_is_not_loaded`, parametrized on `ids=["disabled", "pinned-version-gone"]`:
   - `disabled`: `edit_addons_yaml(config_dir, ...)` sets `tools@acme` to `false`. Add `{"id": "x", "tasks": [{"id": "t", "extends": "tools:base"}]}`.
   - `pinned-version-gone`: publish 1.1.0, `_update`, then `drop_store(<1.0.0 root>)`. This is the pattern of `test_a_launch_restores_the_pinned_store_it_needs`. Add `{"id": "x", "extends": "release:stage"}`.
   - Both rows: the snapshot is `mine` (pins `release`), `live = TemplateLibrary.from_yaml_dir(config_dir, addons=load.installed(...))`, and `pytest.raises(RevisionError, match=r"extends no (node|task) named")`.
   - Add a one-line docstring: refused with the resolver's message, never resolved against another version.
4. Run `just test tests/addons/test_pins.py -k revision`. The three new success rows fail with a pydantic `ValidationError` (string pattern). The refusal rows fail at the same place, which is expected before task 2. The two old rows pass.

### Task 2: Switch `extends` to `QualifiedIdentifier`

Files: `src/kraft/templates/revision.py`.

1. Import `QualifiedIdentifier` beside `Identifier` (:37).
2. `AddedTask.extends: QualifiedIdentifier` (:78) and `AddedNode.extends: QualifiedIdentifier | None = None` (:95). The `id` fields stay `Identifier`.
3. Docstrings:
   - `AddedTask` (:72-73): "a library task by name, local or an add-on's (`<namespace>:<name>`), and nothing else, so a revision can only run work an administrator wrote or accepted".
   - `AddedNode` (:88-89): likewise.
4. `just test tests/addons/test_pins.py -k revision`: everything is green.
5. Mutations:
   - Revert (2): the three new rows fail.
   - Drop `if addon.left_out is None` in `TemplateLibrary.with_addons` (`templates/library.py:445`): `disabled` fails.
   - `_pinned` returns `library`: `pinned-version-gone` and the old rows fail.
   - Revert each mutation.

### Task 3: Ids stay bare, pinned at parse

Files: `tests/templates/test_revision.py`.

1. Add a row to `test_anything_but_one_strict_change_set_is_refused` (its parameters are `(text, match)`, with the ids in a separate `ids=[...]` list): text `_artifact({"rationale": "ok", "add": [{"after": "build", "evidence": "e", "node": {"id": "release:x", "extends": "release:stage"}}]})`, match `r"node\.id"`, and append `"added-node-with-a-qualified-id"` to `ids`. It passes as soon as it is written: it pins the bare-id half of the decision.
2. Mutation: `AddedNode.id: QualifiedIdentifier` makes the row fail. Revert.
3. `just test tests/templates/test_revision.py`.

### Task 4: The gate names what an added node comes from

Files: `tests/templates/test_revision.py`, `src/kraft/templates/revision.py`.

1. Test first: new `test_the_gate_names_what_an_added_node_comes_from(tmp_path, node, source)`.
   - Rows:
     - `local-node`: `{"id": "x", "extends": "extra_check"}` gives `` `extra_check` ``;
     - `addon-node`: `{"id": "x", "extends": "release:stage"}` gives `` `release:stage` ``;
     - `addon-tasks`: `{"id": "x", "tasks": [{"id": "a", "extends": "release:base"}, {"id": "b", "extends": "check"}, {"id": "c", "extends": "release:base"}]}` gives `` `release:base`, `check` ``.
   - The library: hoist the mapping `LIBRARY` is built from into a module constant `_LOCAL = {...}` and build `LIBRARY = TemplateLibrary.from_mappings(_LOCAL, (), library_path=Path("library.yaml"))` from it (no behaviour change). The test builds `TemplateLibrary.from_mappings(_LOCAL, (), library_path=tmp_path / "library.yaml", addons=[installed(tmp_path, "release", library={"tasks": {"base": {"kind": "subprocess", "command": "true"}}, "nodes": {"stage": {"kind": "exec", "tasks": [{"id": "t", "extends": "base"}]}}})])`, `installed` from `support.addons`.
     - `installed()` writes the files as given; `_add_addon` qualifies the bare `base` on load (`load.qualify`).
     - A subprocess task is refused only at install (`update.problems`), never by `_add_addon` (`templates/library.py:380-402` reads and qualifies, nothing else), so this shape loads.
     - Pass every file through `installed(...)`'s arguments and never write into `addon.root` afterwards: item 2 (merging after you) turns `installed()` into a digest-checked store (Coordination).
   - `shown, _ = revision.render(_artifact({"rationale": "r", "add": [_add("build", node)]}), _chain(), GATE, library)`, then assert `` f"- add `x` after `build`, from {source} -- plan: needs it" in shown ``.
   - It fails first: today's line has no `from`.
2. Code: `_sources(node: AddedNode) -> list[str]` returns `node.extends`, or each task's `extends` over `node.tasks` or every `step.tasks`, deduplicated in order (`dict.fromkeys`). In `render` (:462):

   ```python
   lines += [
       f"- add `{a.node.id}` after `{a.after}`, from "
       f"{', '.join(f'`{s}`' for s in _sources(a.node))} -- {a.evidence}"
       for a in changes.add
   ]
   ```

3. `just test tests/templates/test_revision.py tests/api/test_chain_revision_gate.py tests/executor/test_chain_revision.py`. Nothing else asserts the old add line (`git grep -n "add \`" tests` finds none), and `digest` hashes the revised chain, not the text.
4. Mutation: drop `, from ...` and the three rows fail. Revert.

### Task 5: The item-draft door, end to end

Files: `tests/api/test_addon_content.py`.

1. New `test_an_item_draft_adds_an_addons_node(client, repo, tmp_path)`:
   - Call `load_release(client, tmp_path, library={"tasks": {"base": {**AGENT, "skill": "notes"}}, "nodes": {"build": BUILD}})`. Reuse the module's `BUILD`, and move the test below it.
   - File a paused `default` item, as `tests/api/test_item_drafts.py::_filed` does. Inline the two lines rather than import a private helper. If `just check-tests` flags a duplicate body, move `_filed` to `tests/support/api.py` and import it from both.
   - `PUT /api/work-items/{wid}/draft` with `{"op": "add_node", "after": "verification", "node": {"id": "release_build", "extends": "release:build"}}`.
   - Assert a 200, `problems == []`, and `release_build` among `nodes`.
   - `POST .../draft/apply` returns 200. Read the item's `materialized_chain` the way `test_item_drafts.py` reads the row. Assert `MaterializedChain.from_json(...).chain.addons` has `release`.
   - Agent tasks need the fake `claude` harness: `AGENT` uses `codex`. If `default`'s policy refuses `codex` (`allowed_harnesses`), give the node's tasks the harness the `client` fixture's templates use. Check `templates_dir` in `tests/conftest.py`.
2. Mutation: revert task 2's type, and the PUT answers 422. Revert.
3. `just test tests/api/test_addon_content.py tests/api/test_item_drafts.py tests/drafts/test_item.py`.

### Task 6: The add-node menu pre-fills a bare id

Files: `frontend/src/ng/item/draft/AddNodeMenu.tsx`, `AddNodeMenu.test.tsx`.

1. Test first: turn "fills the id with the library id, and Create sends add_node after the seam's node" into `it.each([["security", "security"], ["release:stage", "stage"]])`. Keep that title, with the base appended.
   - Add `{ kind: "nodes", name: "release:stage", definition: { tasks: [{ id: "t" }] } }` to `library`.
   - The row picks the option named `/release:stage/`, expects the id box to hold `stage` and to be accepted unedited, and expects the PUT body `node: { id: "stage", extends: "release:stage" }`.
   - Edit the existing row's flow (clear, then type `security_scan`) only as needed for the shared body. Either keep the rename in both rows or drop it in both.
   - The `release:stage` row fails first: the box holds `release:stage` and the button is disabled.
2. Code (:37): `initial={base.split(":").pop()!}`.
3. Mutation: revert, and the add-on row fails. Revert.
4. `just test-ui`.

### Task 7: Tell the revising agent

Files: `src/kraft/skills/chain-review/SKILL.md`.

1. The `add` bullet (:60-67): after the two shapes, add "A component an add-on ships is named as `kraft admin templates library` lists it, `<namespace>:<name>` (`release:security-review`); the `id` you give the node or a task is always bare."
2. The checklist (:138): "Does every added node and task `extend` a component `kraft admin templates library` lists, by the name it lists, and give a bare `id`?"
3. `just test tests/skills/test_chain_review.py`. The examples' keys are unchanged, so it stays green.

### Task 8: Docs and intent

1. **Intent.** Add `## REQ a-revision-can-add-an-addon-component` to `docs/intent/kraft-addons.md`, right after `running-item-keeps-its-addon-versions`, with the text, `enforced-by` and `origin` from the spec's Requirement section. The ids must match the rows as written in tasks 1, 3 and 5. Leave the existing REQ untouched. Run `just intent`.
2. **Docs.** Each of the following gets one sentence or table cell, within the 80-word and 40-word limits:
   - `docsite/content/5.reference/03.configuration/04.library-and-chains.md` §Qualified names: the first bullet, "`extends`, `steering`, `skill` and `profile` take a qualified name", gains "including on a node a chain revision or an item draft adds".
   - `docsite/content/5.reference/03.configuration/12.addons.md`:
     - the table row "A task, step or node" becomes `extends: release:implementer`, also in a chain revision's or an item draft's added node;
     - §What a work item pins, the chain-revision bullet: "resolves against the pinned versions, and may add a node from an add-on the item had not read, which then joins its pins at the lock's version."
   - `docsite/content/2.concepts/1.how-a-work-item-runs.md` §Chain revision:
     - "add one built from library components, yours or an installed add-on's";
     - the gate shows "each change with the line of the spec or plan behind it, the component each added node comes from, and the diff".
   - `docsite/content/5.reference/08.http-api/8.draft-ops.md` §`add_node` on an item draft: "`extends` names your library's component or an add-on's as `<namespace>:<name>`; `id` is always bare."
   - `docsite/content/6.project/1.security.md` §Kraft add-ons, "Nothing changes without a review": new bullet. "A chain revision or an item draft can add an installed add-on's component to a running item: a revision only through its gate, which names the component, and a draft only by your own apply. The item then pins that add-on's version."
   - Then run `uv run python dev/check_docs_walls.py` on each touched page, and `dev/check_docs_redirects.py` (no heading moves).
3. **Checks.** Run `just lint`, `just check-tests` and `just intent`. Then run `just test` (testmon) and `just test-ui`.
4. Commit.

### Task 9: Final verification and the PR

1. **Merge the integration branch in:** `git fetch origin && git merge origin/ccr-143df22f-uetbpy`. Item 1 may have landed; it touches none of your files (Coordination).
2. **Checks**, on the merged head:

   ```bash
   just lint
   just intent
   just check-tests
   just test tests/addons/test_pins.py tests/templates/test_revision.py tests/api/test_addon_content.py tests/api/test_item_drafts.py tests/drafts/test_item.py tests/api/test_chain_revision_gate.py tests/executor/test_chain_revision.py tests/executor/test_walk_revised.py tests/skills/test_chain_review.py --no-testmon
   just test            # testmon: everything else this branch touched
   just test-ui
   uv run python dev/check_docs_walls.py docsite/content/5.reference/03.configuration/04.library-and-chains.md docsite/content/5.reference/03.configuration/12.addons.md docsite/content/2.concepts/1.how-a-work-item-runs.md docsite/content/5.reference/08.http-api/8.draft-ops.md docsite/content/6.project/1.security.md
   uv run python dev/check_docs_redirects.py
   wc -l tests/addons/test_pins.py tests/templates/test_revision.py tests/api/test_addon_content.py   # each <= 800
   ```

3. Write the PR body to `${TMPDIR:-/tmp}/pr-body-3.md` (outside the worktree), run `uv run python dev/check_removals.py origin/ccr-143df22f-uetbpy "${TMPDIR:-/tmp}/pr-body-3.md"` (exit 0), then `gh pr create --base ccr-143df22f-uetbpy --label release::none --title "A chain revision can add a node that extends an add-on's component" --body-file "${TMPDIR:-/tmp}/pr-body-3.md"`.

**PR body:**

- Base branch: `ccr-143df22f-uetbpy` (DECISIONS D1), not `main`.
- Label `release::none`. Add-ons (#700, `041216a`) are in no tag: `git tag --contains 041216a` is empty and the latest is `v2.0.0`. This completes unreleased behaviour and rides with the release that ships add-ons. If a release ships add-ons before this merges, it becomes `release::minor`.
- `## Changelog` (DECISIONS D6/D9: written even under `release::none`, for the final PR to collect): "A chain revision or an item draft can add a node or task that extends an installed add-on's component (`release:stage`); the revision gate names where each added node comes from."
- `## Removed tests`: none. `test_a_revision_resolves_against_pinned_addons` keeps its name and its two ids, and the frontend case is reshaped within its file (the `it` title gains the base, which `check_removals` does not track for a kept file).
- `## Test evidence`: paste the last lines of every command in step 2 and of `check_removals`, as run on the merged head.
- Mutation table: one row per mutation in tasks 2-6, "applied, confirmed failing, reverted".
- Note for item 4 (repo-library scoping): `_added_nodes` now sees `<repo-id>:x` directly; item 4 adds the direct-form row (DECISIONS D7).

---

## Coordination

Order: 1, **3**, 2, 4.

- **Item 1** touches none of your files.
- **Item 2 (store reads checked against the digest)** lands after you. It turns `support.addons.installed()` into a `store/<digest>/` layout with a `.kraft-digest` manifest, and makes `TemplateLibrary._add_addon` and `load.for_item` read through that manifest. Your new tests (`test_the_gate_names_what_an_added_node_comes_from`, the `test_pins` rows) keep working as long as every file is passed through `installed(...)`/`publish(...)` and never written into a store afterwards. Item 2 re-runs your tests after merging; you owe no row.
- **Item 4 (repo library scoped to its repo)** lands last and changes the same file, `templates/revision.py`:
  - it adds `repo_id: str | None = None` to `revise`, `render`, `artifact_digest` and `drafts.item.evaluate`, and threads it through `_pinned` and `_added_nodes`. `None` means "no repository": repo libraries are out of scope, add-ons untouched. Your calls without `repo_id` stay valid because your rows name only add-ons and local components, which scope never touches (DECISIONS D10);
  - it rewrites `render`'s signature, not its change lines: keep your `from ...` add line and `_sources` helper as written, and item 4 merges around it;
  - it appends the left-out reason to `TemplateLibrary`'s "extends no X named 'Y:n'" message. Your refusal rows use `match=r"extends no (node|task) named"` (a search), so they keep passing; do not anchor that regex with `$`;
  - it rewrites `TemplateLibrary._pins` to pin from references, not prose. Your pins come from references (`nodes.release:stage`, `tasks.release:base`), so your rows keep their pin sets;
  - the cross-item row "a revision adds another repository's library component directly" (`AddedNode(id="x", tasks=[{"id": "t", "extends": "app:base"}])` refused for an item in another repo) needs both your type change and item 4's scope check: **item 4 adds it** (DECISIONS D7). Do not add a repo-library row here.
- Docs: item 2 edits other paragraphs of `12.addons.md` and `1.security.md`, and item 4 other paragraphs of `1.security.md`. Item 2 and item 1 add REQs elsewhere in `kraft-addons.md`; yours goes right after `running-item-keeps-its-addon-versions`. Textual only.
