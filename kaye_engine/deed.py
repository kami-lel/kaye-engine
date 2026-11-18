"""
deed.py

define ``track``, ``format_size``, ``tmp_deeds`` -- report a file or
directory action as one fixed-wording log line at block exit, success or
failure; stands in for the deed feature dropped from kamilog 3.0.0
"""

import contextlib
import logging
import os

from kaye_engine.badge import (
    CP_BADGE,
    DEL_BADGE,
    MV_BADGE,
    NEW_BADGE,
    OWR_BADGE,
    TMP_BADGE,
)

__all__ = ("format_size", "tmp_deeds", "track")


# constants  ###################################################################
# deed name → (wording template, success level, failure level, success badge)
_DEEDS = {
    "create_file": ("create {}", logging.INFO, logging.ERROR, NEW_BADGE),
    "owr_file": ("overwrite {}", logging.WARNING, logging.ERROR, OWR_BADGE),
    "create_dir": ("create dir {}", logging.INFO, logging.ERROR, NEW_BADGE),
    "pack_files": ("pack {} -> {}", logging.INFO, logging.ERROR, NEW_BADGE),
    "mv_file": ("move {} -> {}", logging.INFO, logging.ERROR, MV_BADGE),
    "cp_file": ("copy {} -> {}", logging.INFO, logging.ERROR, CP_BADGE),
    "del_file": ("delete {}", logging.INFO, logging.ERROR, DEL_BADGE),
    "del_dir": ("delete dir {}", logging.INFO, logging.ERROR, DEL_BADGE),
    # scratch write outside any ``tmp_deeds`` root, eg a sibling temp name
    "create_tmp": ("create {}", logging.DEBUG, logging.ERROR, TMP_BADGE),
    # args: kind, path; ``stats`` set on the scope fills the bracket
    "create_zip": (
        "export {}{stats}: {}", logging.INFO, logging.ERROR, NEW_BADGE,
    ),
    "load_config": ("load {}", logging.INFO, logging.ERROR, None),
    "save_config": ("save {}", logging.INFO, logging.ERROR, None),
}

# open ``tmp_deeds`` blocks; success lines drop to DEBUG and wear the tmp
# badge while above 0
_tmp_depth = 0

# temp folders of the open blocks, shown as ``<tmp>`` in a logged path
_tmp_roots = []

# stands in for a tmp root inside a logged path
_TMP_MARK = "<tmp>"

# unit steps for ``format_size``
_SIZE_STEP = 1024

# frames from ``Logger.log`` up to the code holding the ``with``:
# _emit, __exit__, the with statement
_STACKLEVEL = 3


class _DeedScope:  # ***********************************************************
    """
    context manager of one deed; logs once at block exit, a failure line
    with traceback when the block raised an ``Exception``
    """

    def __init__(self, logger, template, level, err_level, badge, args):
        self._logger = logger
        self._template = template
        # success level; a caller may raise it before the block exits
        self.level = level
        self._err_level = err_level
        self._badge = badge
        self._args = tuple(map(str, args))
        # detail shown in brackets once known, eg ``23 skills, 412 KB``
        self.stats = ""

    @property
    def _message(self):
        stats = " ({})".format(self.stats) if self.stats else ""
        return self._template.format(*self._args, stats=stats)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None and _tmp_depth:
            self._emit(
                logging.DEBUG, _mask_tmp_roots(self._message),
                badges=TMP_BADGE,
            )
        elif exc_type is None:
            self._emit(self.level, self._message, badges=self._badge)
        elif issubclass(exc_type, Exception):
            cause = exc_type.__name__
            if str(exc_value):
                cause = "{}: {}".format(cause, exc_value)
            self._emit(
                self._err_level,
                "fail to {}: {}".format(self._message, cause),
                (exc_type, exc_value, traceback),
            )
        return False

    def _emit(self, level, message, exc_info=None, badges=None):
        if self._logger.isEnabledFor(level):
            self._logger.log(
                level, message, exc_info=exc_info, stacklevel=_STACKLEVEL,
                badges=badges,
            )


def _mask_tmp_roots(message):
    """
    :return: ``message`` with every open tmp root shown as ``<tmp>``, the
            longest root first so a nested root is not cut short
    :rtype: str
    """
    for root in sorted(_tmp_roots, key=len, reverse=True):
        message = message.replace(root, _TMP_MARK)
    return message


@contextlib.contextmanager
def tmp_deeds(*roots):  # ======================================================
    """
    log every deed success inside the block at ``DEBUG`` with the ``tmp``
    badge, whatever its own level and badge; failure lines keep their error
    level, badge-free, and real paths

    blocks nest: lines stay scratch until the outermost block exits


    :param roots: temp folders the block works in; each shows as ``<tmp>``
            inside a logged path
    :type roots: Path-like
    """
    global _tmp_depth  # pylint: disable=global-statement
    marks = [os.fspath(root).rstrip(os.sep) for root in roots]
    marks = [m for m in marks if m]
    _tmp_depth += 1
    _tmp_roots.extend(marks)
    try:
        yield
    finally:
        _tmp_depth -= 1
        del _tmp_roots[len(_tmp_roots) - len(marks):]


def format_size(size):  # ======================================================
    """
    format a byte count as short text, eg ``412 KB``, ``1.1 MB``


    :param size: byte count
    :type size: int
    :return: size with the largest fitting unit; whole number below 1 MB,
            1 decimal from 1 MB up
    :rtype: str
    """
    if size < _SIZE_STEP:
        return "{} B".format(size)
    kilo = size / _SIZE_STEP
    if kilo < _SIZE_STEP:
        return "{} KB".format(round(kilo))
    return "{:.1f} MB".format(kilo / _SIZE_STEP)


class _DeedTrack:  # ***********************************************************
    """
    namespace of deeds bound to one logger, each method returning a
    context manager: ``with track(logger).create_file(path): ...``
    """

    def __init__(self, logger):
        self._logger = logger

    def __getattr__(self, name):
        try:
            template, level, err_level, badge = _DEEDS[name]
        except KeyError:
            raise AttributeError(name) from None

        def deed(*args):
            return _DeedScope(
                self._logger, template, level, err_level, badge, args
            )

        return deed


def track(logger):  # ==========================================================
    """
    bind the deeds to ``logger``


    :param logger: logger every deed line goes through
    :type logger: logging.Logger
    :return: namespace with one method per deed (``create_file``,
            ``owr_file``, ``create_dir``, ``pack_files``, ``mv_file``,
            ``cp_file``, ``del_file``, ``del_dir``, ``create_tmp``,
            ``create_zip``, ``load_config``, ``save_config``); every
            scope takes a ``level`` attribute to override its success
            level, and the ``create_zip`` scope a ``stats`` attribute,
            shown in brackets
    :rtype: _DeedTrack
    """
    return _DeedTrack(logger)
