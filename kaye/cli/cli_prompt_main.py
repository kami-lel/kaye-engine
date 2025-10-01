# BUG not functional


def _prompt_main(_):
    # when calling ``python -m kaye prompt``
    prompt_psr.print_help()


PROMPT_HELP_TEXT = (
    "dynamically generate AI system prompt with a prompt blueprint"
    " as a subset of the prompt corpus"
)
prompt_psr = kaye_subpsr.add_parser(
    "prompt",
    help=PROMPT_HELP_TEXT,
    description=PROMPT_HELP_TEXT,
    aliases=["p"],
)

prompt_psr.set_defaults(func=_prompt_main)
prompt_subpsr = prompt_psr.add_subparsers(
    description="utility functions related to prompt generation"
)
