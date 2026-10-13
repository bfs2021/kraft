# A file read from an add-on's store is checked against its digest when it is read

## Problem

The add-ons spec (The digest) says: "At each launch, `skill.read` checks the `SKILL.md` it reads against the manifest, so a store edited after the start is caught before its text reaches an agent." On main (f024b41) it does not:

- `skill._addon_path` and `skill.read` (`src/kraft/skill.py:115-173`) find `skills/<name>/SKILL.md` in the store and `read_text()` it.
- The store's `.kraft-digest` manifest (`addons/fetch.py:340-353`, written by `write_store` at `:359-392`) is used only at load. `load._why_left_out` (`addons/load.py:325-330`) checks that the manifest hashes to the store's name, and re-hashes every file only when `verify=True` (start, reload, doctor, `restore_missing` at start).
- A **pinned** store gets no check at all at launch: `load.for_item` (`load.py:431-463`) only asks `root.is_dir()`.
- Between those, the store's read-only file mode is the only guard. A worker, or anything running as the operator, can `chmod` and edit a file in `run/addons/store/`, and the next launch reads the edited text.

Every place that reads a store file after load, found by grepping `addon.root`, `addon_dirs`, `/ "skills"`, `profiles.yaml`, `library.yaml`, `CHAINS_DIR` and `extract_dir(`:

| Read | When | Reaches an agent |
|---|---|---|
| `skills/<n>/SKILL.md`: `skill.read` from `adapters/agent.py:224` (`resolve_invocation`) | every launch with an add-on `skill:` (dispatch, gate review, escalation, review reply, Settings preview, doctor) | yes: the method text |
| `profiles.yaml`: `templates/environment.py:582` `_addon_profiles` | **every launch**, for **every** add-on the item can see, live or pinned: `adapters/profiles.py:36` `harness_table(harnesses, pins)` → `load.for_item(pins)` → `HarnessProfileTable.from_yaml`. Also from `dispatch.py:1305` (fallback table), `policy.py:291`, `gate_review.py:101`, `escalate`, Settings and the Harnesses API | yes: model, effort, fallback list |
| `library.yaml` and `chains/*.yaml`: `templates/library.py:380` `_add_addon` | at load (start/reload, after `verify=True`), and **after load** when a running item's chain is revised: `templates/revision.py:384` `_pinned` → `library.with_addons(load.for_item(pins))` | yes: added nodes' prompts and steering are frozen into the item's snapshot |
| the whole store: `extract_dir(store)` at `addons/update.py:588` and `addons/repo_library.py:381` | an update or repo-library check, to diff the installed version against the candidate | indirectly: a store edited to look like the candidate hides the change from the reviewer |
| `.kraft/addon.json`: `load.py:333`, `load.py:649`, `api/config_check.py:685` | load, health, major-update listing | no: metadata only |

Two traps in the obvious fix:

1. **Candidates are not stores.** Five places lay an unaccepted add-on out in a scratch directory with no `.kraft-digest` and build a library and a profile table from it: `addons/update.py:611-615`, `addons/repo_library.py:399-403`, `addons/review.py:169-174`, `cli/addon.py:48-53` (`_lint`) and `cli/addon.py:98-103`. Making `_addon_profiles` (or `_add_addon`) demand a manifest without changing these breaks every install, update, review and `kraft admin addon validate`.
2. **The profile table is shared.** `harness_table` reads every visible add-on's `profiles.yaml`, so raising out of the table build for one edited add-on stops every launch on the instance, including launches that read nothing from it. That breaks `a-launch-stops-only-for-an-addon-it-reads` and `a-broken-addon-affects-only-itself`.

## Behaviour

