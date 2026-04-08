from dify_studio.kaye_chat.nodes.sense.post_start import (
    OUTPUT_SKIP_KEY,
    OUTPUT_ROLE_KEY,
    OUTPUT_DIFF_KEY,
    OUTPUT_SENSE_BODY_KEY,
)

# helpers  #####################################################################


def _assert_structure(opt):
    assert OUTPUT_SKIP_KEY in opt
    assert isinstance(opt[OUTPUT_SKIP_KEY], bool)
    assert OUTPUT_ROLE_KEY in opt
    assert isinstance(opt[OUTPUT_SENSE_BODY_KEY], str)
    assert OUTPUT_DIFF_KEY in opt
    assert isinstance(opt[OUTPUT_DIFF_KEY], int)
    assert OUTPUT_SENSE_BODY_KEY in opt
    assert isinstance(opt[OUTPUT_SENSE_BODY_KEY], str)
