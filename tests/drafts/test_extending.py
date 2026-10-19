"""The Templates editor's ops on a chain that extends another: every one
writes `remove`, `add` or `overrides`, never a copy of what it inherits."""

from __future__ import annotations

import pytest
from support.drafts import apply_ops, draft_state, refused

IMPLEMENT = "implementation.main.implement"
TEAM = """id: team
extends: default
remove: [external_approval]
add:
  - after: verification
    node:
      id: security_scan
      kind: exec
      tasks:
        - {id: scan, kind: subprocess, command: "true"}
overrides:
  implementation.main.implement: {prompt: Implement it carefully.}
"""


@pytest.fixture
def st(templates_dir, database):
    (templates_dir / "chains" / "team.yaml").write_text(TEAM)
    return draft_state(templates_dir, database)


def team(st, *batch):
    return apply_ops(st, *batch, key="team")


def no(st, *batch) -> str:
    return refused(st, *batch, key="team")


@pytest.mark.parametrize(
    "batch",
    [
        [("add_node", {"at": 3, "id": "lint", "kind": "gate"})],
        [("remove", {"path": "post_merge_ci"})],
        [("move", {"path": "security_scan", "to": 10})],
        [("set_field", {"path": IMPLEMENT, "field": "effort", "value": "high"})],
        [
            (
                "add_task",
                {"container": "security_scan", "step": "main", "kind": "subprocess", "id": "lint"},
            )
        ],
        [("restore", {"node": "external_approval"})],
    ],
    ids=["add_node", "remove", "move", "set_field", "add_task-in-added", "restore"],
)
async def test_no_op_writes_a_nodes_list(st, batch):
    r = team(st, *batch)
    assert "nodes" not in r.model and "\nnodes:" not in r.text


async def test_removing_an_inherited_node_writes_remove(st):
    r = team(st, ("remove", {"path": "post_merge_ci"}))
    assert r.model["remove"] == ["external_approval", "post_merge_ci"]
    assert r.answers == [{"broken": []}]
    assert "post_merge_ci" not in r.resolved_order


async def test_the_editor_keeps_the_final_gate(st):
    assert no(st, ("remove", {"path": "final_review"})).startswith("final_review is the final gate")


async def test_restoring_a_removed_node_deletes_its_entry(st):
    r = team(st, ("restore", {"node": "external_approval"}))
    assert "remove" not in r.model
    order = r.resolved_order
    assert order.index("external_approval") == order.index("mark_ready") + 1


#: A gate added right behind `security_scan` (index 8) first, on the same
#: anchor: an add dropped between the two goes between their entries.
BEHIND = [("add_node", {"at": 9, "id": "notify", "kind": "gate"})]


@pytest.mark.parametrize(
    ("first", "prev", "after"),
    [
        ([], "implementation", "implementation"),
        ([], "verification", "verification"),
        (BEHIND, "security_scan", "verification"),
        ([], "post_merge_ci", "post_merge_ci"),
    ],
    ids=[
        "after-an-inherited-node",
        "before-an-earlier-add-on-that-node",
        "after-an-added-node",
        "at-the-end",
    ],
)
async def test_an_add_resolves_where_it_was_dropped(st, first, prev, after):
    at = team(st, *first).resolved_order.index(prev) + 1
    r = team(st, *first, ("add_node", {"at": at, "id": "lint", "kind": "gate"}))
    assert r.resolved_order[at] == "lint"
    assert next(e for e in r.model["add"] if e["node"]["id"] == "lint")["after"] == after


@pytest.mark.parametrize(
    "batch",
    [
        ("add_node", {"at": 0, "id": "lint", "kind": "gate"}),
        ("move", {"path": "security_scan", "to": 0}),
    ],
    ids=["add_node", "move"],
)
async def test_nothing_goes_before_the_first_node(st, batch):
    assert "no place before spec" in no(st, batch)


@pytest.mark.parametrize(
    "to_after", ["work_item_summary", "implementation"], ids=["later", "earlier"]
)
async def test_moving_an_added_node_rewrites_its_entry(st, to_after):
    rest = [i for i in team(st).resolved_order if i != "security_scan"]
    to = rest.index(to_after) + 1
    r = team(st, ("move", {"path": "security_scan", "to": to}))
    assert r.resolved_order.index("security_scan") == to
    assert r.model["add"][0]["after"] == to_after


@pytest.mark.parametrize(
    ("batch", "error"),
    [
        ([("remove", {"path": "verification"})], "security_scan goes after it"),
        ([("remove", {"path": "spec"})], "spec_approval's reject_to names it"),
        (
            [
                ("remove", {"path": "spec_approval"}),
                ("remove", {"path": "spec"}),
                ("restore", {"node": "spec_approval"}),
            ],
            "restore spec first",
        ),
    ],
    ids=["remove-an-anchor", "remove-a-pointer-target", "restore-a-pointer-to-a-removed-node"],
)
async def test_the_editor_leaves_nothing_naming_a_removed_node(st, batch, error):
    assert error in no(st, *batch)
