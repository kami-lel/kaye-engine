"""
rule_file.py

define ``ContinueRule``
"""


from kaye.cli.frontmatter_doc import FrontmatterDoc, dump_yaml


class ContinueRule(FrontmatterDoc):  ##########################################
    """
    a Continue AI rule document: metadata frontmatter plus rule body


    :param name: rule name written to the ``name`` frontmatter field
    :type name: str
    :param description: rule description; omitted from frontmatter when
            empty
    :type description: str
    :param globs: file globs the rule applies to; omitted when empty
    :type globs: iterable(str)
    :param always_apply: value of the ``alwaysApply`` frontmatter field;
            default=False
    :type always_apply: bool, optional
    :param invokable: whether the rule is invokable; emitted only when
            True; default=False
    :type invokable: bool, optional
    :param body: markdown body written after the frontmatter block
    :type body: str
    :example:
    >>> # blueprint rule
    ... ContinueRule.from_registry(reg).write(path)

    >>> # abbreviation rule
    ... ContinueRule(name=~~, description=~~, body=~~).write(path)
    """

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
        self.globs = globs or []
        self.always_apply = always_apply
        self.invokable = invokable
        self.body = body

    # factory  =================================================================

    @classmethod
    def from_registry(cls, registry):
        """
        :param registry: blueprint registry entry to render
        :type registry: BlueprintRegistry
        :return: a rule built from ``registry`` and its blueprint prompt
        :rtype: ContinueRule
        """
        sidecars = registry.blueprint.sidecars
        return cls(
            name=registry.display_name,
            description=sidecars.description_and_when_to_use,
            globs=sidecars.globs,
            always_apply=registry.always_apply,
            invokable=not registry.llm_invokable,
            body=registry.blueprint.generate_prompt(
                contains_sidecars=("prerequisite",)
            ),
        )

    # implement FrontmatterDoc  ================================================

    def _render_frontmatter(self):
        metadata = {"name": self.name}
        if self.description:
            metadata["description"] = self.description

        metadata["alwaysApply"] = self.always_apply
        if self.invokable:
            metadata["invokable"] = self.invokable

        rendered = dump_yaml(metadata)

        if self.globs:
            globs_str = ", ".join('"{}"'.format(g) for g in self.globs)
            rendered += "globs: [{}]\n".format(globs_str)

        return rendered
