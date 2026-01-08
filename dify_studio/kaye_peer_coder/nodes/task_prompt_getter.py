from enum import IntFlag, auto

# constants  ###################################################################
PROMPT_KEY_IN_CACHE = "task_prompt"
FLAGS_KEY_IN_CACHE = "flags"
OUTPUT_PROMPT_KEY = "task_prompt"
OUTPUT_CACHES_KEY = "updated_caches"


class PL(IntFlag):
    """
    represent a single programming language
    """

    NONE = 0

    # pylint: disable=invalid-name

    # abbreviations defined in prompt corpus
    c = auto()
    cpp = auto()
    ue = auto()
    csharp = auto()
    u3d = auto()
    console = auto()
    css = auto()
    html = auto()
    js = auto()
    ts = auto()
    py = auto()


def _calc_flags(languages):
    flags = PL.NONE

    if languages:  # when languages list is not empty
        for lang in languages.split(","):
            flags |= PL[lang]

    return flags


def main(languages: str, caches: dict):
    flags = _calc_flags(languages)

    try:
        cached_flags = PL(int(caches[FLAGS_KEY_IN_CACHE]))
    except KeyError:
        cached_flags = PL.NONE

    if flags == cached_flags and cached_flags:
        # identical language requirement, thus send cached prompt
        return {
            OUTPUT_PROMPT_KEY: caches[PROMPT_KEY_IN_CACHE],
            OUTPUT_CACHES_KEY: caches,
        }

    # get prompt  --------------------------------------------------------------
    flags |= cached_flags  # combined with previous languages

    if flags == 0:  # no programming
        task_prompt = "basic"  # Todo use API

    else:
        # contains additional required languages
        task_prompt = "basic + {}".format(repr(flags))  # Todo use API

    # update Conversation Variable caches
    caches[FLAGS_KEY_IN_CACHE] = flags
    caches[PROMPT_KEY_IN_CACHE] = task_prompt

    return {
        OUTPUT_PROMPT_KEY: task_prompt,
        OUTPUT_CACHES_KEY: caches,
    }
