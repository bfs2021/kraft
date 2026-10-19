"""The Templates editor's ops on a chain that extends another (`extends:`
plus `remove`, `add` and `overrides`): each writes one of those edits, and none
copies an inherited component into the file. A node the chain adds lives in
the file (`add[].node`), so the ordinary op edits it there; an inherited one
has no edit form for a structural change, which answers 422 naming the YAML
view and Detach (`docs/intent/templates-editor.md`)."""

from __future__ import annotations

from typing import Literal

from kraft.drafts import authored, ops
from kraft.drafts.ops import Draft, OpError, _check_id, _position
from kraft.drafts.ops import _extending as parent_of
from kraft.templates.library import ComponentSource, Namespace, TemplateLibraryError, _Resolution
from kraft.templates.models import PATH_SEPARATOR

Owner = Literal["chain", "added", "inherited", "removed"]


def _inherited_message(d: Draft, path: str) -> str:
    return (
        f"{path} is inherited from {parent_of(d)}; change it in the YAML view "
        "(an override that replaces its list), or detach the chain"
    )


def _order(d: Draft) -> list[dict]:
    """The resolved chain's nodes, edits applied (item 1's `_extend`, through
    `Draft.expanded`)."""
    nodes = d.expanded().get("nodes")
    if not isinstance(nodes, list):
        raise OpError(f"{d.key} does not resolve; fix it in the YAML view first")
    return [n for n in nodes if isinstance(n, dict)]


def _ids(d: Draft) -> list[str]:
    return [n.get("id") for n in _order(d)]


def _list(d: Draft, key: str) -> list:
    """The chain's `remove` or `add` list, made when absent."""
    if not isinstance(d.chain.get(key), list):
        authored.put(d.chain, "", key, [])
    return d.chain[key]


def _prune(d: Draft, key: str) -> None:
    """An edit key left empty goes."""
    if key in d.chain and not d.chain[key]:
        del d.chain[key]


def _added(d: Draft) -> list[str]:
    return [n.get("id") for n in authored.added_nodes(d._chain)]


def _removed(d: Draft) -> list:
    removed = d._chain.get("remove")
    return removed if isinstance(removed, list) else []


def _entry(d: Draft, id: str) -> int:
    """The index of the `add` entry adding node `id`."""
    return next(i for i, e in enumerate(_list(d, "add")) if (e.get("node") or {}).get("id") == id)


def owner(d: Draft, path: str) -> Owner:
    """Who holds the component at `path`, decided by its node: the file (the
    chain itself, or a node it adds), the parent, or nobody since this chain
    removes it."""
    if not path:
        return "chain"
    root = path.split(PATH_SEPARATOR)[0]
    if root in _added(d):
        return "added"
    if root in _removed(d):
        return "removed"
    if root in _ids(d):
        return "inherited"
    raise OpError(f"nothing at {path!r}")


def _place(d: Draft, entry: dict, order: list[str], at: int) -> None:
    """Write `entry` (`{after, node}`) into `add` so its node resolves at index
    `at` of `order`, the resolved ids without it. Adds after one node resolve
    in written order (item 1), and anchor only on a parent node: after an
    inherited `prev`, first among its adds; after an added `prev`, right behind
    `prev`'s entry, on its anchor."""
    if at == 0:
        first = order[0] if order else "the first node"
        raise OpError(
            "an extending chain adds a node after one of its parent's nodes; "
            f"there is no place before {first}"
        )
    adds = _list(d, "add")
    index = {(e.get("node") or {}).get("id"): i for i, e in enumerate(adds)}
    prev = order[at - 1]
    if prev in index:
        entry["after"] = adds[index[prev]]["after"]
        adds.insert(index[prev] + 1, entry)
    else:
        entry["after"] = prev
        first = next((i for i, e in enumerate(adds) if e.get("after") == prev), len(adds))
        adds.insert(first, entry)


def add_node(d: Draft, at: int, id: str, kind: str) -> None:
    ids = _ids(d)
    _check_id(id, [*ids, *_removed(d)])
    if kind not in ("exec", "gate"):
        raise OpError(f"a node is exec or gate, not {kind!r}")
    node = {"id": id, "kind": kind} if kind == "gate" else {"id": id, "kind": kind, "steps": []}
    _place(d, {"after": None, "node": node}, ids, _position(at, len(ids)))


