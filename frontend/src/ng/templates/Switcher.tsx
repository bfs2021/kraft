import { useEffect, useRef, useState, type KeyboardEvent } from "react";
import { Check, ChevronDown } from "lucide-react";
import * as api from "../../api";
import { useStore } from "../../store";
import { Popover } from "../ui/Popover";
import { listDrafts } from "./draft/draftApi";
import { focusSoon } from "./menus/focus";
import { IdRow } from "./menus/IdRow";
import { isOpen } from "../board/counts";
import type { Addon } from "../../types";
import { AddonBadge } from "./addon";
import { NoMatch } from "../ui/NoMatch";
import { Empty } from "../ui/Empty";

type Row = { id: string; nodes: number; open: number; draft: boolean; addon?: Addon | null };
export type SwitchTo = { kind: "switch"; id: string } | { kind: "new"; id: string } | { kind: "dup"; id: string } | { kind: "extend"; id: string };
type Stage = "list" | "new" | "dup" | "extend";

/** The chain crumb, and the switcher it opens (Decisions §9 Chain switcher):
 *  search, every chain with its size and open items, ✓ on the current one,
 *  an amber dot on one with a draft; then New chain and Duplicate, which turn
 *  the menu into the id step. No Delete here. An add-on's chain (`copy`) is
 *  duplicated as "Copy to my library", from the page's own button. Extend starts
 *  a chain that follows this one (`extend`: not a repo library's). */
