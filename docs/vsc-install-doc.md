# Kaye Engine: VS Code Install Algorithm

How a **payload** (what `generate_vs_code_payload` writes: `CLAUDE.md` and
the marketplace folder) lands in a user's existing `.claude/` folder, so
the plugins are registered and enabled with no manual step. One algorithm,
3 implementers; this file is the spec, the code follows it.

Verified on a real machine before this spec was written: with
`extraKnownMarketplaces` and `enabledPlugins` hand-written into
`~/.claude/settings.json` and VS Code restarted, the marketplace is listed
and its plugins are installed and enabled without a click.

## Implementers

All 3 follow the steps below and differ only in tooling:

| implementer | where | language | claude folder | payload from |
|---|---|---|---|---|
| **Engine command** | `kaye_engine/cli/claude/vs_code/place.py`, `place_vs_code_payload(payload_folder, claude_folder)`, run by `kaye-engine claude vs-code-extension` | Python | `CLAUDE_FOLDER` argument, default `~/.claude` | stage 1 output in a temp folder |
| **Windows installer** | `installer_templates/install.ps1`, run by `Install.cmd` | PowerShell | `%USERPROFILE%\.claude`, no override | `payload\` beside the script |
| **Linux installer** | `installer_templates/install.sh`, header of the `.run` file | bash plus `python3` | `$HOME/.claude`, no override | `payload/` extracted to a temp folder |

A change to any one of them goes through this doc first, then the other
two, then `tests/cli/github_release_parity_test.py`.

| step | engine (Python) | `install.ps1` | `install.sh` |
|---|---|---|---|
| 0 Locate | `Path.iterdir`, `json` | `Get-ChildItem`, `ConvertFrom-Json` | `find`, `python3 json` |
| 1 Preflight | `json.loads` | `ConvertFrom-Json` in `try` | `python3 json.load` |
| 2 `CLAUDE.md` | bytes compare, `shutil.copy2`, temp then `os.replace` | `Get-FileHash`, `Copy-Item`, `Move-Item -Force` | `cmp -s`, `cp -p`, `mv -f` |
| 3 Marketplace | `shutil.copytree`, `os.replace` | `Copy-Item -Recurse`, `Rename-Item` | `cp -a`, `mv` |
| 4 Settings | `json`, `os.replace` | `ConvertFrom-Json`, `ConvertTo-Json -Depth 20` | `python3 json` |
| 5 Report | `kamilog` deeds | `Write-Host` | `printf` |
| 6 Failure | `raise SystemExit(1)` | `exit 1` | `exit 1` |

JSON text is not byte-compared across implementers: key order is kept, but
indentation and escaping may differ (PowerShell serializes its own way).
The parity test compares the parsed settings.

## Terms

- `P`: the payload folder; holds `CLAUDE.md` and the marketplace folder
- `C`: the Claude folder, the install target
- `M`: the marketplace folder name, the one folder under `P` holding
  `.claude-plugin/marketplace.json`; it is also the marketplace name
- `NAME`: the `name` value inside that `marketplace.json`
- `PLUGINS`: the `name` of every entry of `plugins` in that
  `marketplace.json`
- `TS`: local time `YYYYMMDDHHMMSS`

No step names a consumer: marketplace and plugin names are read from the
payload at run time.

## Pseudocode

```text
place(P, C):

  # step 0: locate the marketplace
  candidates = every direct subfolder of P holding
               .claude-plugin/marketplace.json
  if len(candidates) != 1:           fail F1
  M = name of that folder

  # step 1: preflight, no write happens before every check passed
  if P/CLAUDE.md is not a file:      fail F2
  manifest = parse JSON of P/M/.claude-plugin/marketplace.json
             (invalid -> fail F3)
  NAME = manifest.name
  if NAME != M:                      fail F4
  PLUGINS = [p.name for p in manifest.plugins]
  if PLUGINS is empty or any name missing/not a string:  fail F5
  if C/settings.json exists:
      settings = parse JSON (invalid -> fail F6)
      if settings is not an object:                      fail F6
      for key in (extraKnownMarketplaces, enabledPlugins):
          if key exists and is not an object:            fail F6
  else:
      settings = {}
  create C if missing

  # step 2: CLAUDE.md
  if C/CLAUDE.md missing:
      write P/CLAUDE.md to C/CLAUDE.md                   -> "created"
  elif bytes(C/CLAUDE.md) == bytes(P/CLAUDE.md):         -> "unchanged"
  else:
      bak = C/CLAUDE.md.TS.bak
      while bak exists: append -2, -3, ... before .bak
      copy C/CLAUDE.md to bak                  # never deleted afterwards
      write P/CLAUDE.md to C/CLAUDE.md.tmp, then rename over C/CLAUDE.md
                                                         -> "replaced, backup bak"

  # step 3: marketplace swap through sibling temp names
  if C/M exists and its tree equals P/M (same relative files,
                                         same bytes):    -> "unchanged"
  else:
      tmp = C/M.new-RANDOM
      copy tree P/M to tmp
      if C/M exists:
          old = C/M.old-RANDOM
          rename C/M to old
          try rename tmp to C/M
          on error: rename old back to C/M, remove tmp, fail F7
          remove old
      else:
          rename tmp to C/M
      (any leftover tmp is removed on failure)           -> "created"/"replaced"

  # step 4: settings.json merge, key level, existing keys never changed
  added = []
  entry = {"source": {"source": "directory", "path": absolute(C/M)}}
  ekm = settings.extraKnownMarketplaces  (created as {} if absent)
  if NAME not in ekm:      ekm[NAME] = entry;  added += "marketplace NAME"
  else if ekm[NAME] != entry:  note "kept existing entry"   # never overwritten
  ep = settings.enabledPlugins  (created as {} if absent)
  for plugin in PLUGINS:
      key = plugin + "@" + NAME
      if key not in ep:    ep[key] = true;     added += key
      # a present key stays as is, an explicit false included
  if added is empty and settings.json exists:            -> "unchanged"
  else:
      write settings (UTF-8, no BOM, 2-space indent, trailing newline,
      other keys and their order untouched) to C/settings.json.tmp,
      then rename over C/settings.json                   -> "created"/"merged"

  # step 5: report
  one line per step: what was created, replaced, merged, or left unchanged
  if the settings merge kept an existing entry, say so
  last line: "restart VS Code; the plugins are enabled"

  exit 0
