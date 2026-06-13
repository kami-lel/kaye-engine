"""
frontmatter_md_file.py

define ``FrontmatterMDFile``
"""


class FrontmatterMDFile:  ######################################################
    """
    base class for writing a markdown file with a YAML frontmatter block


    :param path:
    :type path: Path-like
    """

    def write_frontmatter(self):
        raise NotImplementedError

    # properties  ==============================================================

    @property
    def blueprint(self):
        return self._blueprint

    @blueprint.setter
    def blueprint(self, value):
        self._blueprint = value
        if value:
            self.frontmatter["name"] = value.display_name
            self.frontmatter["description"] = value.description

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

    def __init__(self, path):
        self._path = path

        self.file = None
        self.frontmatter = {
            "name": "",
            "description": "",
            "license": "",
            "compatibility": "",
            "metadata": {},
            "allowed-tools": [],
        }

        self._blueprint = None

    # support context manager  =================================================

    def __enter__(self):
        self.file = open(
            self._path, self._FILE_MODE, encoding=self._FILE_ENCODING
        )
        return self

    def __exit__(self, *_):
        if self.blueprint:
            self.write_frontmatter()
            self.file.write(self.blueprint.generate_prompt())
        self.file.close()
