"""
frontmatter_doc.py

define ``FrontmatterDoc`` and the shared ``dump_yaml`` helper
"""

import io
from pathlib import Path

import kamilog
import yaml

from kaye_engine.deed import track
from kaye_engine import LOGGER_NAME
from kaye_engine.cli.dry_run import is_dry_run

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

_FILE_ENCODING = "utf-8"


def dump_yaml(mapping):  # =====================================================
    """
    dump a mapping as a YAML block using the project's shared settings


    :param mapping: frontmatter fields to serialize
    :type mapping: dict
    :return: YAML text for ``mapping``
    :rtype: str
    """
    yaml_buffer = io.StringIO()
    yaml.dump(
        mapping,
        yaml_buffer,
        default_flow_style=False,
        sort_keys=False,
        width=float("inf"),
        allow_unicode=True,
    )
    return yaml_buffer.getvalue()


class FrontmatterDoc:  # =======================================================
    """
    base class for a markdown document made of a YAML frontmatter block
    fenced with ``---`` delimiters, followed by a body string


    :param body: markdown body written after the frontmatter block
    :type body: str
    """

    # Public Methods  ----------------------------------------------------------

    def render(self):
        """
        render the full document: fenced frontmatter block plus body


        :return: complete markdown document text
        :rtype: str
        """
        return "---\n{}---\n\n{}".format(self._render_frontmatter(), self.body)

    def write(self, path):
        """
        render the document and write it to ``path``


        :param path: output path for the file to write
        :type path: Path-like
        """
        path = Path(path)
        deed = track(logger).owr_file if path.exists() else (
            track(logger).create_file
        )
        with deed(path):
            if not is_dry_run():
                path.write_text(self.render(), encoding=_FILE_ENCODING)

    # fields   -----------------------------------------------------------------

    body = ""  # default; dataclass subclasses override as a field

    # Abstract Method  ---------------------------------------------------------

    def _render_frontmatter(self):
        """
        render ``self``'s frontmatter fields in the format-specific layout


        :return: frontmatter text, without the ``---`` fences
        :rtype: str
        """
        raise NotImplementedError
