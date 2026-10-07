"""
frontmatter_doc_test.py

Unit Tests (using pytest) for:

FrontmatterDoc.write() deed logging
"""

import logging

from kaye_engine import LOGGER_NAME
from kaye_engine.cli.frontmatter_doc import FrontmatterDoc


# auxiliaries  #################################################################
class _Doc(FrontmatterDoc):
    body = "body"

    def _render_frontmatter(self):
        return "a: 1\n"


def _messages(caplog):
    return [rec.message for rec in caplog.records]


# pytest  ######################################################################
class TestWriteDeeds:

    def test_new_file_logs_create(_, tmp_path, caplog):
        path = tmp_path / "doc.md"
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            _Doc().write(path)

        assert path.read_text(encoding="utf-8").startswith("---\na: 1\n")
        assert _messages(caplog) == ["create {}".format(path)]

    def test_existing_file_logs_overwrite_as_warning(_, tmp_path, caplog):
        path = tmp_path / "doc.md"
        path.write_text("old", encoding="utf-8")
        with caplog.at_level(logging.DEBUG, logger=LOGGER_NAME):
            _Doc().write(path)

        assert _messages(caplog) == ["overwrite {}".format(path)]
        assert caplog.records[0].levelno == logging.WARNING
