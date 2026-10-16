# Screenshots for the console workbench PR

Images only, never merged. Taken from a dev instance of `kraft/console-workbench` at 6a1d8ae73 (main at 9d4a5863f plus the keys fix and the workbench redesign, after review fixes), dark theme unless named otherwise, console shots at 2x from Textual's own renderer. Two items were running while these were taken, so the spinners and clocks show.

## console/

- `board-120x40.png`: the Board with running rows mid-spin and the peek on a running item
- `board-80x24.png`: the Board at 80x24
- `narrow-60x16.png`: the Board at 60x16
- `board-light-120x40.png`: the Board in the light theme
- `item-running-log-120x40.png`: a running item's Log tab, with `Running` and the working line under it
- `item-gate-overview-120x40.png`: an item's Overview at a spec gate
- `item-activity-120x40.png`: the Activity tab, reached with the right arrow from Overview
- `server-120x40.png`: the Server screen
- `repos-120x40.png`: the Repos screen
- `addons-120x40.png`: the Add-ons screen with a directory collection
- `help-120x40.png`: the `?` key list
- `confirm-120x40.png`: `/admin restart`'s confirm, Back focused, never confirmed
- `prompt-focused-120x40.png`: the prompt focused, its footer reading previous, complete, leave

## web/

Same seeded server, frontend swapped between runs. The branch changes no frontend file, so the two bundles are identical.

- `before/board.png`, `before/board-phone.png`, `before/item-failed.png`: origin/main's frontend (9d4a5863f)
- `after/board.png`, `after/board-phone.png`, `after/item-failed.png`: this branch's frontend

1440x700 for `board` and `item-failed`, 390x844 for `board-phone`.
