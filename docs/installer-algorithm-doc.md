# Kaye Engine: Installer Algorithm

One spec per install target: every implementer of a target follows it and
differs only in tooling. A change goes through this doc first, then each
implementer, then the parity test. Targets so far: [Claude VS Code
Plugin](#claude-vs-code-plugin).

## Claude VS Code Plugin

Places a **payload** (`CLAUDE.md` plus the marketplace folder, from
`generate_vs_code_payload`) into an existing `.claude/` folder, registering
the marketplace and enabling its plugins with no manual step. Checked by
hand: with both `settings.json` keys written and VS Code restarted, the
plugins show installed and enabled.

### Implementers

| implementer | claude folder | payload from |
|---|---|---|
| `place_vs_code_payload` (`vs_code/place.py`, run by `claude vs-code-extension`; Python) | `CLAUDE_FOLDER`, default `~/.claude` | stage 1 output in a temp folder |
| `install.ps1` (Windows installer; PowerShell) | `%USERPROFILE%\.claude` | `payload\` beside the script |
| `install.sh` (Linux installer; bash and `python3`) | `$HOME/.claude` | `payload/` extracted to a temp folder |

Settings JSON is compared parsed, never as bytes: key order is kept, but
indentation and escaping may differ (PowerShell serializes its own way).

### Terms

- `P` payload folder, `C` Claude folder
- `M` the one folder under `P` holding `.claude-plugin/marketplace.json`;
  `NAME` the `name` inside it; `PLUGINS` every `plugins[].name`
- `TS` local time `YYYYMMDDHHMMSS`

Nothing names a consumer: all names come from the payload at run time.

### Steps

```text
place(P, C):

  # 0 locate
  M = the single marketplace folder under P         (else F1)

  # 1 preflight: no write before every check passes
  P/CLAUDE.md must exist                            (else F2)
  parse P/M/.claude-plugin/marketplace.json         (else F3)
  NAME == M                                         (else F4)
  PLUGINS non-empty, each a string                  (else F5)
  settings = parse C/settings.json, or {} if absent
  settings, extraKnownMarketplaces, enabledPlugins
      must be objects when present                  (else F6)
  create C if missing

  # 2 CLAUDE.md
  absent:                    write
  identical bytes:           leave
  differs:                   copy to CLAUDE.md.TS.bak (add -2, -3 on a
                             name clash), then replace via temp + rename

  # 3 marketplace swap
  C/M tree equals P/M tree:  leave
  else: copy P/M to sibling C/M.new-RANDOM, rename old C/M aside,
        rename new into place, delete old;
        on error restore old, remove temp                (F7)

  # 4 settings.json: add missing keys only, never change an existing one
  extraKnownMarketplaces[NAME] = {source: {source: directory,
                                           path: absolute(C/M)}}
  enabledPlugins[plugin@NAME] = true   for each plugin
      (an existing key stays, an explicit false included)
  nothing added: leave the file; else write via temp + rename
      (UTF-8, no BOM, 2-space indent, other keys and order untouched)

  # 5 report
  per step: created, replaced, merged, or unchanged; note an existing
  marketplace entry kept; last line "restart VS Code"
```

### Failures

A failure prints one plain line and exits `1`; a `.bak` is never deleted.

| id | cause | written before |
|---|---|---|
| F1 | zero or several marketplace folders | none |
| F2 | `CLAUDE.md` missing in `P` | none |
| F3 | `marketplace.json` invalid or missing keys | none |
| F4 | `NAME` differs from folder name | none |
| F5 | no plugins, or a nameless one | none |
| F6 | `settings.json` invalid, or a key of the wrong type | none |
| F7 | a copy or rename failed | earlier steps stay; step 3 restores the old folder |
| F8 | `python3` absent (`install.sh` only, checked first) | none |

### Idempotence and Differences

A second run over the same payload reports `unchanged` throughout, writes
nothing, and makes no `.bak`. A changed `CLAUDE.md` makes a new `.bak`
each run. The engine alone honors `--dry-run` (steps 2 to 4 report their
verdict, write nothing) and takes `CLAUDE_FOLDER`.

### Tests

`tests/cli/claude/vs_code_place_test.py` (engine),
`github_release_installer_linux_test.py` (`install.sh` under a temp `HOME`),
`github_release_parity_test.py` (both routes, one payload). `install.ps1`
has only a shipped-bytes test; Windows is checked by hand once per release.
