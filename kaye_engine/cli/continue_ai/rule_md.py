"""
rule_md.py

define ``ContinueRule``
"""

from kaye_engine.cli.frontmatter_doc import FrontmatterDoc, dump_yaml


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
