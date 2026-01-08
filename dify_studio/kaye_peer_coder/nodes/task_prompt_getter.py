from enum import IntFlag, auto

TASK_PROMPT_KEY = "task_prompt"


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
    # TODO docstring
    flags = PL.NONE
    for lang in languages:
        flags |= PL[lang]
    return flags


def main(languages: dict, task_prompt_flags: float, task_prompt_cache: str):
    flags = _calc_flags(languages)
    cached_flags = PL(int(task_prompt_flags))

    if flags == 0:  # no programming
        task_prompt = ""  # TODO

    elif flags not in cached_flags:
        # contains additional required languages
        task_prompt = ""  # TODO

    else:
        # sending the cached/same prompt
        task_prompt = task_prompt_cache

    return {TASK_PROMPT_KEY: task_prompt}
