"""
frontmatter_md_file.py

define ``FrontmatterMDFile``
"""


class FrontmatterMDFile:  ######################################################
    """
    base class for writing a markdown file with a YAML frontmatter block


    :param path:
    :type path: Path-like
    :param blueprint: blueprint object
    :type blueprint: PromptBlueprint
    """

    def write_frontmatter(self):
        raise NotImplementedError

    def write_blueprint_content(self):
        self.file.write(self._blueprint.generate_prompt())

    # properties  ==============================================================

    name = property()

    @name.setter
    def name(self, value):
        self.frontmatter["name"] = value

    description = property()

    @description.setter
    def description(self, value):
        self.frontmatter["description"] = value

    # file operation wrapper  ==================================================

    def write(self, content):
        self.file.write(content)

    def writelines(self, lines):
        self.file.writelines(lines)

    # constants  ===============================================================

    _FILE_MODE = "w"
    _FILE_ENCODING = "utf-8"

    def __init__(self, path, blueprint):
        self._path = path
        self._blueprint = blueprint

        self.file = None
        self.frontmatter = {}

    # support context manager  =================================================

    def __enter__(self):
        self.file = open(
            self._path, self._FILE_MODE, encoding=self._FILE_ENCODING
        )
        return self

    def __exit__(self, *_):
        self.file.close()
