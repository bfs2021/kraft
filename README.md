# Screenshots for the final `kraft console` PR

Images only, never merged. The PR body embeds them by raw URL. Taken from a dev instance (`kraft/console` at 4bcbcfab3), dark theme unless named otherwise, console shots at 2x.

## console/ (Textual's own renderer)

At 120x40:

- `board-peek-gate.png`: the Board with a gate item selected and its spec in the peek
- `item-overview-gate.png`: an item's Overview at a spec gate
- `item-question.png`: an item where the agent asks a question
- `item-activity.png`: the Activity tab
- `item-log.png`: the Log tab
- `item-diff.png`: the Diff tab
- `item-menu.png`: the `m` menu on a failed item
- `reject-dialog.png`: rejecting a gate, with a note and the node to go back to
- `server.png`: the Server screen
- `repos.png`: the Repos screen
- `addons.png`: the Add-ons screen, with a directory collection
- `help.png`: the `?` key list
- `output-panel.png`: `/view list` in the output panel
- `confirm.png`: `/admin restart`'s confirm, listing the running items (answered Back)
- `since-line-120x40.png`: the "since HH:MM" line after reopening with a change in between
- `board-light-120x40.png`: the Board in the light theme

At other sizes:

- `board-80x24.png`: the Board at 80x24
- `new-item-80x24.png`: the New item form at 80x24
- `repos-connect-80x24.png`: the Connect form at 80x24
- `narrow-60x16.png`: the Board at 60x16
- `board-empty-80x24.png`: the Board when nothing needs you

## web/ (same seeded server, frontend swapped between runs)

- `before/board.png`, `before/board-phone.png`, `before/item-failed.png`: origin/main's frontend (33996aa9a, the merge base)
- `after/board.png`, `after/board-phone.png`, `after/item-failed.png`: this branch's frontend

1440x700 for `board` and `item-failed`, 390x844 for `board-phone`.
