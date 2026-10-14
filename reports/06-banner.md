# 06-banner

PR: https://github.com/itsOmidKarami/kraft/pull/764 (branch kraft/docs-banner, base kraft/docs-design, label release::none)

## Summary
The /next/ banner was a saturated amber slab (48px, 56px on a phone) on every page, while the real version switch was muted plain text. The banner is now a ~32px neutral strip (elevated surface, border, small amber left mark): "Docs for unreleased main · Switch to v2.0.0 docs →", same-page link kept. The header switch is a bordered two-part pill (current docs filled, other version a link) with an aria-label saying what it does.

## Decisions
- Banner text is the default text color on bg-elevated: AA in both modes, and the old "dark text in both modes" property is kept by not using amber text.
- Amber appears only as a 4px mark in the banner and as the filled "next" segment of the header pill (warning-900 on warning-100; warning-200 on warning-950 in dark).
- Header pill is a segmented toggle, not a single link: the current side is a span with aria-current, the other side is the link. Text uses default, not muted (muted on elevated is 4.35:1).
- aria-labels: "Switch to the v2.0.0 docs" (next) and "Switch to the docs for unreleased main" (stable); falls back to "release" when no stable version is configured.
- Banner wraps instead of truncating; at 390px it fits on one line (~32px).
- Stable has no banner; its pill reads `v2.0.0 | next`.

## Checks
- check_docs_coverage / walls / redirects / landings / shell: all ok.
- nuxt generate, next and stable channels: exit 0.
- Contrast was judged from the token choices and the screenshots, not measured with a tool.

## Screenshots
06-banner/{before,after}/: install-1440-light, install-1440-dark, install-390-light, stable-header-1440-light (all .png).

## Skipped / uncertain
- Did not run a contrast tool; hover state of the pill not screenshotted.
- The stable dev server needed NUXT_IGNORE_LOCK=1 to run beside the next one.
