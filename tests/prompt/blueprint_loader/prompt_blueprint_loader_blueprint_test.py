"""
test function ``get_embedded_prompt_blueprints_folder_path()`` & ``get_embedded_prompt_blueprints_names()``
"""

# BUG BUG tests

import os

from kaye.gen_prompt import (
    get_embedded_prompt_blueprints_folder_path,
    get_embedded_prompt_blueprints_names,
)

blueprints_folder_path = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../kaye/gen_prompt/embedded_blueprints",
    )
)
non_tech_blueprints = set(
    os.path.splitext(name)[0] for name in os.listdir(blueprints_folder_path)
)


class TestGEPBFP:  # get_embedded_prompt_blueprints_folder_path()

    def test1(_):
        submission = get_embedded_prompt_blueprints_folder_path()
        print(submission)
        assert str(submission) == blueprints_folder_path


class TestGEPBN:  # get_embedded_prompt_blueprints_names

    def test_dft(_):
        opt = get_embedded_prompt_blueprints_names()
        print(opt)
        expected = non_tech_blueprints.copy()
        expected.update({"full", "empty"})
        assert set(opt) == expected

    def test_exclude(_):  # exclude tech blueprints
        opt = get_embedded_prompt_blueprints_names(
            exclude_technical_blueprint=True
        )
        print(opt)
        # Assert that both lists contain the same elements regardless of order
        assert set(opt) == non_tech_blueprints
