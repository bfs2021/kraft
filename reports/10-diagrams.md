# 10-diagrams: redraw the docs diagrams in the StageStrip style

PR: https://github.com/itsOmidKarami/kraft/pull/774 (kraft/docs-diagrams → kraft/docs-design, label release::none)

## Summary

Bead Kraft-8zq5z covered the docs' ten diagrams, which were Mermaid SVGs shown as images. Plex could not load in them, they could not follow dark mode, their label sizes differed, and a screen reader got an image announced as a button. The chain was drawn three ways. All ten are now markup in the StageStrip vocabulary, drawn by three MDC components with one shared frame:

- `::diagram-flow`: stages with branch trees, loops and groups
- `::diagram-graph`: nodes with their outgoing edges, used for the status machine and the components
- `::diagram-sequence`: numbered messages

The shared language is Plex Mono at 14px throughout, `›`/`→`/`⇢`/`↻` arrows, the violet gate chip, and one group frame. Each diagram is a `<figure>` with a `<figcaption>` (the old alt text) and list semantics. The Mermaid sources, configs and SVGs, the `docs-diagrams` recipe, and the ARCHITECTURE.md image are removed. CONTRIBUTING says how a diagram is written now. The stable (v2.0.0) build still shows images: `dev/build_docs_site.sh` takes `public/diagrams/` from the tag, and ProseImg's diagram handling and prose.css's dark card stay with a "remove when" comment.

## Decisions

- YAML-prop components rather than Markdown slots: they give exact semantic markup. The LLM raw copies show the data as a JSON prop, the same as the landing hero's `:links`.
- Vertical, one stage per line, at every width, like StageStrip on a phone. Rows with notes wrapped badly. Parallel lanes (remote ways) and the graphs use a 2–3 column grid.
- Notes go on the line under the name, toned; names are highlighted. Colour, not size, sets them apart, because the brief asked for one label size.
- The gate chip is also used for `needs_human` and "waits for you" outcomes, since a person decides there.
- Chip text uses violet-700 in light mode and violet-300 in dark. `--ui-primary` on the chip tint was 4.3:1 and 4.1:1, which fails AA at 14px; StageStrip's chip passes only because it is large text.
- `⇢` is the one dashed notation: a conditional path (permission "left to the CLI", "network, when sandboxed") or a reply in the sequence.
- Unlabelled implied edges got the pages' own words: fix-loop "no" and "one holds", status `filed` as the start node, and the "Outside tools" frame for gh/bd.
- Permission gate: allow and deny each list `permission_decision`, because a tree cannot join two branches.
- `public/diagrams/` comes from the tag in the stable build instead of being kept in main. The v2.0.0 SVGs differ from main's (its status machine has no queued or blocked), so the tag's copies are the correct ones anyway.
- Left alone: `dev/check_docs_redirects.py`'s `/diagrams/` file root and its test row. They are harmless and out of scope.

## Checks

- check_docs_coverage, walls, redirects, landings, shell, ledes: all ok.
- `dev/build_docs_site.sh /tmp/kraft-docs-diagrams-site` (next and stable nuxt generate): exit 0. `check_llm_docs.py`: ok.
- Contrast was measured in the browser on every text element of every diagram:

  | Text | Light | Dark |
  |---|---|---|
  | names | 16.3 | 14.6 |
  | toned text | 6.9 | 9.8 |
  | gate name | 5.4 | 5.1 |
  | chip | 5.3 | 6.4 |
  | arrows, graphic only | 4.35 | 5.6 |

- At 390px no figure scrolls sideways and the page does not either. Every figure computes to Plex Mono 14px.

## Screenshots

`10-diagrams/before/` and `10-diagrams/after/`, three shots per diagram (1440, 1440-dark and 390), named `<page>-<diagram>-<1440|1440-dark|390>.png`. The before 390 shots of the landscape diagrams show the old sideways-scroll crop. Pages and diagrams:

- how-a-work-item-runs: lifecycle, structure
- caps-and-budgets: caps-scopes
- permission-gate: permission-gate
- remote-access: remote-ways
- put-a-proxy-in-front-of-kraft: proxy
- statuses: status
- fix-loop: fix-loop
- architecture: components, request-flow

`10-diagrams/stable/` has the stable build's lifecycle and status pages, showing that v2.0.0 still renders its SVGs, with the dark card.

## Skipped or uncertain

- `just` is not installed in this container, so I could not run `just --list` after removing the recipe. The diff is a clean block removal.
- The build logs show @nuxt/fonts "Could not initialize provider" errors. They come from this container's network proxy and are unrelated to this change; the build exits 0.
- Plex's Latin subset has no `→`, `⇢` or `↻`, so those glyphs fall back to the system mono font. That is the same as StageStrip's `→` today.
- The commit message ends with Co-Authored-By followed by the session's Claude-Session line, which the environment adds.
