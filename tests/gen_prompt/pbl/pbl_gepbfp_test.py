"""
test function ``get_embedded_prompt_blueprints_folder_path()``
"""

from os.path import dirname, abspath, join, normpath

from kaye.gen_prompt import get_embedded_prompt_blueprints_folder_path


class Test:
    def test1(_):  # !!! this test change with folder prompt_blueprints

        submission = get_embedded_prompt_blueprints_folder_path()
        solution = normpath(
            join(
                dirname(abspath(__file__)),
                "../../../kaye/gen_prompt/prompt_blueprints",
            )
        )
        print("submission:\t{}\nsolution:\t{}".format(submission, solution))
        assert str(submission) == solution