export function Switcher({ chain, renamedTo, onGo, startDup, startExtend, copy, extend = true }: { chain: string; renamedTo?: string; onGo: (to: SwitchTo) => void; startDup?: number; startExtend?: number; copy?: boolean; extend?: boolean }) {
  const [open, setOpen] = useState(false);
  const [stage, setStage] = useState<Stage>("list");
  const [rows, setRows] = useState<Row[] | null>(null);
  const [q, setQ] = useState("");
  const items = useStore((s) => s.workItems);
  const button = useRef<HTMLButtonElement>(null);
  const search = useRef<HTMLInputElement>(null);
  const refs = useRef<(HTMLButtonElement | null)[]>([]);

  const show = (st: Stage) => {
    setStage(st);
    setQ("");
    setOpen(true);
  };
  // The chain pane's Duplicate opens this at its id step.
  useEffect(() => { if (startDup) show("dup"); }, [startDup]);
  // The add-on chain's Extend opens this at its id step.
  useEffect(() => { if (startExtend) show("extend"); }, [startExtend]);
  useEffect(() => {
    if (!open) return;
    Promise.all([api.getTemplates(), listDrafts()]).then(([chains, drafts]) => {
      const drafted = new Set(drafts.status === 200 ? drafts.body.filter((x) => x.area === "chains").map((x) => x.key) : []);
      const all = Object.values(items);
      const ids = [...chains.map((c) => c.id), ...[...drafted].filter((k) => !chains.some((c) => c.id === k))];
      setRows(ids.map((id) => ({
        id,
        nodes: chains.find((c) => c.id === id)?.nodes.length ?? 0,
        open: all.filter((w) => w.chain_template === id && isOpen(w)).length,
        draft: drafted.has(id),
        addon: chains.find((c) => c.id === id)?.addon,
      })));
    }).catch(() => setRows([]));
    if (stage === "list") focusSoon(search.current);
  }, [open, stage, items]);

  const close = () => {
    setOpen(false);
    button.current?.focus();
  };
  const shown = (rows ?? []).filter((r) => !q || r.id.includes(q.toLowerCase()));
  const move = (e: KeyboardEvent, from: number) => {
    if (e.key !== "ArrowDown" && e.key !== "ArrowUp") return;
    e.preventDefault();
    const to = from + (e.key === "ArrowDown" ? 1 : -1);
    if (to < 0) search.current?.focus();
    else refs.current[Math.min(to, shown.length + 2)]?.focus();
  };
  const dupTitle = copy ? `Copy ${chain} to my library as` : `Duplicate ${chain} as`;
  const bare = chain.split(":").pop()!;
  const step = {
    new: { title: "New chain id", label: "New chain id", initial: "", go: "Create →" },
    // An add-on's chain id is `<namespace>:<name>`; the copy is the operator's own, so it starts from the bare name.
    dup: { title: dupTitle, label: "Duplicate id", initial: copy ? bare : `${chain}_copy`, go: copy ? "Copy →" : "Duplicate →" },
    extend: { title: `Extend ${chain} as`, label: "Extending chain id", initial: `${bare}_ext`, go: "Extend →" },
  };
  const go = (to: SwitchTo) => {
    setOpen(false);
    onGo(to);
  };
  return (
    <>
      <button ref={button} type="button" className={`tpl-switch${open ? " is-open" : ""}`} aria-haspopup="dialog" aria-expanded={open} aria-label={`Chain ${chain}${renamedTo ? `, renamed to ${renamedTo} in the draft` : ""}, switch chain`} onClick={() => (open ? close() : show("list"))}>
        {chain}{renamedTo && <> → {renamedTo}</>} <ChevronDown size={12} aria-hidden />
      </button>
      <Popover anchor={button} open={open} onClose={close} role="dialog" label={stage === "list" ? "Switch chain" : step[stage].title}>
        {stage === "list" ? (
          <div className="task-menu sw">
            <input ref={search} className="picklist-q" aria-label="Search chains" placeholder="Search chains" value={q} onChange={(e) => setQ(e.target.value)} onKeyDown={(e) => {
              move(e, -1);
              if (e.key === "Enter" && shown[0]) go({ kind: "switch", id: shown[0].id });
            }} />
            <div className="picklist-items" role="listbox" aria-label="Chains">
              {rows === null && <Empty className="picklist-empty">Loading…</Empty>}
              {rows !== null && !shown.length && q && <NoMatch className="picklist-empty" query={q} onClear={() => setQ("")} />}
              {shown.map((r, k) => (
                <button key={r.id} ref={(el) => void (refs.current[k] = el)} type="button" role="option" aria-selected={r.id === chain} className="menu-item sw-row" onKeyDown={(e) => move(e, k)} onClick={() => go({ kind: "switch", id: r.id })}>
                  <span className="sw-check" aria-hidden="true">{r.id === chain && <Check size={12} />}</span>
                  <span className="sw-main"><span className="picklist-name">{r.id}</span><span className="picklist-sub">{r.nodes} nodes · {r.open} open</span></span>
                  {r.addon && <AddonBadge addon={r.addon} />}
                  {r.draft && <span className="sw-dot" aria-label="unpublished draft" />}
                </button>
              ))}
            </div>
            <div className="sw-acts">
              <button ref={(el) => void (refs.current[shown.length] = el)} type="button" className="menu-item" onKeyDown={(e) => move(e, shown.length)} onClick={() => show("new")}>New chain</button>
              {!copy && <button ref={(el) => void (refs.current[shown.length + 1] = el)} type="button" className="menu-item" onKeyDown={(e) => move(e, shown.length + 1)} onClick={() => show("dup")}>Duplicate</button>}
              {extend && <button ref={(el) => void (refs.current[shown.length + 2] = el)} type="button" className="menu-item" onKeyDown={(e) => move(e, shown.length + 2)} onClick={() => show("extend")}>Extend</button>}
            </div>
          </div>
        ) : (
          <div className="seam-id">
            <p className="menu-title">{step[stage].title}</p>
            <IdRow
              label={step[stage].label}
              initial={step[stage].initial}
              taken={(rows ?? []).map((r) => r.id)}
              go={step[stage].go}
              onGo={(id) => go({ kind: stage, id })}
            />
          </div>
        )}
      </Popover>
    </>
  );
}
