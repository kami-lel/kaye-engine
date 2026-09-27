"""
skill_form.py

define ``build_skill_form``
"""

from kaye_engine.cli.skill.skill_md import Skill

__all__ = ("SKILL_FORM_FIELDS", "build_skill_form")

# constants  ###################################################################

# fields the form owns, in the order the Open WebUI API reads them
SKILL_FORM_FIELDS = (
    "id",
    "name",
    "description",
    "content",
    "meta",
    "is_active",
)


# Public API  ##################################################################
def build_skill_form(exportable, render_profile=None):
    """
    turn an exportable into the Open WebUI ``SkillForm`` payload

    reuses :meth:`Skill.from_exportable`, so the description, when-to-use,
    and body match the Claude skill export; no network involved


    :param exportable: entry to convert, blueprint or abbr group alike
    :type exportable: Exportable
    :param render_profile: forwarded to ``Skill.from_exportable``
    :type render_profile: RenderProfile, optional
    :return: form fields keyed per :data:`SKILL_FORM_FIELDS`
    :rtype: dict
    """
    skill = Skill.from_exportable(exportable, render_profile=render_profile)
    description = "\n\n".join(
        part for part in (skill.description, skill.when_to_use) if part
    )

    return {
        "id": exportable.canonical_name,
        "name": exportable.display_name,
        "description": description,
        "content": skill.body,
        "meta": {"tags": []},
        "is_active": True,
    }
