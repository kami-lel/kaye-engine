"""
metadata_md_file.py

define ``MetadataMDFile``
"""

import io
import yaml


# FIXME update to continue specific: rule file
class MetadataMDFile:  #########################################################
    """
    manage metadata and content writing for markdown file with metadata fields


    :param path:
    :type path: Path-like
    :param blueprint: optional blueprint object to populate metadata
    :type blueprint: PromptBlueprint or None
    :example:
    >>> with MetadataMDFile("my_md_file.md", blueprint=bp) as md_file:
    ...     md_file.globs = ~~
    ...     md_file.always_apply = ~~
    ...     md_file.write_continue_metafield_and_content()
    """

    def write_continue_frontmatter(self):
        self.file.write("---\n")

        metadata = {"name": self.name}

        if self.description:
            metadata["description"] = self.description

        metadata["alwaysApply"] = self.always_apply

        if self.invokable:
            metadata["invokable"] = self.invokable

        yaml_buffer = io.StringIO()
        yaml.dump(
            metadata,
            yaml_buffer,
            default_flow_style=False,
            sort_keys=False,
            width=float("inf"),
        )
        self.file.write(yaml_buffer.getvalue())

        if self.globs:
            globs_str = ", ".join('"{}"'.format(g) for g in self.globs)
            self.file.write("globs: [{}]\n".format(globs_str))

        self.file.write("---\n\n")

    def write_continue_frontmatter_and_content(self):
        """
        write metadata fields and prompt content, in **Continue** style
        """
        self.write_continue_frontmatter()

        # content
        self.file.write(self._blueprint.generate_prompt())

    # file operation wrapper  ==================================================

    def write(self, content):
        """
        write string content to the file


        :param content: text to write
        :type content: str
        """
        self.file.write(content)

    def writelines(self, lines):
        """
        write multiple lines to the file


        :param lines: sequence of strings to write
        :type lines: iterable[str]
        """
        self.file.writelines(lines)

    # constants  ===============================================================

    _FILE_MODE = "w"
    _FILE_ENCODING = "utf-8"

    def __init__(self, path, *, blueprint=None):
        self._path = path
        self._blueprint = blueprint

        self.file = None

        # metadata fields  -----------------------------------------------------
        self.name = ""
        self.description = ""

        # continue fields
        self.globs = []
        self.always_apply = False
        self.invokable = False

        # read from blueprint  -------------------------------------------------
        if blueprint:
            self.name = blueprint.display_name
            self.description = blueprint.description

    # support context manager  =================================================

    def __enter__(self):
        self.file = open(
            self._path, self._FILE_MODE, encoding=self._FILE_ENCODING
        )
        return self

    def __exit__(self, *_):
        self.file.close()
