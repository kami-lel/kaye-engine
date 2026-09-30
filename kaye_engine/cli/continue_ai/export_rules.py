"""
export_rules.py

define ``classify_exportable`` and ``export_continue_folder``
"""

from pathlib import Path

import kamilog
from kaye_engine.cli.continue_ai import LOGGER_CONTINUE_NAME
from kaye_engine.cli.dry_run import is_dry_run
from kaye_engine.cli.continue_ai.rule_md import ContinueRule
from kaye_engine.exportable import exportable_registry

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_CONTINUE_NAME)

# constants  ###################################################################

RULES_SUBFOLDER = "rules"
PROMPTS_SUBFOLDER = "prompts"

_KIND_RULE = "rule"
_KIND_PROMPT = "prompt"

# classification  ##############################################################


def classify_exportable(exportable):
    """
    decide how an entry lands in a Continue folder

    ``always_apply`` forces a rule; otherwise an LLM-invokable entry is a
    rule, a merely user-invokable one is a prompt, and the rest is skipped


    :param exportable: entry to classify
    :type exportable: Exportable
    :return: ``"rule"``, ``"prompt"``, or ``None`` when skipped
    :rtype: str or None
    """
    if exportable.always_apply or exportable.llm_invokable:
        return _KIND_RULE
    if exportable.is_user_invokable:
        return _KIND_PROMPT
    return None


# entry point  #################################################################


def export_continue_folder(folder, *, render_profile=None):
    """
    export every `exportable_registry` entry into a Continue folder

    writes ``rules/<canonical_name>.md`` or ``prompts/<canonical_name>.md``
    under ``folder`` per :func:`classify_exportable`; skipped entries write
    nothing


    :param folder: Continue config folder, e.g. ``~/.continue``
    :type folder: Path-like
    :param render_profile: render options forwarded to
            :meth:`ContinueRule.from_exportable`
    :type render_profile: RenderProfile, optional
    """
    logger.enter("exporting exportables as Continue rules & prompts")

    folder = Path(folder)
    subfolders = {
        _KIND_RULE: folder / RULES_SUBFOLDER,
        _KIND_PROMPT: folder / PROMPTS_SUBFOLDER,
    }
    try:
        for subfolder in subfolders.values():
            if not subfolder.is_dir():
                with logger.track.create_dir(subfolder):
                    if not is_dry_run():
                        subfolder.mkdir(parents=True, exist_ok=True)
    except OSError as err:
        raise SystemExit(1) from err

    for exportable in exportable_registry.values():
        kind = classify_exportable(exportable)
        if kind is None:
            logger.debug("skip:\t" + exportable.canonical_name)
            continue

        path = subfolders[kind] / (exportable.canonical_name + ".md")
        try:
            ContinueRule.from_exportable(
                exportable,
                is_prompt=kind == _KIND_PROMPT,
                render_profile=render_profile,
            ).write(path)
        except OSError as err:
            raise SystemExit(1) from err
