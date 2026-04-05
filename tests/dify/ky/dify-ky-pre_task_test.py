"""
dify-ky-pre_task_test.py

Unit Tests (using pytest) for:

``pre_task`` node of Kaye Chat Dify App
"""

import json


from dify_studio.kaye_chat.nodes import pre_task
from dify_studio.kaye_chat.nodes.pre_task import (
    OUTPUT_BODY_KEY,
    OUTPUT_DIRECT_KEY,
    OUTPUT_LLMS_KEY,
)

# helpers  #####################################################################


def _assert_structure(opt):
    assert OUTPUT_BODY_KEY in opt
    assert isinstance(opt[OUTPUT_BODY_KEY], str)
    assert OUTPUT_LLMS_KEY in opt
    assert isinstance(opt[OUTPUT_LLMS_KEY], list)
    assert all(isinstance(e, str) for e in opt)
    assert OUTPUT_DIRECT_KEY in opt
    assert isinstance(opt[OUTPUT_DIRECT_KEY], bool)


# Pytest unit tests  ###########################################################


class TestBody:  # =============================================================

    def test1(_):
        pass  # TODO