1. **One reader.** Every read of a file from an add-on's or a repo library's store after the store is written goes through `fetch.open_store(root)`. It:
   - reads `.kraft-digest` (bounded) and checks that its SHA-256 equals the store directory's name, which is the digest the lock or the item's pin recorded;
   - parses the manifest exactly as `digest_manifest` writes it: one `path NUL mode NUL sha256-hex LF` line per file, sorted by the path's bytes;
   - `read(rel)` opens the file with `O_NOFOLLOW | O_NONBLOCK`, requires a regular file, reads at most the file's cap + 1 (`fetch._cap`), and returns the bytes only if their SHA-256 equals the file's manifest line. The bytes returned are the bytes hashed, so nothing can change in between (no check-then-reread);
   - `read(rel, optional=True)` returns `None` for a file the manifest does not list when nothing is at that path. A file at that path that the manifest does not list is refused (planted), and so is a listed file that is gone;
   - `listed(prefix)` gives the manifest's paths under a prefix, so `chains/` is enumerated from the manifest, not a glob.
2. **What a refusal says.** `fetch.StoreMismatch` (a subclass of `AddonRefused`) names the store-relative file and ends with `the store was changed after it was installed`:
   - `skills/deploy-review/SKILL.md does not match its digest; the store was changed after it was installed`;
   - `.kraft-digest does not hash to the store's name; ...`, `chains/x.yaml is not in its digest; ...`, `profiles.yaml is missing; ...`.
3. **A launch stops only for what it reads.**
   - **Skill.** `skill.read` reads through the store and raises `SkillError("skill: add-on 'release' could not be read: <StoreMismatch>")`. Dispatch already turns a `SkillError` into a `config` stop (`dispatch.py:1343`), as for a missing skill. `read` keeps its signature: `addon_dirs` maps namespace to root, so the message names the namespace, not the id and version. `validate` still checks presence only.
   - **Agent profiles.** `load.for_item` checks each add-on it returns that loads: it opens the store and reads `profiles.yaml` (optional). A refusal sets that add-on's `left_out` to the message. The table then leaves the add-on out, and `resolve_agent_task`'s existing check (`adapters/agent.py:363-371`) stops only a launch whose skill, profile or fallback names the namespace: `add-on release@acme 1.0.0 could not be read: profiles.yaml does not match its digest; the store was changed after it was installed`. A launch that reads nothing from it runs. `_addon_profiles` also reads through the store, so the bytes parsed are the bytes checked. A file edited between the two reads fails the table, which fails closed.
   - **Library and chains.** `TemplateLibrary._add_addon` reads `library.yaml` (optional) and each `chains/*.yaml` the manifest lists through the store. A refusal is a `TemplateLibraryError` that starts with the file's full path, so `_why_left_out` keeps attributing it to the add-on (`str(root) in str(exc)`), and a chain revision of a running item cannot resolve against edited text.
4. **`fetch.verify_store(root) -> Extracted`** is the whole-store check: the manifest check above, then `digest_manifest(extract_dir(root).files)` must equal `.kraft-digest`. It is used by:
   - `write_store`, before it reuses an existing `store/<digest>/` (`fetch.py:366`). A store that fails is **replaced**: the fresh copy is built in `staging/`, the old directory is made writable (macOS will not move a read-only directory to another parent) and renamed aside into `staging/`, the fresh one is renamed into place, and the old one is removed. A rename that loses a race to another writer is handled as today. Restoring an add-on, or installing the same content again, therefore repairs an edited store;
   - `load._why_left_out(verify=True)`, in place of its inline comparison. The `left_out` text stays `its files do not match the locked digest`;
   - the two review comparisons (`update.py:588`, `repo_library.py:381`), so an edited installed copy is reported as `could not be read to compare with`, never diffed.
5. **Candidates are laid out as stores.** `fetch.write_scratch(parent, extracted) -> Path` writes the files and `.kraft-digest` into `parent/<digest>/`, writable. `write_store` builds its staging copy with the same code. All five candidate sites use it, so a check of an add-on not yet installed reads through the same reader. `cli/addon.py` then maps messages back with `m.replace(str(store), str(root))`, since the scratch root is now a subdirectory of `tmp`.
6. **Cost.** No cache, and no whole-store hashing at launch. Per launch, for each add-on the item can see, Kraft hashes `.kraft-digest` and `profiles.yaml` (KBs) once per `for_item` call (two or three calls per launch), plus one `SKILL.md` (≤ 256 KiB) for a task with an add-on skill. `verify_store` runs only at start, reload, doctor and store writes, as `verify=True` already does.

