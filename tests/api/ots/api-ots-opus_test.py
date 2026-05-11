"""
api-ots-opus_test.py

Unit Tests (using pytest) for:

/kaye/dify-app/opus-tag-smith/opus
"""

import pytest

# Pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, dify_app_endpoint):
    endpoint = dify_app_endpoint + "/opus-tag-smith/opus"
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

    def test_title5(_, opt, title5):
        assert title5 in opt

    def test_title6(_, opt, title6):
        assert title6 in opt

    def test_title7(_, opt, title7):
        assert title7 in opt

    def test_title8(_, opt, title8):
        assert title8 in opt

    def test_title9(_, opt, title9):
        assert title9 in opt

    def test_title10(_, opt, title10):
        assert title10 in opt

    def test_title11(_, opt, title11):
        assert title11 in opt

    def test_title12(_, opt, title12):
        assert title12 in opt

    def test_title13(_, opt, title13):
        assert title13 in opt

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

    def test_tags_cm3(_, opt, tags_cm3):
        assert tags_cm3 in opt

    def test_tags_cm4(_, opt, tags_cm4):
        assert tags_cm4 in opt

    # tags unique  -------------------------------------------------------------

    def test_tags0(_, opt):
        assert "### tags for Opus" in opt

    def test_tags1(_, opt):
        assert "- `web`: include WEB-DL, WEBRip" in opt

    def test_tags2(_, opt):
        assert "- `Amzn`: from Amazon Prime Video" in opt

    def test_tags3(_, opt):
        assert "- `RM`: remastered" in opt

    def test_tags4(_, opt):
        assert "- `UCut`: Ultimate Cut" in opt

    def test_tags5(_, opt):
        assert (
            "  - `H264`: H.264, x264, MPEG-4 Part 10, "
            "Advanced Video Coding, AVC"
            in opt
        )

    def test_tags6(_, opt):
        assert "  - `Xvid`" in opt

    def test_tags7(_, opt):
        assert "  - `HDR10`: 10-bit" in opt

    def test_tags8(_, opt):
        assert "- audio encoding:" in opt

    def test_tags9(_, opt):
        assert "  - `AC-3`: Dolby AC-3" in opt

    def test_tags10(_, opt):
        assert "  - `Opus`: libopus" in opt

    def test_tags11(_, opt):
        assert "- `MAL`: multiple audio languages, use when: MULTi" in opt

    def test_tags12(_, opt):
        assert "- `repack`: REPACK" in opt

    def test_tags13(_, opt):
        assert "- `RARBG`" in opt
