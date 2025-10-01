# BUG not functional


def _prompt_ls_main(_):
    # when calling ``python -m kaye prompt ls``
    print("(all available embedded blueprints:)")
    for blueprint_name in blueprint_names:
        print(blueprint_name)


LS_HELP_TEXT = "show all available embedded blueprints"
ls_psr = prompt_subpsr.add_parser(
    "ls",
    help=LS_HELP_TEXT,
    description=LS_HELP_TEXT,
)
ls_psr.set_defaults(func=_prompt_ls_main)