## Out of scope

- `.kraft/addon.json` reads (load, health, `left_out_by`, config check): metadata that never reaches an agent, and its manifest-level check already happens at load.
- `update.referrers` (`update.py:202`): an install-time namespace check that already ignores a store that does not read.
- `gate_review.py:279` and `review_reply.py:148` do not catch `SkillError`. That is true today for a skill that does not load; this change adds one more way to raise it, and does not widen what those handlers catch.

## Where

- `src/kraft/addons/fetch.py`: `StoreMismatch`, `open_store` / `StoreFiles` (`read`, `listed`), `verify_store`, `write_scratch`, and `write_store` re-verifying and replacing. These sit next to `digest_manifest`.
- `src/kraft/skill.py`: `_addon_path` returns `(root, rel)`, `read` goes through `open_store`, and `validate` keeps its presence check. `fetch` is imported inside the function: `fetch` imports `kraft.config`, which imports `templates.environment`.
- `src/kraft/templates/environment.py:575-587` (`_addon_profiles`): read through the store.
- `src/kraft/templates/library.py:380-402` (`_add_addon`): read through the store, with chains enumerated from the manifest.
- `src/kraft/addons/load.py`: `for_item` checks the store at launch, and `_why_left_out` uses `verify_store`.
- `src/kraft/addons/update.py:588,611-615`, `src/kraft/addons/repo_library.py:381,399-403`, `src/kraft/addons/review.py:169-174`, `src/kraft/cli/addon.py:48-53,98-103`: `verify_store` and `write_scratch`.
- `tests/support/addons.py::installed`: lays the store out with `write_scratch`, so its root is `store/<digest>/` with a manifest. It gains a `files=` argument (path to raw text) for the rows that need a malformed file inside the digest.

## Requirements

Add to `docs/intent/kraft-addons.md`, after `an-addon-whose-digest-does-not-match-is-not-loaded`:

```
## REQ an-edited-store-file-is-never-read

IF a file the system reads from an add-on's or a repo library's store after the store was written does not match the digest the store was written with, THEN the system SHALL refuse the file, naming it, instead of reading its text.
enforced-by: tests/addons/test_fetch.py::test_a_store_file_is_read_only_if_it_matches_its_digest[edited-file-is-refused], tests/addons/test_fetch.py::test_a_store_file_is_read_only_if_it_matches_its_digest[edited-digest-manifest-is-refused], tests/addons/test_fetch.py::test_a_store_file_is_read_only_if_it_matches_its_digest[unlisted-file-is-refused], tests/test_skill.py::test_addon_skill_references[edited-store-is-refused], tests/test_skill.py::test_addon_skill_references[edited-digest-manifest-is-refused], tests/templates/test_environment.py::test_addon_profiles[edited-store-is-refused], tests/templates/test_library_addons.py::test_an_addon_error_names_the_store_file[edited-after-install], tests/addons/test_update.py::test_an_installed_copy_that_does_not_read_is_said_in_the_review[edited-but-valid], tests/addons/test_repo_library.py::test_a_change_is_reviewed_against_the_accepted_version[store-edited]
origin: src/kraft/addons/fetch.py §open_store

## REQ an-edited-store-is-replaced-not-reused

WHEN an add-on's store is written and a store with the same digest already exists, the system SHALL reuse it only if its files match the digest, and otherwise replace it with the files being written.
enforced-by: tests/addons/test_fetch.py::test_a_store_is_addressed_by_its_content[edited-store-is-rewritten], tests/addons/test_fetch.py::test_a_store_is_addressed_by_its_content[edited-digest-manifest-is-rewritten]
origin: src/kraft/addons/fetch.py §write_store
```

