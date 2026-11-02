"""
deed.py

define ``track``, ``format_size``, ``quiet_deeds`` -- report a file or directory action as one fixed-wording
log line at block exit, success or failure; stands in for the deed feature
dropped from kamilog 3.0.0
"""

import contextlib
import logging

from kaye_engine.badge import MV_BADGE, NEW_BADGE, OWR_BADGE

__all__ = ("format_size", "quiet_deeds", "track")


# constants  ###################################################################
# deed name → (wording template, success level, failure level, success badge)
_DEEDS = {
    "create_file": ("create {}", logging.INFO, logging.ERROR, NEW_BADGE),
    "owr_file": ("overwrite {}", logging.WARNING, logging.ERROR, OWR_BADGE),
    "create_dir": ("create dir {}", logging.INFO, logging.ERROR, NEW_BADGE),
    "pack_files": ("pack {} -> {}", logging.INFO, logging.ERROR, NEW_BADGE),
    "mv_file": ("move {} -> {}", logging.INFO, logging.ERROR, MV_BADGE),
    # args: kind, path; ``stats`` set on the scope fills the bracket
    "create_zip": (
        "export {}{stats}: {}", logging.INFO, logging.ERROR, NEW_BADGE,
    ),
    "load_config": ("load {}", logging.INFO, logging.ERROR, None),
    "save_config": ("save {}", logging.INFO, logging.ERROR, None),
}

# open ``quiet_deeds`` blocks; success lines drop to DEBUG while above 0
_quiet_depth = 0

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
        if exc_type is None:
            level = logging.DEBUG if _quiet_depth else self.level
            self._emit(level, self._message, badges=self._badge)
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


@contextlib.contextmanager
def quiet_deeds():  # ==========================================================
    """
    log every deed success inside the block at ``DEBUG``, whatever its own
    level; failure lines stay at their error level

    blocks nest: lines stay quiet until the outermost block exits
    """
    global _quiet_depth  # pylint: disable=global-statement
    _quiet_depth += 1
    try:
        yield
    finally:
        _quiet_depth -= 1


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
            ``create_zip``, ``load_config``, ``save_config``); every
            scope takes a ``level`` attribute to override its success
            level, and the ``create_zip`` scope a ``stats`` attribute,
            shown in brackets
    :rtype: _DeedTrack
    """
    return _DeedTrack(logger)