def move(d: Draft, path: str, to: int, to_step: str | None = None) -> None:
    if PATH_SEPARATOR in path or to_step is not None:
        return _inside(d, path, ops.move, path=path, to=to, to_step=to_step)
    if owner(d, path) != "added":
        raise OpError(
            f"{path} is {parent_of(d)}'s node; an extending chain keeps its parent's "
            "order. Detach the chain to reorder it"
        )
    before = _order(d)
    rest = [n for n in before if n.get("id") != path]
    to = _position(to, len(rest))
    moved = next(n for n in before if n.get("id") == path)
    # Only a violation the new order adds refuses it, as `ops.move` checks.
    old = set(ops.order_issues(before))
    if bad := [x for x in ops.order_issues([*rest[:to], moved, *rest[to:]]) if x not in old]:
        raise OpError(f"can't move {path}: {bad[0]}")
    entry = _list(d, "add").pop(_entry(d, path))
    _place(d, entry, [n.get("id") for n in rest], to)
    return None


def remove(d: Draft, path: str) -> dict:
    if PATH_SEPARATOR in path:
        return _inside(d, path, ops.remove, path=path)
    who = owner(d, path)
    if who == "removed":
        raise OpError(f"{path} is already removed; put it back with restore")
    nodes = _order(d)
    broken = [r for r in ops.references(nodes, path) if r["path"] != path]
    if who == "added":
        del _list(d, "add")[_entry(d, path)]
        _prune(d, "add")
        return {"broken": broken}
    # Refused here, not only at resolve: once the edits don't apply, the
    # chain has no nodes for the canvas to draw or to edit back.
    if next(n for n in nodes if n.get("id") == path).get("chain_finalized"):
        raise OpError(f"{path} is the final gate, which an extending chain keeps")
    adds = [e for e in d._chain.get("add") or () if isinstance(e, dict)]
    if follows := [(e.get("node") or {}).get("id") for e in adds if e.get("after") == path]:
        raise OpError(f"can't remove {path}: {follows[0]} goes after it; move {follows[0]} first")
    if broken:
        ref = broken[0]
        raise OpError(
            f"can't remove {path}: {ref['path']}'s {ref['field']} names it; "
            "point it elsewhere first"
        )
    _list(d, "remove").append(path)
    return {"broken": []}


def restore(d: Draft, node: str) -> None:
    if node not in _removed(d):
        raise OpError(f"{node} is not removed from {parent_of(d)}")
    # The parent's own node: item 1 refuses an override of a removed one.
    bare = d.expanded({"id": d.key, "extends": parent_of(d)}).get("nodes") or []
    mine = next((n for n in bare if n.get("id") == node), {})
    pointers = (mine.get("reject_to"), ops._restart_from(mine))
    if gone := [t for t in pointers if t != node and t in _removed(d)]:
        raise OpError(f"restore {gone[0]} first: {node} names it, and this chain removes it")
    d.chain["remove"].remove(node)
    _prune(d, "remove")


def _inside(d: Draft, path: str, fn, **fields):
    """`fn` on a component the file holds (the chain, or a node it adds); a
    refusal naming the way out otherwise."""
    who = owner(d, path)
    if who in ("chain", "added"):
        return fn(d, **fields)
    if who == "removed":
        raise OpError(f"{path.split(PATH_SEPARATOR)[0]} is removed; restore it first")
    raise OpError(_inherited_message(d, path))


def expansion_error(d: Draft) -> str | None:
    """Why `d`'s chain does not expand (its edits don't apply to its parent),
    or None when it does."""
    library = d.resolving_library()
    if library is None or not isinstance(d._chain, dict):
        return None
    raw = authored.parse(authored.dump(d._chain))
    source = ComponentSource(d.st.templates_dir / d.name, Namespace.NODES, d.key, chain=True)
    try:
        _Resolution(library, source).expand_chain({**raw, "id": d.key})
    except TemplateLibraryError as exc:
        return str(exc)
    return None


OPS = {
    **ops.OPS,
    "add_node": add_node,
    "move": move,
    "remove": remove,
    "restore": restore,
}
