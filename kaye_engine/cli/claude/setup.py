"""
setup.py

define ``setup_claude_cli``, ``get_claude_cli_consumer_version``,
``get_marketplace_folder_name``
"""

# pylint: disable=protected-access


from kaye_engine import kamilog
from kaye_engine.cli import claude
from kaye_engine.prompt.affordance_registry import (
    affordance_registry,
    register_affordance,
)

__all__ = (
    "get_claude_cli_consumer_version",
    "get_claude_cli_display_name",
    "get_marketplace_folder_name",
    "get_surface_profiles",
    "setup_claude_cli",
)

# logger  ######################################################################
logger = kamilog.getLogger(claude.LOGGER_CLAUDE_NAME)


# Public API  ##################################################################


def setup_claude_cli(
    plugin_name,
    display_name,
    marketplace_name,
    chat_exportable_name,
    chat_coder_exportable_name,
    version,
    marketplace_folder_name,
    affordance_names=(),
    surface_profiles=None,
):
    """
    set every consumer-configurable value used by the ``claude`` CLI
    subcommand family in one call

    Prerequisite: :func:`register_exportable_entry` (or
    :func:`register_blueprint`) for ``chat_exportable_name`` and
    ``chat_coder_exportable_name``


    :param plugin_name: name written into ``plugin.json``, and used as the
            plugin's folder name and export keyword
    :type plugin_name: str
    :param display_name: display name stamped into ``plugin.json``'s
            ``display_name`` field
    :type display_name: str
    :param marketplace_name: name written into ``marketplace.json``
    :type marketplace_name: str
    :param chat_exportable_name: registered name, in
            `exportable_registry`, of the Chat exportable
    :type chat_exportable_name: str
    :param chat_coder_exportable_name: registered name, in
            `exportable_registry`, of the precomputed Chat+Coder
            exportable, used to build the final ``-c`` prompt
            (``usp -c``, ``claude code``, ``claude vs-code-extension``)
    :type chat_coder_exportable_name: str
    :param version: version string stamped into ``plugin.json``,
            ``marketplace.json``, and every exported ``SKILL.md``
    :type version: str
    :param marketplace_folder_name: folder name used for the marketplace,
            under ``~/.claude`` for ``claude marketplace``'s default
            destination, and under the target Claude folder for ``claude
            vs-code-extension``
    :type marketplace_folder_name: str
    :param affordance_names: canonical names registered into
            `affordance_registry` via `register_claude_affordances`;
            defaults to ``()``
    :type affordance_names: Iterable[str], optional
    :param surface_profiles: populates the ``--surface`` flag's
            choices; ``None`` (default) omits ``--surface`` entirely
    :type surface_profiles: dict[str, RenderProfile] or None, optional
    """
    claude._plugin_name = plugin_name
    claude._display_name = display_name
    claude._marketplace_name = marketplace_name
    claude._chat_exportable_name = chat_exportable_name
    claude._chat_coder_exportable_name = chat_coder_exportable_name
    claude._version = version
    claude._marketplace_folder_name = marketplace_folder_name
    claude._affordance_names = affordance_names
    claude._surface_profiles = surface_profiles

    register_claude_affordances()


def register_claude_affordances():
    """
    register every name in the consumer-configured `affordance_names`
    (see `setup_claude_cli`) into `affordance_registry` via
    `register_affordance`, skipping any `canonical_name` already
    registered -- keeps repeated `setup_claude_cli(...)` calls within
    one process idempotent instead of raising on the second call
    """
    for canonical_name in claude._affordance_names:
        if canonical_name in affordance_registry:
            continue
        register_affordance(canonical_name)


def get_claude_cli_consumer_version():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_claude_cli(...)``
    :return: configured version string
    :rtype: str
    """
    if claude._version is None:
        logger.critical(
            "no version set\n"
            "a consumer project should call "
            "setup_claude_cli(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return claude._version


def get_claude_cli_display_name():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_claude_cli(...)``
    :return: configured display name
    :rtype: str
    """
    if claude._display_name is None:
        logger.critical(
            "no display name set\n"
            "a consumer project should call "
            "setup_claude_cli(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return claude._display_name


def get_marketplace_folder_name():
    """
    :raises SystemExit: exit code 1, when no consumer project has called
            ``setup_claude_cli(...)``
    :return: configured marketplace folder name
    :rtype: str
    """
    if claude._marketplace_folder_name is None:
        logger.critical(
            "no marketplace folder name set\n"
            "a consumer project should call "
            "setup_claude_cli(...) before invoking this CLI"
        )
        raise SystemExit(1)
    return claude._marketplace_folder_name


def get_surface_profiles():
    """
    :return: configured ``dict[str, RenderProfile]`` populating the
            ``--surface`` flag's choices, or ``None`` when the consumer
            project never configured surfaces -- unlike this module's
            other getters, ``None`` is a valid, non-error configuration
            (precedented by ``default_surface=()`` for surface-less
            subcommands), so this never raises
    :rtype: dict[str, RenderProfile] or None
    """
    return claude._surface_profiles
