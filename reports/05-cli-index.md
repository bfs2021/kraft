# 05-cli-index

PR: https://github.com/itsOmidKarami/kraft/pull/766 (branch kraft/docs-cli-index, base kraft/docs-design, label release::none)

## Summary
The item, view, repo and admin CLI pages each open with a `## Verbs at a glance` table after the opening paragraph: the verb in code (linked), a one-line purpose, and the anchor of the section documenting it. Task-named headings are untouched. This answers the critique finding that /reference/cli/item is ~15,900px with 15 tables and an "On this page" that names tasks, not verbs. `reference/cli` (index) already is a task-to-command finder, so it was left alone.

## Decisions
- Two columns (linked verb, purpose), not three: a separate link column made each phone card taller, and at 390px the table still reflows to cards.
- Verbs derived from each page's sections and cross-checked against `kraft <group> --help`: all 27 item, 13 view, 6 repo, 16 admin top-level verbs present; none extra. A script checked every anchor against the page's heading slugs.
- repo and admin had no heading over their command table, so path, open, reindex, mcp and permission-hook had no anchor: added `## Commands` above that table and linked those rows to it.
- repo had no opening paragraph (page began with a code block); added one sentence on omitting the ID inside a worktree, so the index is not the first thing under the title.
- admin index collapses `templates`, `addon` and install/uninstall-service to one row each (the existing table lists each of the 30 forms); install-service and init link to their guides.
- Did not reuse check_docs_coverage data: it only checks mentions, and wording is hand-written.

## Checks
coverage, walls, redirects, landings, shell, ledes: all ok. `nuxt generate` (next): exit 0.

## Screenshots
05-cli-index/{before,after}/{item,view,repo,admin}-{1440,390}.png (light, top of page).

## Sidebar split (not done, as instructed)
Not warranted now. Reference (11), Configuration (13) and Run the server (11) are all flat lists of sibling pages with clear names, and the sidebar already collapses groups. Configuration at 13 is the one to watch; split it only if it passes ~15 or a clear seam (e.g. files vs. policy) emerges.

## Uncertain
- The linked verb renders as a dark code chip, not link-coloured, as for linked code elsewhere on the site; the affordance is weak but consistent. A site-wide fix is out of scope.
