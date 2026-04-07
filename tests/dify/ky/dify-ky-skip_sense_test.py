"""
dify-ky-skip_sense_test.py

Unit Tests (using pytest) for:

``skip_sense`` node of Kaye Chat Dify App
"""

from dify_studio.kaye_chat.nodes.sense import skip_sense
from dify_studio.kaye_chat.nodes.sense.skip_sense import (
    OUTPUT_ROLE_KEY,
    OUTPUT_DIFF_KEY,
)

# helpers  #####################################################################


def _assert_structure(opt):
    assert OUTPUT_ROLE_KEY in opt
    assert isinstance(opt[OUTPUT_ROLE_KEY], str)
    assert OUTPUT_DIFF_KEY in opt
    assert isinstance(opt[OUTPUT_DIFF_KEY], float)


# Pytest unit tests  ###########################################################
