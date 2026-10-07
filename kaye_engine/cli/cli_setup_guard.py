"""
cli_setup_guard.py

define ``check_corpus_setup_for_cli``
"""

import kamilog
from kaye_engine import LOGGER_NAME, get_corpus_tree
from kaye_engine.prompt.blueprint import blueprint_registry

__all__ = ("check_corpus_setup_for_cli",)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


# Public API  ##################################################################
def check_corpus_setup_for_cli():
    """
    log an error when no consumer project has loaded a corpus and registered
    blueprints

    checks both that a corpus tree is loaded and that
    ``blueprint_registry`` is non-empty, logging separately for each
    """
    try:
        get_corpus_tree()
    except ValueError:
        logger.error(
            "no corpus tree loaded\n"
            "a consumer project should call "
            "load_corpus_tree(sources) "
            "before invoking this CLI"
        )

    if not blueprint_registry:
        logger.error(
            "no blueprints registered\n"
            "a consumer project should register "
            "blueprints before invoking this CLI"
        )
