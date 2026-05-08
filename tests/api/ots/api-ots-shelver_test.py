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
        assert "For names in `authors`, `editors`, and `translators`:" in opt

    def test_authors2(_, opt):
        assert (
            "- use `FirstName LastName` or "
            "`FirstName MiddleName LastName` order"
            in opt
        )

    def test_authors3(_, opt):
        assert (
            "- if a person is commonly known in abbreviated form, "
            "use that form instead of the full name"
            in opt
        )

    def test_authors4(_, opt):
        assert "e.g., use `F A Hayek`, not `Friedrich August von Hayek`" in opt

    def test_authors5(_, opt):
        assert (
            "- if additional people exist but are not individually listed, "
            "use `et_al` as the last entry"
            in opt
        )

    def test_authors6(_, opt):
        assert (
            "If no author, editor, or translator is present, "
            "return an empty list for that field."
            in opt
        )

    # publisher  ---------------------------------------------------------------

    def test_publisher0(_, opt):
        assert "#### publisher" in opt

    def test_publisher1(_, opt):
        assert "A string indicating the publisher of the book." in opt

    def test_publisher2(_, opt):
        assert "Use the most relevant part of the name. E.g.:" in opt

    def test_publisher3(_, opt):
        assert "- `Harvard`, not `Harvard University Press`" in opt

    def test_publisher4(_, opt):
        assert "- `Yale`" in opt

    def test_publisher5(_, opt):
        assert "- `Macmillan`" in opt

    def test_publisher6(_, opt):
        assert "- `Allyn&Bacon`" in opt

    def test_publisher7(_, opt):
        assert "- `S.F.Masterworks`" in opt

    # ddc code  ----------------------------------------------------------------

    def test_ddc_code0(_, opt):
        assert "#### ddc_code" in opt

    def test_ddc_code1(_, opt):
        assert (
            "Use Edition 23 of Dewey Decimal Classification "
            "fit for the book, eg:"
            in opt
        )

    def test_ddc_code2(_, opt):
        assert "'330.1'" in opt

    def test_ddc_code3(_, opt):
        assert "'210'" in opt

    def test_ddc_just0(_, opt):
        assert "#### ddc_justification" in opt

    def test_ddc_just1(_, opt):
        assert (
            "A **multi-line string** explaining "
            "the DDC classification of the book."
            in opt
        )

    def test_ddc_just2(_, opt):
        assert (
            "- **First line** must state the meaning of the exact DDC number"
            in opt
        )

    def test_ddc_just3(_, opt):
        assert (
            "  - first item must be the direct parent "
            "of the exact DDC number (e.g. `741.6` for DDC `741.66`)"
            in opt
        )

    def test_ddc_just4(_, opt):
        assert "  - do not include `?00`-level DDCs (e.g. `100`, `500`)" in opt

    def test_ddc_just5(_, opt):
        assert "<ddc-justification-example1>" in opt

    def test_ddc_just6(_, opt):
        assert "</ddc-justification-example1>" in opt

    def test_ddc_just7(_, opt):
        assert "DDC of `302.23` is **Mass media**:" in opt

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

    def test_tags_shelver0(_, opt):
        assert "### tags for Shelver" in opt

    def test_tags_shelver1(_, opt):
        assert (
            "- edition or version (not year, only when exact edition is known)"
            in opt
        )

    def test_tags_shelver2(_, opt):
        assert (
            "  - use `ed[1]` for 1st edition, use `ed[2]` for 2nd edition, etc."
            in opt
        )

    def test_tags_shelver3(_, opt):
        assert "  - `ed[new]`: new edition" in opt
