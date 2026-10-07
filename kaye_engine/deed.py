"""
deed.py

define ``track`` -- report a file or directory action as one fixed-wording
log line at block exit, success or failure; stands in for the deed feature
dropped from kamilog 3.0.0
"""

import logging

__all__ = ("track",)


# constants  ###################################################################
# deed name → (wording template, success level, failure level)
_DEEDS = {
    "create_file": ("create {}", logging.INFO, logging.ERROR),
    "owr_file": ("overwrite {}", logging.WARNING, logging.ERROR),
    "create_dir": ("create dir {}", logging.INFO, logging.ERROR),
    "pack_files": ("pack {} -> {}", logging.INFO, logging.ERROR),
    "mv_file": ("move {} -> {}", logging.INFO, logging.ERROR),
    "load_config": ("load {}", logging.INFO, logging.ERROR),
    "save_config": ("save {}", logging.INFO, logging.ERROR),
}

# frames from ``Logger.log`` up to the code holding the ``with``:
# _emit, __exit__, the with statement
_STACKLEVEL = 3


class _DeedScope:  # ***********************************************************
    """
    context manager of one deed; logs once at block exit, a failure line
    with traceback when the block raised an ``Exception``
    """

    def __init__(self, logger, template, level, err_level, args):
        self._logger = logger
        self._level = level
        self._err_level = err_level
        self._message = template.format(*map(str, args))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self._emit(self._level, self._message)
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

    def _emit(self, level, message, exc_info=None):
        if self._logger.isEnabledFor(level):
            self._logger.log(
                level, message, exc_info=exc_info, stacklevel=_STACKLEVEL
            )


class _DeedTrack:  # ***********************************************************
    """
    namespace of deeds bound to one logger, each method returning a
    context manager: ``with track(logger).create_file(path): ...``
    """

    def __init__(self, logger):
        self._logger = logger

    def __getattr__(self, name):
        try:
            template, level, err_level = _DEEDS[name]
        except KeyError:
            raise AttributeError(name) from None

        def deed(*args):
            return _DeedScope(self._logger, template, level, err_level, args)

        return deed


def track(logger):  # ==========================================================
    """
    bind the deeds to ``logger``


    :param logger: logger every deed line goes through
    :type logger: logging.Logger
    :return: namespace with one method per deed (``create_file``,
            ``owr_file``, ``create_dir``, ``pack_files``, ``mv_file``,
            ``load_config``, ``save_config``)
    :rtype: _DeedTrack
    """
    return _DeedTrack(logger)
