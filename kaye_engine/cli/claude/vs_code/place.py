"""
place.py

define ``place_vs_code_payload`` -- stage 2 of the VS Code extension
export: merge a payload into an existing Claude folder, register its
marketplace and enable its plugins; follows
``docs/installer-algorithm-doc.md``, as do
``place-payload-into-claude-folder.ps1`` and ``install.sh``
"""

import json
import logging
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path

import kamilog
from kaye_engine.badge import NEW_BADGE, OWR_BADGE, DEL_BADGE, UNDO_BADGE
from kaye_engine.cli.claude import LOGGER_CLAUDE_NAME
from kaye_engine.cli.dry_run import is_dry_run
from kaye_engine.deed import track

__all__ = ("place_vs_code_payload",)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CLAUDE_NAME)

# constants  ###################################################################
_MARKETPLACE_JSON = Path(".claude-plugin") / "marketplace.json"
_SETTINGS_KEYS = ("extraKnownMarketplaces", "enabledPlugins")


# Public API  ##################################################################
def place_vs_code_payload(payload_folder, claude_folder):
    """
    merge the payload into the Claude folder, idempotently

    backs up a differing ``CLAUDE.md`` to ``CLAUDE.md.TS.bak`` then
    replaces it, swaps the marketplace folder in through a sibling temp
    name, and adds the marketplace and its plugins to ``settings.json``
    (``extraKnownMarketplaces``, ``enabledPlugins``), never changing a key
    already there; every input is checked before the first write; under a
    dry run the same verdicts are reported and nothing is written


    :param payload_folder: folder holding ``CLAUDE.md`` and one marketplace
            folder, see :func:`generate_vs_code_payload`
    :type payload_folder: Path-like
    :param claude_folder: the ``.claude/`` folder to install into
    :type claude_folder: Path-like
    :raises SystemExit: exit code 1, when a check or a step fails
    :return: path to the installed marketplace.json
    :rtype: Path
    """
    payload = Path(payload_folder)
    claude = Path(claude_folder)

    # 0 locate, 1 preflight: nothing is written before every check passed
    logger.enter("preflight: check payload and settings, write nothing")
    folders = [
        d for d in sorted(payload.iterdir())
        if (d / _MARKETPLACE_JSON).is_file()
    ] if payload.is_dir() else []
    if len(folders) != 1:
        _fail("expected exactly 1 marketplace folder in payload")
    market = folders[0].name
    logger.debug("pass: 1 marketplace folder in payload: " + market)
    if not (payload / "CLAUDE.md").is_file():
        _fail("payload has no CLAUDE.md")
    logger.debug("pass: payload has CLAUDE.md")
    name, plugins = _read_manifest(folders[0] / _MARKETPLACE_JSON, market)
    logger.debug(
        "pass: marketplace {} lists {} plugin(s)".format(name, len(plugins))
    )
    settings_path = claude / "settings.json"
    settings = _read_settings(settings_path)
    logger.debug(
        "pass: settings.json {}".format(
            "readable" if settings_path.exists() else "absent, starts empty"
        )
    )

    if not claude.is_dir():
        with track(logger).create_dir(claude):
            if not is_dry_run():
                claude.mkdir(parents=True)

    logger.enter("merge CLAUDE.md")
    _place_prompt(payload / "CLAUDE.md", claude / "CLAUDE.md")
    logger.enter("swap marketplace folder " + market)
    _place_marketplace(payload / market, claude / market)
    logger.enter("merge settings.json")
    _merge_settings(settings_path, settings, name, plugins, claude / market)

    return claude / market / _MARKETPLACE_JSON


# Auxiliaries  #################################################################
def _fail(message):
    logger.critical(message)
    raise SystemExit(1)


def _load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        _fail("{} is not valid JSON: {}".format(path, err))


def _read_manifest(path, market):
    """
    :return: the marketplace name and the names of its plugins
    :rtype: tuple[str, list[str]]
    """
    manifest = _load_json(path)
    name = manifest.get("name") if isinstance(manifest, dict) else None
    plugins = manifest.get("plugins") if isinstance(manifest, dict) else None
    if not isinstance(name, str) or not isinstance(plugins, list):
        _fail("{} lacks a name or a plugins list".format(path))
    if name != market:
        _fail("marketplace name differs from its folder name")
    names = [p.get("name") if isinstance(p, dict) else None for p in plugins]
    if not names or not all(isinstance(n, str) and n for n in names):
        _fail("marketplace lists no plugin, or one has no name")
    return name, names


def _read_settings(path):
    if not path.exists():
        return {}
    settings = _load_json(path)
    if not isinstance(settings, dict) or not all(
        isinstance(settings.get(key, {}), dict) for key in _SETTINGS_KEYS
    ):
        _fail("settings.json has a key of the wrong type")
    return settings


def _replace_via_temp(path, data):
    """
    write ``data`` (bytes) to a sibling temp file, then rename it over
    ``path``; both steps are logged, and skipped under a dry run
    """
    tmp = path.with_name("{}.tmp-{}".format(path.name, uuid.uuid4().hex[:8]))
    try:
        with track(logger).create_tmp(tmp):
            if not is_dry_run():
                tmp.write_bytes(data)
        with track(logger).mv_file(tmp, path) as moved:
            moved.level = logging.DEBUG
            if not is_dry_run():
                os.replace(tmp, path)
    except OSError as err:
        tmp.unlink(missing_ok=True)
        _fail("could not write {}: {}".format(path, err))


