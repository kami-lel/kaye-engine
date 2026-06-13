"""
frontmatter_md_file.py

define ``FrontmatterMDFile``
"""


# TODO version
class FrontmatterMDFile:  ######################################################
    """
    base class for writing a markdown file with a YAML frontmatter block


    :param path:
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
        """write the YAML frontmatter block fenced with ``---`` delimiters"""
        self.file.write("---\n")
        self._write_frontmatter_content()
        self.file.write("---\n\n")

    # properties  ==============================================================

    @property
    def name(self):
        """:return: frontmatter ``name`` field"""
        return self.frontmatter["name"]

    @name.setter
    def name(self, value):
        """:param value: new value for the frontmatter ``name`` field"""
        self.frontmatter["name"] = value

    @property
    def description(self):
        """:return: frontmatter ``description`` field"""
        return self.frontmatter["description"]

    @description.setter
    def description(self, value):
        """:param value: new value for the frontmatter ``description`` field"""
        self.frontmatter["description"] = value

    # file operation wrapper  ==================================================

    def write(self, content):
        """
        thin wrapper for ``self.file.write()``
        """
        self.file.write(content)

    # constants  ===============================================================

    _FILE_MODE = "w"
    _FILE_ENCODING = "utf-8"

    def __init__(self, path, blueprint=None):
        self.file = None
        self.frontmatter = {
            "name": "",
            "description": "",
            "license": "",
            "compatibility": "",
            "metadata": {},
            "allowed-tools": [],
        }
        self._path = path
        self._blueprint = None

        if blueprint:
            self._blueprint = blueprint
            self.description = blueprint.description

    # support context manager  =================================================

    def __enter__(self):
        """open the output file and return ``self``"""
        self.file = open(
            self._path, self._FILE_MODE, encoding=self._FILE_ENCODING
        )
        return self

    def __exit__(self, *_):
        """
        if a blueprint is set, write frontmatter then generated prompt;
        close the file in all cases
        """
        if self._blueprint:
            self.write_frontmatter_part()
            self.file.write(self._blueprint.generate_prompt())

        self.file.close()
