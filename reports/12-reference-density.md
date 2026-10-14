# 12-reference-density

PR: https://github.com/itsOmidKarami/kraft/pull/772

Summary: the copy button no longer covers command text (below 1024px it sits on a row above the block; from 1024px up it stays a hover button with the existing first-line padding). Inline code is a tint with no border; in headings it is plain mono in the heading colour. Table cells are 6px above and below instead of 12 (rows ~37px, was 51).

Decisions
- Button on its own row below 1024px: padding only clears it once scrolled to the line end, so it cannot guarantee clear text at rest.
- Titled blocks keep the button in the title bar.
- Padding rule for first line limited to 1024px and up, where the button overlays.
- Table padding changed for all tables; the phone card reflow sets its own padding and is unaffected (checked 390px page).
- Method badge skipped: needs content changes.

Checks: the six dev/check_docs_*.py pass; nuxt generate (next) exit 0. Contrast not re-measured numerically: heading code inherits heading colour, the tint is Nuxt UI's existing bg-muted.

Screenshots: http-api-1440-light, http-api-1440-dark, http-api-390-light, cli-item-1440-light, stop-1440-light (before and after).
Uncertain: the 390 shot shows only one block; blocks with a long first line were not re-checked individually.
