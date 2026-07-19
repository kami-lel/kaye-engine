"""list names of all available embedded blueprints"""

from kaye import PROGRAM_NAME, kamilog
from kaye.prompt.blueprint import get_embedded_prompt_blueprints_names


def register_cli_prompt_ls_parser(cli_prompt_subparser):
    """
    create cli parser for ``kaye prompt ls``,
    and add it to ``cli_prompt_ls_parser``
    """
    logger = kamilog.getLogger(PROGRAM_NAME)

    ls_parser = cli_prompt_subparser.add_parser(
        "ls", help=__doc__, description=__doc__
    )

    def _cli_prompt_ls_main(_):
        # when calling ``python -m kaye prompt ls``
        try:
            blueprint_names = get_embedded_prompt_blueprints_names()
        except (FileNotFoundError, OSError) as err:
            logger.error(err)
            raise

        for blueprint_name in blueprint_names:
            print(blueprint_name)

    ls_parser.set_defaults(func=_cli_prompt_ls_main)
