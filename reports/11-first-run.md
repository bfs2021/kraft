# 11-first-run report

PR: https://github.com/itsOmidKarami/kraft/pull/771 (branch kraft/docs-first-run, base kraft/docs-design, label release::none)

## Summary
"Your first work item" is now Part 1 of 2 and ends when the quick-task run lands on the board (steps 1-5, plus Troubleshooting and a "Next: the real chain" pointer). Steps 6-7 and Next steps moved to a new page, "The real chain" (Part 2 of 2). "Why Kraft" moves the etymology to a closing "The name" section and turns the nine bullets into bold headlines with one or two sentences each. Full-page height at 1440: 10,084px -> 7,051px (part 1) + 4,286px (part 2).

## Decisions
- New file 3.the-real-chain.md; faq renumbered 3 -> 4 (URLs carry no numbers).
- Terminal connect path sits after the agent path as "### Or from a terminal"; no collapsible component exists in the site, so it is a labelled section, not interleaved. "If connect finds no test or setup command" is now an h4 under it (anchor unchanged).
- Troubleshooting stays on Part 1 (the first-run stops happen there); step 6/7 links point to it.
- Redirects added for `#_6-...`, `#_7-...`, `#next-steps`; the old `#where-to-go-from-here` redirect repointed to the new page.
- Steps keep their 6/7 numbering on page 2 so existing anchors and the "step 6" references stay true.
- The Claude Code slash-command note is split: /kraft:onboard, handoff, board on Part 1; /kraft:gates on Part 2.
- Why Kraft bullets: every fact kept; where a fact needed a second sentence I kept it (Checks, Several agents).
- Landing page link to /get-started/first-work-item untouched.

## Checks
coverage, walls, redirects, landings, shell, ledes: all ok. `nuxt generate` (next): exit 0.

## Screenshots
before/ and after/: first-work-item-1440, first-work-item-390, why-kraft-1440, why-kraft-390; after/ also the-real-chain-1440.

## Uncertain
Part 1 is still ~7,000px at 1440 because the step content is kept whole (move, don't delete). The 390 viewport shots are the first screen only.
