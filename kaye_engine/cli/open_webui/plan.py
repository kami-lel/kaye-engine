"""
plan.py

define ``SyncPlan``, ``plan_skill_sync``
"""

from dataclasses import dataclass, field

from kaye_engine.cli.open_webui.skill_form import SKILL_FORM_FIELDS

__all__ = ("SyncPlan", "plan_skill_sync")


@dataclass
class SyncPlan:
    """
    what a sync has to do, grouped by action


    :param create: forms absent from the remote
    :type create: list[dict]
    :param update: forms whose remote record differs
    :type update: list[dict]
    :param skip: ids whose remote record already matches
    :type skip: list[str]
    :param prune: remote-only ids
    :type prune: list[str]
    """

    create: list = field(default_factory=list)
    update: list = field(default_factory=list)
    skip: list = field(default_factory=list)
    prune: list = field(default_factory=list)


# Public API  ##################################################################
def plan_skill_sync(local_forms, remote_records):
    """
    compare local forms with the remote export

    only the fields in ``SKILL_FORM_FIELDS`` are compared; server-owned
    fields such as timestamps never trigger an update


    :param local_forms: forms built from the local registry
    :type local_forms: list[dict]
    :param remote_records: records from the remote export
    :type remote_records: list[dict]
    :return: the actions to take
    :rtype: SyncPlan
    """
    remote_by_id = {record["id"]: record for record in remote_records}
    plan = SyncPlan()

    for form in local_forms:
        remote = remote_by_id.get(form["id"])
        if remote is None:
            plan.create.append(form)
        elif _is_form_changed(form, remote):
            plan.update.append(form)
        else:
            plan.skip.append(form["id"])

    local_ids = {form["id"] for form in local_forms}
    plan.prune = [
        remote_id for remote_id in remote_by_id if remote_id not in local_ids
    ]
    return plan


# auxiliaries  #################################################################
def _is_form_changed(form, remote):
    return any(form[key] != remote.get(key) for key in SKILL_FORM_FIELDS)
