PROMPTS = {
    "full": "entire prompt",
    "general": "almost like full, but without some specific-tasked roles",
    "secretary": (
        "prompt focus on everyday activity, e.g. conversation, encyclopedic,"
        " translation, etc."
    ),
    "code": "prompt include all code-writing roles",
    "python": "prompt specific for Python code assistance",
    "librarian": "create a book label and determine DDC",
    "commit": (
        "take a result of git diff, then generate an appropriate git commit"
        " message"
    ),
    "diff": "take a result of git diff, return a summary of changes",
}


PROMPT_DOC = """
predefined prompts:

{}
""".format("\n".join("- {}: {}".format(k, v) for k, v in PROMPTS.items()))


__doc__ = PROMPT_DOC

__all__ = ("get_prompt", "PROMPTS", "PROMPT_DOC")


def get_prompt(prompt_name):
    pass  # TODO
