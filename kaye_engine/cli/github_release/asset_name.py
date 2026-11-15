"""
asset_name.py

define ``get_release_asset_name``, ``get_release_asset_stem`` -- name every
release asset ``REPO-VERSION-TYPE[-OS].ext`` from the repo name and version
the consumer project registered
"""

from kaye_engine.consumer import get_default_consumer
from kaye_engine.repo import get_repo_name, get_repo_version

__all__ = (
    "ASSET_DESKTOP_PLUGIN",
    "ASSET_VSC_INSTALLER",
    "OS_LINUX",
    "OS_WINDOWS",
    "get_release_asset_name",
    "get_release_asset_stem",
)

# constants  ###################################################################
ASSET_DESKTOP_PLUGIN = "claude-desktop-plugin"
ASSET_VSC_INSTALLER = "claude-vsc-installer"

OS_WINDOWS = "Win"
OS_LINUX = "linux"

_INSTALLER_EXTENSIONS = {OS_WINDOWS: ".zip", OS_LINUX: ".run"}


# Public API  ##################################################################
def get_release_asset_stem(asset_type, *, os_name=None, consumer=None):
    """
    :param asset_type: ``ASSET_DESKTOP_PLUGIN`` or ``ASSET_VSC_INSTALLER``
    :type asset_type: str
    :param os_name: the installer's OS, ``OS_WINDOWS`` or ``OS_LINUX``;
            required for an installer, refused for a plugin
    :type os_name: str, optional
    :param consumer: canonical name of the plugin's consumer; the default
            consumer leaves its name out; refused for an installer
    :type consumer: str, optional
    :raises ValueError: on an unknown ``asset_type`` or ``os_name``, or an
            argument the type does not take
    :raises SystemExit: exit code 1, when the repo name, the repo version,
            or (given ``consumer``) the default consumer is unset
    :return: the asset's file name w/o extension, ``REPO-VERSION-TYPE`` plus
            ``-CONSUMER`` or ``-OS``
    :rtype: str
    """
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
    else:
        raise ValueError("unknown asset type {!r}".format(asset_type))

    return "-".join([get_repo_name(), get_repo_version(), *segments])


def get_release_asset_name(asset_type, *, os_name=None, consumer=None):
    """
    :return: the asset's full file name, :func:`get_release_asset_stem`
            plus its extension: ``.zip`` for a plugin and the Windows
            installer, ``.run`` for the Linux installer
    :rtype: str
    """
    stem = get_release_asset_stem(
        asset_type, os_name=os_name, consumer=consumer
    )
    extension = (
        ".zip" if asset_type == ASSET_DESKTOP_PLUGIN
        else _INSTALLER_EXTENSIONS[os_name]
    )
    return stem + extension
