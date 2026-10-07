"""
rule_md.py

define ``ContinueRule``
"""

from kaye_engine.cli.exportable_abbr import ExportableAbbr
from kaye_engine.cli.frontmatter_doc import FrontmatterDoc, dump_yaml
from kaye_engine.prompt.blueprint import BlueprintRegistry
from kaye_engine.prompt.blueprint.render import (
    show_globs,
    show_description_and_when_to_use,
)


class ContinueRule(FrontmatterDoc):
    """
    a Continue AI rule or prompt document: metadata frontmatter plus body

    a rule lives in ``rules/``; a prompt lives in ``prompts/`` and carries
    ``invokable: true``


    :param name: value of the ``name`` frontmatter field
    :type name: str
    :param description: value of the ``description`` field; omitted when
            empty
    :type description: str
    :param globs: file globs the document applies to; omitted when empty
    :type globs: list[str]
    :param always_apply: value of the ``alwaysApply`` field;
            default=False
    :type always_apply: bool, optional
    :param invokable: whether the document is an invokable prompt;
            emitted only when True; default=False
    :type invokable: bool, optional
    :param body: markdown body written after the frontmatter block
    :type body: str
    :example:
    >>> ContinueRule(name="x", description="d", body="b").write(path)
    """

    # implement FrontmatterDoc  ------------------------------------------------

    def _render_frontmatter(self):
        fields = {"name": self.name}
        if self.description:
            fields["description"] = self.description
        fields["alwaysApply"] = self.always_apply
        if self.invokable:
            fields["invokable"] = True
        if self.globs:
            fields["globs"] = self.globs
        return dump_yaml(fields)

    # fields  ------------------------------------------------------------------

    def __init__(
        self,
        name="",
        description="",
        globs=None,
        always_apply=False,
        invokable=False,
        body="",
    ):
        self.name = name
        self.description = description
        self.globs = list(globs) if globs else []
        self.always_apply = always_apply
        self.invokable = invokable
        self.body = body

    # factory  -----------------------------------------------------------------

    @classmethod
    def from_exportable(
        cls, exportable, *, is_prompt=False, render_profile=None
    ):
        """
        dispatches on the concrete `Exportable` implementer, as the Claude
        translation layer does, so `Exportable` stays Continue-agnostic


        :param exportable: entry to render, either a `BlueprintRegistry`
                or an `ExportableAbbr` group
        :type exportable: Exportable
        :param is_prompt: whether to build an invokable prompt rather than
                a rule; a prompt is never always-apply
        :type is_prompt: bool, optional
        :param render_profile: render profile forwarded to
                ``exportable.content(...)``
        :type render_profile: RenderProfile, optional
        :return: a document built from ``exportable``'s content
        :rtype: ContinueRule
        """
        if isinstance(exportable, BlueprintRegistry):
            description = show_description_and_when_to_use(
                exportable.blueprint
            )
            globs = show_globs(exportable.blueprint)
        else:
            assert isinstance(exportable, ExportableAbbr)
            description = exportable.display_name
            globs = None

        return cls(
            name=exportable.display_name,
            description=description,
            globs=globs,
            always_apply=exportable.always_apply and not is_prompt,
            invokable=is_prompt,
            body=exportable.content(profile=render_profile),
        )
