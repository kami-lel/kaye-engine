"""
sync.py

define ``SyncSummary``, ``sync_skills``
"""

from dataclasses import dataclass, field
from functools import partial

from kaye_engine import kamilog
from kaye_engine.cli.open_webui import LOGGER_OPEN_WEBUI_NAME
from kaye_engine.cli.open_webui.client import OpenWebUIError
from kaye_engine.cli.open_webui.plan import plan_skill_sync
from kaye_engine.cli.open_webui.skill_form import build_skill_form
from kaye_engine.exportable import exportable_registry

__all__ = ("SyncSummary", "sync_skills")

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_OPEN_WEBUI_NAME)


@dataclass
class SyncSummary:
    """
    outcome of a sync, as skill ids per action

    under a dry run, ``created``, ``updated``, and ``pruned`` list what
    would have been done


    :param created: ids created
    :type created: list[str]
    :param updated: ids updated
    :type updated: list[str]
    :param skipped: ids already up to date
    :type skipped: list[str]
    :param pruned: ids deleted from the remote
    :type pruned: list[str]
    :param failed: ``(id, error)`` pairs whose request failed
    :type failed: list[tuple[str, OpenWebUIError]]
    """

    created: list = field(default_factory=list)
    updated: list = field(default_factory=list)
    skipped: list = field(default_factory=list)
    pruned: list = field(default_factory=list)
    failed: list = field(default_factory=list)


# Public API  ##################################################################
def sync_skills(client, is_dry_run=False, should_prune=False):
    """
    push every registered exportable to Open WebUI as a skill

    one failed request is recorded and never aborts the rest; a failure
    to fetch the remote export does raise, since nothing can be planned


    :param client: client for the target server
    :type client: OpenWebUIClient
    :param is_dry_run: whether to plan and report without writing
    :type is_dry_run: bool, optional
    :param should_prune: whether to delete remote skills absent locally
    :type should_prune: bool, optional
    :return: what was done, or would be done under a dry run
    :rtype: SyncSummary
    :raises OpenWebUIError: if the remote export cannot be fetched
    """
    local_forms = [
        build_skill_form(exportable_registry[name])
        for name in sorted(exportable_registry)
    ]
    plan = plan_skill_sync(local_forms, client.export_skills())
    summary = SyncSummary(skipped=list(plan.skip))

    for form in plan.create:
        _apply(
            summary.created, summary, "create", form["id"], is_dry_run,
            partial(client.create_skill, form),
        )
    for form in plan.update:
        _apply(
            summary.updated, summary, "update", form["id"], is_dry_run,
            partial(client.update_skill, form),
        )
    if should_prune:
        for skill_id in plan.prune:
            _apply(
                summary.pruned, summary, "prune", skill_id, is_dry_run,
                partial(client.delete_skill, skill_id),
            )

    return summary


# auxiliaries  #################################################################
def _apply(bucket, summary, verb, skill_id, is_dry_run, request):
    label = verb + (" (dry run)" if is_dry_run else "")
    if not is_dry_run:
        try:
            request()
        except OpenWebUIError as err:
            summary.failed.append((skill_id, err))
            logger.caution("{} failed:\t{}\t{}".format(verb, skill_id, err))
            return
    bucket.append(skill_id)
    logger.succ("{}:\t{}".format(label, skill_id))
