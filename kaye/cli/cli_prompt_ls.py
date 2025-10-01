"""show all available embedded blueprints"""

from kaye.gen_prompt import get_embedded_prompt_blueprints_names


def register_cli_prompt_ls_parser(cli_prompt_subparser):
    cli_prompt_ls_parser = cli_prompt_subparser.add_parser(
        "ls", help=__doc__, description=__doc__
    )

    def _cli_prompt_ls_main(_):
        # when calling ``python -m kaye prompt ls``
        print("(all available embedded blueprints:)")
        for blueprint_name in get_embedded_prompt_blueprints_names():
            print(blueprint_name)

    cli_prompt_ls_parser.set_defaults(func=_cli_prompt_ls_main)
