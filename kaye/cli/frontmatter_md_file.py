"""
frontmatter_md_file.py

define ``FrontmatterMDFile``
"""

import copy


class FrontmatterMDFile:  ######################################################
    """
    base class for writing a markdown file with a YAML frontmatter block


    :param path: output path for the file to write
    :type path: Path-like
    :param blueprint: blueprint object
    :type blueprint: PromptBlueprint
    """

    # abstract method  =========================================================

    def _write_frontmatter_content(self):
        """
        write ``.frontmatter`` content into ``self.file``
        in the specific format required
        """
        raise NotImplementedError

    # public methods  ==========================================================

    def write_frontmatter_part(self):
        """
        write the YAML frontmatter block fenced with ``---`` delimiters
        """
        self.file.write("---\n")
        self._write_frontmatter_content()
        self.file.write("---\n\n")

    # properties  ==============================================================

    @property
    def name(self):
        """
        retrieve the frontmatter ``name`` field


        :return: value of the frontmatter ``name`` field
        :rtype: str
        """
        return self.frontmatter["name"]

    @name.setter
    def name(self, value):
        """
        set the frontmatter ``name`` field


        :param value: new value for the frontmatter ``name`` field
        :type value: str
        """
        self.frontmatter["name"] = value

    @property
    def description(self):
        """
        retrieve the frontmatter ``description`` field


        :return: value of the frontmatter ``description`` field
        :rtype: str
        """
        return self.frontmatter["description"]

    @description.setter
    def description(self, value):
        """
        set the frontmatter ``description`` field


        :param value: new value for the frontmatter ``description`` field
        :type value: str
        """
        self.frontmatter["description"] = value

    # file operation wrapper  ==================================================

    def write(self, content):
        """
        thin wrapper for ``self.file.write()``


        :param content: content to write to the file
        :type content: str
        """
        self.file.write(content)

    # constants  ===============================================================

    _FILE_MODE = "w"
    _FILE_ENCODING = "utf-8"
    _DEFAULT_FRONTMATTER = {
        "name": "",
        "description": "",
        "license": "",
        "compatibility": "",
        "metadata": {},
        "allowed-tools": [],
        "user-invocable": True,
    }

    def __init__(self, path, blueprint=None):
        self.file = None
        self.frontmatter = copy.deepcopy(self._DEFAULT_FRONTMATTER)
        self._path = path
        self._blueprint = None

        if blueprint:
            self._blueprint = blueprint
            self.description = blueprint.description

    # support context manager  =================================================

    def __enter__(self):
        self.file = open(
            self._path, self._FILE_MODE, encoding=self._FILE_ENCODING
        )
        return self

    def __exit__(self, *_):
        if self._blueprint:
            self.write_frontmatter_part()
            self.file.write(self._blueprint.generate_prompt())

        self.file.close()