```

Order matters: step 1 validates everything, including the `settings.json`
JSON, before step 2 writes, so an invalid file aborts with nothing written.

## Failure Table

Any failure prints a plain one-line message naming the cause, then exits
non-zero (`1`). A `.bak` already written is never deleted.

| id | cause | writes already done |
|---|---|---|
| F1 | zero or several marketplace folders under `P` | none |
| F2 | `P/CLAUDE.md` missing | none |
| F3 | `marketplace.json` missing keys or invalid JSON | none |
| F4 | `NAME` differs from the folder name `M` | none |
| F5 | no plugins listed, or a plugin without a string `name` | none |
| F6 | `C/settings.json` invalid JSON, not an object, or `extraKnownMarketplaces` / `enabledPlugins` not an object | none |
| F7 | a copy or rename failed in steps 2 to 4 | earlier steps stay; step 3 restores the old marketplace folder; no half-written file is left (temp names only) |
| F8 | `python3` absent (Linux installer only) | none: checked before step 0 |

## Idempotence

A second run over an unchanged payload reports `unchanged` for steps 2, 3,
and 4, writes nothing, and creates no new `.bak`. A changed `CLAUDE.md`
makes a new `.bak` each run; the older ones stay. A plugin the user set to
`false` in `enabledPlugins` stays `false`: the merge only adds missing keys.

## Where the Engine Differs

- The engine reads `P` from a temp folder its own stage 1 filled; the
  installers read the shipped `payload/`.
- The engine honors `--dry-run`: steps 0 and 1 run for real, steps 2 to 4
  report the verdict they would give and write nothing under `C`.
- Only the engine takes a `CLAUDE_FOLDER`; the installers read none.

## What the Tests Assert

Every step above has a test in `tests/cli/claude/vs_code_place_test.py`
(engine), `tests/cli/github_release_installer_linux_test.py` (`install.sh`
under a temp `HOME`), and `tests/cli/github_release_parity_test.py` (both
routes over one payload, parsed settings compared). `install.ps1` has no
automated run on Linux: its test only checks the shipped bytes, and Windows
behavior is verified by hand once per release.
