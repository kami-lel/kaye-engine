"""
asset_name.py

define ``get_release_asset_name``, ``get_release_asset_stem`` -- name every
release asset ``REPO-VERSION-TYPE[-X].ext`` from the repo name and version
the consumer project registered
"""

from kaye_engine.consumer import get_default_consumer
from kaye_engine.repo import get_repo_name, get_repo_version

__all__ = (
    "ASSET_DESKTOP_PLUGIN",
    "ASSET_SYSTEM_PROMPT",
    "ASSET_VSC_INSTALLER",
    "OS_LINUX",
    "OS_WINDOWS",
    "PROMPT_CHAT",
    "PROMPT_CODER",
    "get_release_asset_name",
    "get_release_asset_stem",
)

# constants  ###################################################################
ASSET_DESKTOP_PLUGIN = "claude-desktop-plugin"
ASSET_VSC_INSTALLER = "claude-vsc-installer"
ASSET_SYSTEM_PROMPT = "claude-system-prompt"

OS_WINDOWS = "Win"
OS_LINUX = "linux"

PROMPT_CHAT = "chat"
PROMPT_CODER = "coder"

_INSTALLER_EXTENSIONS = {OS_WINDOWS: ".zip", OS_LINUX: ".run"}
_PROMPT_VARIANTS = (PROMPT_CHAT, PROMPT_CODER)


# Public API  ##################################################################
def get_release_asset_stem(
    asset_type,
    *,
    os_name=None,
    consumer=None,
    prompt_variant=None,
    includes_version=True,
):
    """
    :param asset_type: ``ASSET_DESKTOP_PLUGIN``, ``ASSET_VSC_INSTALLER`` or
            ``ASSET_SYSTEM_PROMPT``
    :type asset_type: str
    :param os_name: the installer's OS, ``OS_WINDOWS`` or ``OS_LINUX``;
            required for an installer, refused for a plugin
    :type os_name: str, optional
    :param consumer: canonical name of the plugin's consumer; the default
            consumer leaves its name out; refused for an installer and a
            system prompt
    :type consumer: str, optional
    :param prompt_variant: the system prompt's blueprint, ``PROMPT_CHAT``
            or ``PROMPT_CODER``; required for a system prompt, refused for
            the other types
    :type prompt_variant: str, optional
    :param includes_version: whether to keep the repo version segment
    :type includes_version: bool
    :raises ValueError: on an unknown ``asset_type``, ``os_name`` or
            ``prompt_variant``, or an argument the type does not take
    :raises SystemExit: exit code 1, when the repo name, the repo version,
            or (given ``consumer``) the default consumer is unset
    :return: the asset's file name w/o extension, ``REPO-VERSION-TYPE`` plus
            ``-CONSUMER``, ``-OS`` or ``-VARIANT``
    :rtype: str
    """
    if prompt_variant is not None and asset_type != ASSET_SYSTEM_PROMPT:
        raise ValueError("only a system prompt takes a prompt_variant")
    if asset_type == ASSET_DESKTOP_PLUGIN:
        if os_name is not None:
            raise ValueError("a desktop plugin takes no os_name")
        segments = [asset_type]
        if consumer is not None and (
            consumer != get_default_consumer().canonical_name
        ):
            segments.append(consumer)
    elif asset_type == ASSET_VSC_INSTALLER:
        if consumer is not None:
            raise ValueError("an installer takes no consumer")
        if os_name not in _INSTALLER_EXTENSIONS:
            raise ValueError(
                "installer os_name must be one of {}, got {!r}".format(
                    ", ".join(_INSTALLER_EXTENSIONS), os_name
                )
            )
        segments = [asset_type, os_name]
    elif asset_type == ASSET_SYSTEM_PROMPT:
        if os_name is not None or consumer is not None:
            raise ValueError("a system prompt takes no os_name or consumer")
        if prompt_variant not in _PROMPT_VARIANTS:
            raise ValueError(
                "prompt_variant must be one of {}, got {!r}".format(
                    ", ".join(_PROMPT_VARIANTS), prompt_variant
                )
            )
        segments = [asset_type, prompt_variant]
    else:
        raise ValueError("unknown asset type {!r}".format(asset_type))

    head = [get_repo_name()]
    if includes_version:
        head.append(get_repo_version())
    return "-".join([*head, *segments])


def get_release_asset_name(
    asset_type,
    *,
    os_name=None,
    consumer=None,
    prompt_variant=None,
    includes_version=True,
):
    """
    :param includes_version: whether to keep the repo version segment
    :type includes_version: bool
    :return: the asset's full file name, :func:`get_release_asset_stem`
            plus its extension: ``.zip`` for a plugin and the Windows
            installer, ``.run`` for the Linux installer, ``.md`` for a
            system prompt
    :rtype: str
    """
    stem = get_release_asset_stem(
        asset_type,
        os_name=os_name,
        consumer=consumer,
        prompt_variant=prompt_variant,
        includes_version=includes_version,
    )
    if asset_type == ASSET_DESKTOP_PLUGIN:
        extension = ".zip"
    elif asset_type == ASSET_SYSTEM_PROMPT:
        extension = ".md"
    else:
        extension = _INSTALLER_EXTENSIONS[os_name]
    return stem + extension