Extend `enforced-by:` of existing REQs:

- `a-launch-stops-only-for-an-addon-it-reads`: `tests/addons/test_pins.py::test_a_missing_pin_the_task_does_not_read_does_not_stop_it[edited-profiles-stop-its-profile]` and `[edited-profiles-spare-an-unrelated-task]`.

## Tests

Each change adds rows to an existing test where one covers the behaviour:

- `tests/addons/test_fetch.py::test_a_store_file_is_read_only_if_it_matches_its_digest` (**new**: the reader is a new behaviour). Rows: `unchanged-is-read`, `edited-file-is-refused`, `edited-digest-manifest-is-refused` (the `.kraft-digest` is rewritten to match the edit, so it no longer hashes to the directory name), `unlisted-file-is-refused`, `listed-file-gone-is-refused`, `optional-absent-is-none`, `symlink-is-refused`.
- `tests/addons/test_fetch.py::test_a_store_is_addressed_by_its_content`: parametrized with `unchanged-store-is-reused`, `edited-store-is-rewritten` and `edited-digest-manifest-is-rewritten`.
- `tests/test_skill.py::test_addon_skill_references`: gains a `tamper` column, the store from `support.addons.installed`, and rows `edited-store-is-refused` and `edited-digest-manifest-is-refused`.
- `tests/templates/test_environment.py::test_addon_profiles`: gains a `tamper` column and rows `edited-store-is-refused` and `edited-digest-manifest-is-refused`.
- `tests/templates/test_library_addons.py::test_an_addon_error_names_the_store_file`: its four rows pass their text through `installed(files=...)`, inside the digest. A new row, `edited-after-install`, edits a listed file after the store is written.
- `tests/addons/test_pins.py::test_a_missing_pin_the_task_does_not_read_does_not_stop_it`: gains a `damage` column (`gone` for the four existing rows, `edited-profiles` for the two new ones).
- `tests/addons/test_update.py::test_an_installed_copy_that_does_not_read_is_said_in_the_review`: row `edited-but-valid`, a valid `addon.json` that reads today. The file is at 794 of 800 lines.
- `tests/addons/test_repo_library.py::test_a_change_is_reviewed_against_the_accepted_version`: parametrized `unchanged` and `store-edited`. The `store-edited` row's `reach[0]` is `the accepted version's files could not be read to compare with`.
- **Mutation checks:** drop the hash comparison in `StoreFiles.read` (the read, skill, profile and library rows fail). Drop the name check on `.kraft-digest` (the `edited-digest-manifest` rows fail). Restore `if final.is_dir(): return final` (the `rewritten` rows fail). Drop the `for_item` check (`edited-profiles-stop-its-profile` fails). Make the table raise instead (`edited-profiles-spare-an-unrelated-task` fails). Swap `verify_store` back to `extract_dir` at either review site (its row fails).

## Docs

- `docsite/content/5.reference/03.configuration/12.addons.md`: under **The digest**, Kraft checks every file it reads from a store at launch (skills, agent profiles, and library and chains when a running item's chain is revised) against the manifest. An edited store stops only the launches that read it, and writing the same digest again replaces an edited store. In the load-checks list, keep "its files do not match the locked digest".
- `docsite/content/5.reference/03.configuration/13.repo-libraries.md` (**Work items, restore and the store**): the same check applies to a repo library's store.
- `docsite/content/6.project/1.security.md` (**Kraft add-ons**, the bullet at line 503): "A stored add-on whose files no longer match is not loaded" becomes "...is not loaded, and a file edited after the start is refused when it is read".
- `docsite/content/4.troubleshooting/2.stop-reasons-in-detail.md` (`add-on ... could not be read`): a new reason, `... does not match its digest; the store was changed after it was installed`. Remedy: find out what edited `run/addons/store/` (`kraft admin doctor` names the add-on). Delete that `store/<digest>/` directory (it is read-only, so run `chmod -R u+w` first), and the next launch restores the pinned version from its commit. Then run `kraft item retry ID`. `kraft admin addon install --re-install` repairs the store only while the collection still holds the same content, because it takes the newest commit.

## Decisions

- **Reader in `fetch.py`, imported lazily by its callers**: keeps the rule beside `digest_manifest`, as the spec asked. A new leaf module would move `DIGEST_FILE` and `digest_manifest` and the imports of every test that uses them.
- **`open_store` returns an object, plus a one-shot `read`**: `_add_addon` reads many chains from one store, and loading and hashing the manifest once per store, not once per file, keeps that cheap.
- **Membership comes from the manifest, not the disk**: a planted unlisted file is refused, a listed file that is gone is refused, and chains are enumerated from the manifest. An edit can neither add a file nor make one silently disappear.
- **`profiles.yaml` is checked in `for_item` and marks the add-on left out**: the table is built from every visible add-on, so one edited add-on must not stop unrelated launches (`a-launch-stops-only-for-an-addon-it-reads`). It reuses the existing stop path and its `add-on <id> <version> could not be read:` wording.
- **Skills are not checked in `for_item`**: only the skill a task names is read, so `skill.read` checks that one file. Hashing every `SKILL.md` per launch is the whole-store cost to avoid.
- **The skill message names the namespace, not the id and version**: `read`'s signature (namespace to root) stays, as the spec asked. The task path and namespace identify the add-on.
- **`validate` stays presence-only**: it runs during library builds at load and lint. Verifying there would change `_why_left_out(verify=False)`'s answer for an edited `SKILL.md` (pinned by `test_a_digest_mismatch_leaves_the_addon_out`), and launch is where the text is used.
- **`library.yaml` and `chains/` are in scope**: a chain revision of a running item re-reads them from the pinned store after load (`revision._pinned`), and the text reaches agents through the revised snapshot.
- **`write_store` replaces an edited store instead of refusing**: the bytes being written hash to the directory's name by construction, so replacing yields the correct store. Refusing would block re-install and restore until someone deleted the store by hand, and `gc` never removes a store that is still referenced.
- **An edited store at launch stops the launch rather than self-restoring**: an edit inside `run/` is a security signal for a human. The remedy, documented, is to delete the store directory, which the next launch restores.
- **Candidates get a real manifest via `write_scratch`, not a "skip verification" flag**: one code path for installed and candidate add-ons, and a forgotten flag can never turn verification off. It also replaces five copies of the same write loop.
- **Review comparisons use `verify_store`**: it costs one call, and it stops a store edited to match a malicious update from hiding that update's diff from the reviewer.
- **No cache of verified files**: the cache keyed on stat stamps is the gap being closed. The per-launch cost is a few small hashes.
- **The reader reuses `fetch.read_regular`** (`fetch.py:262`, already `O_NOFOLLOW | O_NONBLOCK`, regular files only, capped) and maps its `FetchError` to `StoreMismatch`: one bounded no-follow reader, not two.
- **`support.addons.installed` and `extracted` share one file-map builder**: `extracted()` already builds the same `{rel: (mode, bytes)}` map, so `installed()` reuses it instead of a second copy of the loop.
- **`tests/addons/test_update.py` (794/800) grows by exactly 3 lines**, a module constant that keeps the row's tuple on the existing one-line list. Item 4 adds nothing there (DECISIONS D11).
- **`_launch_problem` stays a separate function applied last in `for_item`**, so item 4 (merging after this) wraps `for_item` with `scoped(...)` before it and never hashes an out-of-scope store (DECISIONS D13).
- **Item 3's revision and gate tests are re-run after merging the integration branch**: they reach `_add_addon` and `for_item` through `revision._pinned`, which this item changes (DECISIONS D7, D8).
- **A `## Changelog` line under `release::none`, base and removals against the integration branch** (DECISIONS D8, D9).
