"""
dify-ky-pre_sense_test.py

Unit Tests (using pytest) for:

``pre_sense`` node of Kaye Chat Dify App
"""

import json


import pytest


from dify_studio.kaye_chat.nodes.sense import pre_sense
from dify_studio.kaye_chat.nodes.sense.pre_sense import OUTPUT_BODY_KEY

# helpers  #####################################################################


# Pytest fixtures  #############################################################
@pytest.fixture
def kwargs():
    return {"current_role": "", "difficulty_override": 0, "query": ""}


# Pytest unit tests  ###########################################################


# TODO unit test for pre_sense


class TestBody:

    def test1(_, kwargs):

        opt = pre_sense.main(**kwargs)
        print(opt)

        body = json.loads(opt[OUTPUT_BODY_KEY])
        print(body)

        assert body == {"pre_sense_role": "", "difficulty_override": 0}

    def test2(_, kwargs):

        opt = pre_sense.main(**kwargs)
        print(opt)

        body = json.loads(opt[OUTPUT_BODY_KEY])
        print(body)

        assert body == {"pre_sense_role": "", "difficulty_override": 50}

    def test4(_, opt_coder_dft):

        opt = pre_sense.main(**kwargs)
        print(opt)

        opt = opt_coder_dft
        body = json.loads(opt[OUTPUT_BODY_KEY])
        print(body)

        assert body == {"pre_sense_role": "coder", "difficulty_override": 0}
