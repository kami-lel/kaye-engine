"""
verbosity.py

define ``apply_verbosity_arg`` -- the one place a command turns its
parsed ``-v``/``-q``/``-V``/``-Q`` flags into a logging level, so every
engine logger honors them, not only the command's own
"""

import logging

import kamilog

from kaye_engine import LOGGER_NAME

__all__ = ("apply_verbosity_arg",)


def apply_verbosity_arg(args):
    """
    set the level of every engine logger from a parsed namespace

    the level lands on the ``kaye.engine`` logger alone; each existing
    descendant is reset to ``NOTSET`` so it inherits that level, as does
    any logger created later

    :param args: parsed namespace carrying the ``kamilog`` verbosity
        counts
    :type args: argparse.Namespace
    """
    kamilog.set_logging_level_by_namespace(
        args, logger=logging.getLogger(LOGGER_NAME)
    )
    prefix = LOGGER_NAME + "."
    for name, child in list(logging.root.manager.loggerDict.items()):
        if name.startswith(prefix) and isinstance(child, logging.Logger):
            child.setLevel(logging.NOTSET)
