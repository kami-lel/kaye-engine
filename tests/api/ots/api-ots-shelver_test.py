"""
api-ots-shelver_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/opus-tag-smith/shelver
"""

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, dify_app_endpoint):
    endpoint = dify_app_endpoint + "/opus-tag-smith/shelver"
    response = flask_test_client.get(endpoint)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestOpus:

    # main instruction  --------------------------------------------------------

    def test_ots0(_, opt, ots0):
        assert ots0 in opt

    def test_ots1(_, opt, ots1):
        assert ots1 in opt

    def test_ots2(_, opt, ots2):
        assert ots2 in opt

    def test_ots3(_, opt, ots3):
        assert ots3 in opt

    # title  -------------------------------------------------------------------

    def test_title0(_, opt, title0):
        assert title0 in opt

    def test_title1(_, opt, title1):
        assert title1 in opt

    def test_title2(_, opt, title2):
        assert title2 in opt

    def test_title3(_, opt, title3):
        assert title3 in opt

    def test_title4(_, opt, title4):
        assert title4 in opt

    # extract for  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def test_extract_for(_, opt):
        assert "## extract for Shelver" in opt

        # authors  -----------------------------------------------------------------

    def test_authors0(_, opt):
        assert "#### authors, editors, translators" in opt

    def test_authors1(_, opt):
        assert "For *name* of author, editor, or translator:" in opt

    def test_authors2(_, opt):
        assert "- no use `.` in name abbreviation" in opt

    def test_authors3(_, opt):
        assert "- use `et_el` for *other authors*" in opt

    # publisher  ---------------------------------------------------------------

    def test_publisher0(_, opt):
        assert "#### publisher" in opt

    def test_publisher1(_, opt):
        assert "- the publisher of the book" in opt

    def test_publisher2(_, opt):
        assert (
            "- for well-known publisher, "
            "use the most relevant part of the name. E.g.:"
            in opt
        )

    def test_publisher3(_, opt):
        assert (
            "  - use `University of Minnesota`, "
            "not `University of Minnesota Press`"
            in opt
        )

    # tags  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # tag instruction  ---------------------------------------------------------

    def test_tag_instruction0(_, opt, tag_instruction0):
        assert tag_instruction0 in opt

    def test_tag_instruction1(_, opt, tag_instruction1):
        assert tag_instruction1 in opt

    def test_tag_instruction2(_, opt, tag_instruction2):
        assert tag_instruction2 in opt

    def test_tag_instruction3(_, opt, tag_instruction3):
        assert tag_instruction3 in opt

    def test_tag_instruction4(_, opt, tag_instruction4):
        assert tag_instruction4 in opt

    # common tags  -------------------------------------------------------------

    def test_tags_cm1(_, opt, tags_cm1):
        assert tags_cm1 in opt

    def test_tags_cm2(_, opt, tags_cm2):
        assert tags_cm2 in opt

    # tags unique  -------------------------------------------------------------
