"""
json_file.py

define ``write_json_file`` -- write one manifest as indented JSON, its
folder created first; every write is a deed, and a dry run touches nothing
"""

import json
from pathlib import Path

from kaye_engine.cli.dry_run import is_dry_run
from kaye_engine.cli.file_write import write_text_if_changed
from kaye_engine.deed import track

__all__ = ("write_json_file",)


def write_json_file(logger, path, data):
    """
    write ``data`` to ``path`` as 2-space indented JSON plus a newline,
    skipping an identical rewrite


    :param logger: logger every deed reports through
    :type logger: kamilog.Logger
    :param path: file to write
    :type path: Path-like
    :param data: JSON-serializable object
    :type data: dict
    :raises SystemExit: exit code 1, when the file cannot be written
    """
    path = Path(path)
    try:
        if not path.parent.is_dir():
            with track(logger).create_dir(path.parent):
                if not is_dry_run():
                    path.parent.mkdir(parents=True, exist_ok=True)
        write_text_if_changed(logger, path, json.dumps(data, indent=2) + "\n")
    except OSError as err:
        logger.critical("cannot write:\t" + str(path))
        raise SystemExit(1) from err
