"""
metadata_md_file.py

define ``MetadataMDFile``
"""

# TODO docstrings


class MetadataMDFile:  #########################################################

    def write_continue_metafield_and_content(self):
        # metadata  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.file.write("---\n")

        self._write_name_and_description_fields()

        if self.globs:
            globs_str = ", ".join('"{}"'.format(g) for g in self.globs)
            self.file.write("globs: [{}]\n".format(globs_str))

        self.file.write(
            "alwaysApply: {}\n".format(str(self.always_apply).lower())
        )

        if self.invokable:
            self.file.write("invokable: true\n")

        self.file.write("---\n\n")

        # content  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.file.write(self._blueprint.generate_prompt())

    # file operation wrapper  ==================================================

    def write(self, content):
        self.file.write(content)

    def writelines(self, lines):
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

    # helpers  =================================================================
    def _write_name_and_description_fields(self):
        self.file.write("name: {}\n".format(self.name))

        if self.description:
            self.file.write("description: {}\n".format(self.description))

    # support context manager  =================================================

    def __enter__(self):
        self.file = open(
            self._path, self._FILE_MODE, encoding=self._FILE_ENCODING
        )
        return self

    def __exit__(self, *args):
        self.file.close()
