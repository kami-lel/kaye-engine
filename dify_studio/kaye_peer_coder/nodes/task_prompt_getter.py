from enum import Flag, auto

TASK_PROMPT_KEY = "task_prompt"


class Language(Flag):
    """
    represent a single programming language
    """

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


def main(languages: dict, task_prompt_flags: float, task_prompt_cache: str):

    # TODO
    task_prompt = ""

    return {TASK_PROMPT_KEY: task_prompt}
