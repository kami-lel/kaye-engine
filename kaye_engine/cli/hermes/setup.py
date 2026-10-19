"""
setup.py

define ``setup_hermes_cli`` and the getters of its configured values
"""

# pylint: disable=protected-access

import kamilog
from kaye_engine.cli import hermes
from kaye_engine.prompt.blueprint import blueprint_registry

__all__ = (
    "get_hermes_profile_blueprint_names",
    "get_hermes_soul_blueprint_name",
    "setup_hermes_cli",
)

# logger  ######################################################################
logger = kamilog.getLogger(hermes.LOGGER_HERMES_NAME)


# Public API  ##################################################################


def setup_hermes_cli(soul_blueprint_name=None, profile_blueprint_names=None):
    """
    set every consumer-configurable value used by the ``hermes`` CLI
    subcommand in one call

    Prerequisite: :func:`register_consumer` (each consumer's canonical
    name is the folder, under ``skills/``, that holds its exported
    skills), and :func:`register_blueprint` for ``soul_blueprint_name``
    and every value of ``profile_blueprint_names`` when given; a name left
    unset makes ``hermes`` exit 1 with a clear message


    :param soul_blueprint_name: registered name, in `blueprint_registry`,
            of the blueprint rendered into the root ``SOUL.md``
    :type soul_blueprint_name: str or None, optional
    :param profile_blueprint_names: profile name -> registered name, in
            `blueprint_registry`, of the blueprint rendered into
            ``profiles/<profile name>/SOUL.md``
    :type profile_blueprint_names: dict[str, str] or None, optional
    :raises SystemExit: exit code 1, when a blueprint name is not
            registered
    """
    profile_blueprint_names = profile_blueprint_names or {}
    names = [*profile_blueprint_names.values()]
    if soul_blueprint_name is not None:
        names.insert(0, soul_blueprint_name)
    for name in names:
        if name not in blueprint_registry:
            logger.critical(
                "unknown blueprint %r\n"
                "register it before calling setup_hermes_cli(...)",
                name,
            )
            raise SystemExit(1)

    hermes._soul_blueprint_name = soul_blueprint_name
    hermes._profile_blueprint_names = dict(profile_blueprint_names)


def _get_configured(value, description):
    """
    :raises SystemExit: exit code 1, when ``value`` is still unset
    :return: ``value``
    """
    if value is None:
        logger.critical(
            "no %s set\n"
            "a consumer project should call "
            "setup_hermes_cli(...) before invoking this CLI",
            description,
        )
        raise SystemExit(1)
    return value


def get_hermes_soul_blueprint_name():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_hermes_cli(...)``
    :return: configured blueprint name of the root ``SOUL.md``
    :rtype: str
    """
    return _get_configured(
        hermes._soul_blueprint_name, "soul blueprint name"
    )


def get_hermes_profile_blueprint_names():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_hermes_cli(...)``
    :return: configured profile name -> blueprint name mapping
    :rtype: dict[str, str]
    """
    return _get_configured(
        hermes._profile_blueprint_names, "profile blueprint names"
    )
