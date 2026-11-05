"""
file_write.py

define ``write_text_if_changed`` -- the one place a command writes a text
file that may already exist: identical content is skipped and reported,
differing content overwrites, a dry run reports the same verdict w/o
touching the filesystem
"""

from pathlib import Path

from kaye_engine.cli.dry_run import is_dry_run
from kaye_engine.deed import track

__all__ = ("write_text_if_changed",)


# constants  ###################################################################
_DFT_ENCODING = "utf-8"


# Public API  ##################################################################
def write_text_if_changed(logger, path, content, *, encoding=_DFT_ENCODING):
    """
    write ``content`` to ``path``, unless the file already holds it

    - missing file: ``create_file`` deed, then write
    - same content: ``SKIP`` line, nothing written
    - other content: ``owr_file`` deed, then write

    the existing file is read and compared even under a dry run, so the
    dry verdict equals the live one; only the write itself is skipped


    :param logger: logger every line goes through
    :type logger: logging.Logger
    :param path: file to write; its folder must exist
    :type path: Path-like
    :param content: text the file should hold
    :type content: str
    :param encoding: text encoding of the file
    :type encoding: str, optional
    :return: if the file was written, or under a dry run would be written
    :rtype: bool
    """
    path = Path(path)
    if path.exists():
        if _read_text_or_none(path, encoding) == content:
            logger.skip("unchanged " + str(path))
            return False
        deed = track(logger).owr_file
    else:
        deed = track(logger).create_file

    with deed(path):
        if not is_dry_run():
            path.write_text(content, encoding=encoding)
    return True


# auxiliaries  #################################################################
def _read_text_or_none(path, encoding):
    """
    :return: text of ``path`` with universal newlines, so a CRLF checkout
            equals its LF render; ``None`` when unreadable or undecodable,
            which never equals any content
    :rtype: str or None
    """
    try:
        return path.read_text(encoding=encoding)
    except (OSError, UnicodeDecodeError):
        return None
