# 09-p1-fixes

PR: https://github.com/itsOmidKarami/kraft/pull/773 (branch kraft/docs-p1-fixes, base kraft/docs-design, label release::none)

## Summary
The skip link now lands in the page: `#main-content` moved from `UMain` (which wraps the left sidebar) to a `div` around the `<slot />` in `layouts/docs.vue`. Search: `utils/searchSections.ts` emits one extra section per row of a CLI "Verbs at a glance" table (title `kraft item approve`, content the row's purpose, id the row's link target); `AppSearch.vue` ranks by Fuse score (weight 0.3) plus how much of the query is in the hit's title/text, a page ahead of its subsections, verbs exempt from the Reference penalty, and the results are shown as one group.

## Decisions
- Wrapper `div#main-content` inside `UPage`'s default slot, not a change to Docus: it holds the page header, body and the page's own right aside; the first focusable inside is "Copy page". default.vue and error.vue untouched.
- Reference penalty kept (0.55) but verbs (label starts with `kraft `) are exempt; verbs also get a larger title bonus.
- Fuse's score barely separates hits (all near 0, ties by index, hence Overview first for "approve"), so my rank is mostly title/text coverage of the query words.
- Punctuated queries (/ - _ .) skip the Reference penalty and the page-over-subsection preference, so a route section leads for "/api/budget".
- Per-page cap: not possible with the sort function alone (it orders, it does not drop); would need a fork of ContentSearch. Approximated by ranking pages ahead of their subsections. "raise budget" top 5 has at most 2 from any one page.
- Single result group: Nuxt UI renders one group per top-level nav section, ordered by best hit, so the verb (Reference) always followed the guide's subsections. Wrapping the navigation in one parent (`searchNavigation`) makes a single rank-ordered list; group headings (Guides, Reference...) are gone, breadcrumbs remain. This is a visible change.
- For "approve" the guide shows as its page "Reviewing a change" at 5.

## Top 5 before / after
See the PR body (same table).

## Checks
check_docs_coverage/walls/redirects/landings/shell/ledes: exit 0. `nuxt generate` (next): exit 0. One `id="main-content"` in index.html, get-started/install.html, 404.html. Skip link (Tab, Enter, Tab on /next/get-started/install): before sidebar "Get started" button, after "Copy page".

## Screenshots
09-p1-fixes/after: install-focus.png, search-approve.png, search-raise-budget.png. 09-p1-fixes/before: search-approve.png, search-raise-budget.png.

## Skipped / uncertain
- No before/after of install-focus.png pair: the before shot was overwritten by a run made after my layout change, so only the after is kept; the before is recorded as text (focus on the sidebar's "Get started" button).
- The before search shots for "approve"/"raise budget" show the old ranking; "approve" before shows the default results, because that is what the old ranking produced.
- Dark mode and stable build not shot (item asked for light, 1440). Search tuning constants were set by hand against these six queries only.
