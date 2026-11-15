#!/usr/bin/env bash
# install.sh: put the Claude Code prompt structure into $HOME/.claude and
# enable its plugins in VS Code. Self-extracting: this header is followed by
# a tar.gz of payload/. Follows docs/installer-algorithm-doc.md (Claude VS
# Code Plugin); takes no argument and reads no setting. Run: bash NAME.run

set -eu

fail() {
    echo "ERROR: $*" >&2
    exit 1
}

# the JSON work of steps 1 and 4: "check" validates every input, "merge"
# adds the missing settings.json keys
read -r -d '' PY <<'PYTHON' || true
import json
import os
import sys
import uuid

mode, manifest_path, market, settings_path, market_folder = sys.argv[1:6]


def fail(message):
    print("ERROR: " + message, file=sys.stderr)
    sys.exit(1)


def load(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError) as err:
        fail("{} is not valid JSON: {}".format(path, err))


manifest = load(manifest_path)
name = manifest.get("name") if isinstance(manifest, dict) else None
plugins = manifest.get("plugins") if isinstance(manifest, dict) else None
if not isinstance(name, str) or not isinstance(plugins, list):
    fail("{} lacks a name or a plugins list".format(manifest_path))
if name != market:
    fail("marketplace name differs from its folder name")
names = [p.get("name") if isinstance(p, dict) else None for p in plugins]
if not names or not all(isinstance(n, str) and n for n in names):
    fail("marketplace lists no plugin, or one has no name")

settings = load(settings_path) if os.path.isfile(settings_path) else {}
if not isinstance(settings, dict) or not all(
    isinstance(settings.get(key, {}), dict)
    for key in ("extraKnownMarketplaces", "enabledPlugins")
):
    fail("settings.json has a key of the wrong type")
if mode == "check":
    sys.exit(0)

entry = {
    "source": {"source": "directory", "path": os.path.realpath(market_folder)}
}
added = []
known = settings.setdefault("extraKnownMarketplaces", {})
if name not in known:
    known[name] = entry
    added.append("marketplace " + name)
elif known[name] != entry:
    print("settings.json: kept existing marketplace " + name)
enabled = settings.setdefault("enabledPlugins", {})
for plugin in names:
    key = plugin + "@" + name
    if key not in enabled:  # an existing key stays, a false included
        enabled[key] = True
        added.append(key)
if not added:
    print("settings.json: unchanged")
    sys.exit(0)
data = json.dumps(settings, indent=2, ensure_ascii=False) + "\n"
tmp = "{}.tmp-{}".format(settings_path, uuid.uuid4().hex[:8])
try:
    with open(tmp, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(data)
    os.replace(tmp, settings_path)
except OSError as err:
    if os.path.exists(tmp):
        os.unlink(tmp)
    fail("could not write {}: {}".format(settings_path, err))
print("settings.json: added " + ", ".join(added))
PYTHON

place() {
    P=$1
    C=$2

    # 0 locate
    count=0
    M=
    for dir in "$P"/*/; do
        if [ -f "${dir}.claude-plugin/marketplace.json" ]; then
            count=$((count + 1))
            M=$(basename "$dir")
        fi
    done
    [ "$count" -eq 1 ] || fail "expected exactly 1 marketplace folder in payload"

    # 1 preflight: no write before every check passes
    [ -f "$P/CLAUDE.md" ] || fail "payload has no CLAUDE.md"
    python3 -c "$PY" check "$P/$M/.claude-plugin/marketplace.json" "$M" \
        "$C/settings.json" "$C/$M" || exit 1
    mkdir -p "$C"

    # 2 CLAUDE.md
    if [ ! -e "$C/CLAUDE.md" ]; then
        cp "$P/CLAUDE.md" "$C/CLAUDE.md"
        echo "CLAUDE.md: created"
    elif ! cmp -s "$C/CLAUDE.md" "$P/CLAUDE.md"; then
        stamp=$(date +%Y%m%d%H%M%S)
        bak="$C/CLAUDE.md.$stamp.bak"
        n=1
        while [ -e "$bak" ]; do
            n=$((n + 1))
            bak="$C/CLAUDE.md.$stamp-$n.bak"
        done
        cp -p "$C/CLAUDE.md" "$bak"
        t="$C/CLAUDE.md.tmp-$$"
        cp "$P/CLAUDE.md" "$t"
        mv -f "$t" "$C/CLAUDE.md"
        echo "CLAUDE.md: replaced, backup $(basename "$bak")"
    else
        echo "CLAUDE.md: unchanged"
    fi

    # 3 marketplace swap
    if [ -d "$C/$M" ] && diff -r "$P/$M" "$C/$M" > /dev/null 2>&1; then
        echo "$M/: unchanged"
    else
        token="$$-$RANDOM"
        new="$C/$M.new-$token"
        old="$C/$M.old-$token"
        cp -a "$P/$M" "$new" || {
            rm -rf "$new"
            fail "could not replace marketplace folder"
        }
        if [ -e "$C/$M" ]; then
            mv "$C/$M" "$old" || {
                rm -rf "$new"
                fail "could not replace marketplace folder"
            }
        fi
        if ! mv "$new" "$C/$M"; then
            [ ! -e "$old" ] || mv "$old" "$C/$M"
            rm -rf "$new"
            fail "could not replace marketplace folder"
        fi
        rm -rf "$old"
        echo "$M/: replaced"
    fi

    # 4 settings.json: add missing keys only, never change an existing one
    python3 -c "$PY" merge "$P/$M/.claude-plugin/marketplace.json" "$M" \
        "$C/settings.json" "$C/$M" || exit 1

    # 5 done
    echo "restart VS Code"
}

main() {
    [ "$#" -eq 0 ] || fail "takes no argument"
    command -v python3 > /dev/null 2>&1 || fail "python3 is required"
    [ -n "${HOME:-}" ] || fail "HOME is not set"
    tmp=$(mktemp -d) || fail "could not create a temp folder"
    trap 'rm -rf "$tmp"' EXIT
    start=$(awk '/^# __PAYLOAD_BELOW__$/ { print NR + 1; exit }' "$0")
    tail -n +"$start" "$0" | tar -xzf - --no-same-owner -C "$tmp" \
        || fail "could not unpack the payload"
    place "$tmp/payload" "$HOME/.claude"
}

main "$@"
exit $?
# __PAYLOAD_BELOW__