def _unique_backup(claude_md):
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    bak = claude_md.with_name("{}.{}.bak".format(claude_md.name, stamp))
    count = 1
    while bak.exists():
        count += 1
        bak = claude_md.with_name(
            "{}.{}-{}.bak".format(claude_md.name, stamp, count)
        )
    return bak


def _place_prompt(src, dest):
    data = src.read_bytes()
    if not dest.exists():
        with track(logger).create_file(dest):
            _replace_via_temp(dest, data)
        return
    if dest.read_bytes() == data:
        logger.skip("unchanged " + str(dest))
        return

    bak = _unique_backup(dest)
    with track(logger).cp_file(dest, bak):
        if not is_dry_run():
            shutil.copy2(dest, bak)
    with track(logger).owr_file(dest):
        _replace_via_temp(dest, data)


def _tree_files(root):
    return sorted(p.relative_to(root) for p in root.rglob("*") if p.is_file())


def _diff_trees(src, dest):
    """
    :return: files the swap adds, changes and removes, as three sorted lists
            of paths relative to the tree root; read-only
    :rtype: tuple[list[Path], list[Path], list[Path]]
    """
    new = _tree_files(src)
    old = _tree_files(dest) if dest.exists() else []
    added = [f for f in new if f not in old]
    removed = [f for f in old if f not in new]
    changed = [
        f for f in new
        if f in old and (src / f).read_bytes() != (dest / f).read_bytes()
    ]
    return added, changed, removed


def _log_tree_diff(market, added, changed, removed):
    """
    log one ``DEBUG`` line per file the swap touches, then a count line
    """
    for rel in added:
        logger.debug("add " + rel.as_posix(), badges=NEW_BADGE)
    for rel in changed:
        logger.debug("change " + rel.as_posix(), badges=OWR_BADGE)
    for rel in removed:
        logger.debug("remove " + rel.as_posix(), badges=DEL_BADGE)
    logger.debug(
        "{}: {} added, {} changed, {} removed".format(
            market, len(added), len(changed), len(removed)
        )
    )


def _place_marketplace(src, dest):
    added, changed, removed = _diff_trees(src, dest)
    if dest.exists() and not (added or changed or removed):
        logger.skip("unchanged " + str(dest))
        return

    _log_tree_diff(dest.name, added, changed, removed)
    deed = track(logger).owr_file if dest.exists() else track(logger).create_dir
    with deed(dest):
        _swap_in(src, dest)


def _swap_in(src, dest):
    """
    copy ``src`` to a sibling temp folder, move any old ``dest`` aside,
    rename the copy into place, delete the old; on an error the old folder
    comes back and the temp folder goes; every step is logged, and skipped
    under a dry run
    """
    token = uuid.uuid4().hex[:8]
    tmp = dest.with_name("{}.new-{}".format(dest.name, token))
    old = dest.with_name("{}.old-{}".format(dest.name, token))
    had_old = dest.exists()
    try:
        with track(logger).create_tmp(tmp):
            if not is_dry_run():
                shutil.copytree(src, tmp)
        if had_old:
            with track(logger).mv_file(dest, old) as aside:
                aside.level = logging.DEBUG
                if not is_dry_run():
                    os.replace(dest, old)
        try:
            with track(logger).mv_file(tmp, dest) as placed:
                placed.level = logging.DEBUG
                if not is_dry_run():
                    os.replace(tmp, dest)
        except OSError:
            if had_old and not is_dry_run() and old.exists():
                os.replace(old, dest)
                logger.caution(
                    "restore old marketplace folder: {} -> {}".format(
                        old, dest
                    ),
                    badges=UNDO_BADGE,
                )
            raise
    except OSError as err:
        if not is_dry_run():
            shutil.rmtree(tmp, ignore_errors=True)
        _fail("could not replace marketplace folder: {}".format(err))
    if had_old:
        with track(logger).del_dir(old) as dropped:
            dropped.level = logging.DEBUG
            if not is_dry_run():
                shutil.rmtree(old, ignore_errors=True)


def _merge_settings(path, settings, name, plugins, market_folder):
    entry = {
        "source": {
            "source": "directory",
            "path": str(market_folder.resolve()),
        }
    }
    added = []
    known = settings.setdefault("extraKnownMarketplaces", {})
    if name not in known:
        known[name] = entry
        added.append("marketplace " + name)
    elif known[name] != entry:
        logger.warning(
            "settings.json: kept existing marketplace {}".format(name)
        )
    else:
        logger.skip("keep marketplace {}: already registered".format(name))

    enabled = settings.setdefault("enabledPlugins", {})
    for plugin in plugins:
        key = "{}@{}".format(plugin, name)
        if key not in enabled:  # an existing key stays, a False included
            enabled[key] = True
            added.append(key)
        else:
            logger.skip("keep {}: already {}".format(key, enabled[key]))

    if not added:
        logger.skip("unchanged " + str(path))
        return

    for item in added:
        logger.info("add {} to settings.json".format(item), badges=NEW_BADGE)
    data = (json.dumps(settings, indent=2, ensure_ascii=False) + "\n").encode(
        "utf-8"
    )
    with track(logger).save_config(path):
        _replace_via_temp(path, data)
