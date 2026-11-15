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
| `place-payload-into-claude-folder.ps1` (Windows installer, run by `install.cmd` from `src\`; PowerShell) | `%USERPROFILE%\.claude` | `payload\` beside `src\` |
| `install.sh` (Linux installer; bash and `python3`) | `$HOME/.claude` | `payload/` extracted to a temp folder |

`install.sh` stops first, with a plain message, when `python3` is absent.
Settings JSON is compared parsed, never as bytes: key order is kept, but
indentation and escaping may differ (PowerShell serializes its own way).

### Pseudo Code

Nothing names a consumer: all names come from the payload at run time.

```python
def place(P, C):
    # P: payload folder, holds CLAUDE.md and the marketplace folder
    # C: Claude folder, the install target (e.g. ~/.claude)

    # 0 locate
    folders = [d for d in P.iterdir()
               if (d / ".claude-plugin/marketplace.json").is_file()]
    if len(folders) != 1:
        raise SystemExit("expected exactly 1 marketplace folder in payload")
    M = folders[0].name  # marketplace folder name

    # 1 preflight: no write before every check passes
    if not (P / "CLAUDE.md").is_file():
        raise SystemExit("payload has no CLAUDE.md")
    manifest = load_json(P / M / ".claude-plugin/marketplace.json")
    # load_json raises SystemExit("... is not valid JSON") on bad JSON
    NAME = manifest["name"]  # marketplace name, keys settings.json
    if NAME != M:
        raise SystemExit("marketplace name differs from its folder name")
    PLUGINS = [p["name"] for p in manifest["plugins"]]  # every plugin
    if not PLUGINS or not all(isinstance(n, str) for n in PLUGINS):
        raise SystemExit("marketplace lists no plugin, or one has no name")
    settings = load_json(C / "settings.json") if exists else {}
    if not is_dict(settings) or not all(
        is_dict(settings.get(k, {}))
        for k in ("extraKnownMarketplaces", "enabledPlugins")
    ):
        # an unreadable settings.json is never overwritten
        raise SystemExit("settings.json has a key of the wrong type")
    C.mkdir(exist_ok=True)

    # 2 CLAUDE.md
    new, old = P / "CLAUDE.md", C / "CLAUDE.md"
    if not old.exists():
        write(old, new.read_bytes())
        print("CLAUDE.md: created")
    elif old.read_bytes() != new.read_bytes():
        bak = unique(C / f"CLAUDE.md.{TS}.bak")  # TS: local YYYYMMDDHHMMSS
        # unique() adds -2, -3 on a name clash
        copy(old, bak)
        replace_via_temp(old, new.read_bytes())
        print(f"CLAUDE.md: replaced, backup {bak.name}")
    else:
        print("CLAUDE.md: unchanged")

    # 3 marketplace swap
    if (C / M).exists() and same_tree(C / M, P / M):
        print(f"{M}/: unchanged")
    else:
        tmp = C / f"{M}.new-{RANDOM}"  # sibling temp name
        copy_tree(P / M, tmp)
        try:
            swap_in(tmp, C / M)  # old folder renamed aside, deleted after
        except OSError:
            restore_old(C / M)  # old folder renamed back, temp removed
            raise SystemExit("could not replace marketplace folder")
        print(f"{M}/: replaced")

    # 4 settings.json: add missing keys only, never change an existing one
    entry = {"source": {"source": "directory",
                        "path": str((C / M).resolve())}}
    added = []
    ekm = settings.setdefault("extraKnownMarketplaces", {})
    if NAME not in ekm:
        ekm[NAME] = entry
        added.append(f"marketplace {NAME}")
    elif ekm[NAME] != entry:
        print(f"settings.json: kept existing marketplace {NAME}")
    ep = settings.setdefault("enabledPlugins", {})
    for plugin in PLUGINS:
        key = f"{plugin}@{NAME}"
        if key not in ep:  # an existing key stays, an explicit False too
            ep[key] = True
            added.append(key)
    if added:
        replace_via_temp(C / "settings.json", dump_json(settings))
        # UTF-8, no BOM, indent=2, trailing newline, key order kept
        print("settings.json: added " + ", ".join(added))
    else:
        print("settings.json: unchanged")

    # 5 done
    print("restart VS Code")
```

### Idempotence and Differences

A second run over the same payload reports `unchanged` throughout, writes
nothing, and makes no `.bak`. A changed `CLAUDE.md` makes a new `.bak`
each run. The engine alone honors `--dry-run` (steps 2 to 4 report their
verdict, write nothing) and takes `CLAUDE_FOLDER`.
