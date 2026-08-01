"""
cli_setup_guard.py

define ``check_corpus_setup_for_cli``
"""

from kaye_engine import LOGGER_NAME, kamilog, get_default_corpus_tree
from kaye_engine.prompt.blueprint import blueprint_registry

__all__ = ("check_corpus_setup_for_cli",)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)


# Public API  ##################################################################
def check_corpus_setup_for_cli():
    """
    warn when no host project has loaded a corpus and registered
    blueprints

    checks both that a default corpus tree is loaded and that
    ``blueprint_registry`` is non-empty, warning separately for each
    """
    try:
        get_default_corpus_tree()
    except ValueError:
        logger.warning(
            "no corpus tree loaded\n"
            "a host project should call "
            "load_corpus_tree(..., is_default_tree=True) "
            "before invoking this CLI"
        )

    if not blueprint_registry:
        logger.warning(
            "no blueprints registered\n"
            "a host project should register "
            "blueprints before invoking this CLI"
        )
