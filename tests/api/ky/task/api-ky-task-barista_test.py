"""
api-ky-task-barista_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with role=barista
"""

import json


import pytest


from tests.api.ky.task import *

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, task_endpoint):
    role = "barista"

    response = flask_test_client.post(
        task_endpoint,
        data=json.dumps({"role": role}),
        content_type="application/json",
    )

    opt = response.get_data().decode("utf-8")

    return opt


# Pytest unit tests  ###########################################################


class TestBarista:  # ==========================================================

    def test01(_, opt):
        assert "## Assistant Barista" in opt

    def test02(_, opt):
        assert "Maintain a coffee brewing note" in opt

    def test03(_, opt):
        assert "Transform any user-provided input" in opt

    def test04(_, opt):
        assert "Follow the required structure and format" in opt

    def test_doc(_, opt):
        assert "### document structure" in opt

    def test11(_, opt):
        assert "#### Level 1: Document Title" in opt

    def test12(_, opt):
        assert "Include only heading, must be exactly" in opt

    def test21(_, opt):
        assert "#### Level 2: Brand" in opt

    def test22(_, opt):
        assert "Include only heading, must be" in opt

    def test31(_, opt):
        assert "#### Level 3: Product" in opt

    def test32(_, opt):
        assert "Heading: `###` + coffee product name;" in opt

    def test33(_, opt):
        assert "Content may be included as a list of" in opt

    def test34(_, opt):
        assert "- `- Flavor:` roaster-provided tasting notes;" in opt

    def test41(_, opt):
        assert "#### Level 4: Batch/Bag" in opt

    def test42(_, opt):
        assert "Heading: `#### Roast:` + date of roast of" in opt

    def test43(_, opt):
        assert "Content must include bag-open date." in opt

    def test51(_, opt):
        assert "#### Level 5: Brew" in opt

    def test52(_, opt):
        assert "Heading: `##### Brew:` + date-time" in opt

    def test53(_, opt):
        assert "Third is `Experience:`, an optional" in opt

    def test_eg1(_, opt):
        assert "### example" in opt

    def test_eg2(_, opt):
        assert "- good extraction" in opt

    # rapid blueprint  *********************************************************

    def test_intro1(_, opt):
        print(opt)
        assert_intro1(opt)

    def test_intro2(_, opt):
        print(opt)
        assert_intro2(opt)

    def test_format_title(_, opt):
        print(opt)
        assert_format_title(opt)

    def test_format1(_, opt):
        print(opt)
        assert_format1(opt)

    def test_format2(_, opt):
        print(opt)
        assert_format2(opt)

    def test_format3(_, opt):
        print(opt)
        assert_format3(opt)

    def test_format4(_, opt):
        print(opt)
        assert_format4(opt)

    def test_format5(_, opt):
        print(opt)
        assert_format5(opt)

    def test_format_list1(_, opt):
        print(opt)
        assert_format_list1(opt)

    def test_format_list2(_, opt):
        print(opt)
        assert_format_list2(opt)

    def test_format_list3(_, opt):
        print(opt)
        assert_format_list3(opt)

    def test_format_math1(_, opt):
        print(opt)
        assert_format_math1(opt)

    def test_format_math2(_, opt):
        print(opt)
        assert_format_math2(opt)

    def test_format_math3(_, opt):
        print(opt)
        assert_format_math3(opt)

    def test_format_diagrams1(_, opt):
        print(opt)
        assert_format_diagrams1(opt)

    def test_format_diagrams2(_, opt):
        print(opt)
        assert_format_diagrams2(opt)

    def test_format_diagrams3(_, opt):
        print(opt)
        assert_format_diagrams3(opt)

    # abbr *********************************************************************

    def test_abbr_heading(_, opt):
        assert_abbr_heading(opt)
