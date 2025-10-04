"""generate concrete prompt from blueprint"""

from argparse import FileType, ArgumentParser

from kaye import PROGRAM_NAME, kamilog
from kaye.gen_prompt.prompt_blueprint import PromptBlueprint
from kaye.gen_prompt.prompt_blueprint_loader import (
    load_embedded_prompt_blueprint,
)
from kaye.gen_prompt.prompt_corpus_loader import load_embedded_prompt_corpus

# base parsers  ----------------------------------------------------------------
# defining args shared by gen_parser and show_parser
base_gen_show_parser = ArgumentParser(add_help=False)
# positional argument
base_gen_show_parser.add_argument(
    "BLUEPRINT",
    help="name of any embedded blueprints",
    type=str,
)
# options
base_gen_show_parser.add_argument(
    "-f",
    "--destination-file",
    metavar="FILE",
    type=FileType(mode="w"),
    nargs="?",
    help="save the result to file",
)
base_gen_show_parser.add_argument(
    "-s",
    "--source-file",
    action="store_true",
    help="provide blueprint as source file of prompt blueprint",
)
base_gen_show_parser.add_argument(
    "-C",
    "--no-comment",
    action="store_true",
    help="disable last-line prompt comment in result",
)


def _create_blueprint_from_generate_show(namespace):
    pass  # TODO use file name as blueprint display name


def register_cli_prompt_generate_parser(cli_prompt_subparser):
    """
    create cli parser for ``kaye prompt generate``,
    and add it to ``cli_prompt_ls_parser``
    """
    logger = kamilog.getLogger(PROGRAM_NAME)

    gen_parser = cli_prompt_subparser.add_parser(
        "generate",
        help=__doc__,
        description=__doc__,
        aliases=["gen"],
        parents=[base_gen_show_parser],
    )

    # add arguments  -----------------------------------------------------------
    # options
    kamilog.add_verbose_arguments(gen_parser)

    # define main function  ----------------------------------------------------
    def _prompt_generate_main(args):
        # when calling ``python -m kaye prompt gen``
        # todo interactive mode which allow user set preview line, etc.
        kamilog.set_logging_level_by_verbosity(args, PROGRAM_NAME)

        # TODO use _create_blueprint_from_generate_show

        blueprint_arg = args.BLUEPRINT

        if args.source_file:
            try:
                with open(blueprint_arg, "r", encoding="utf-8") as file:
                    file_content = file.read()

            except (FileNotFoundError, OSError) as e:
                raise ValueError(
                    'bad filename "{}" of BLUEPRINT with --source-file'.format(
                        blueprint_arg
                    )
                ) from e

            try:
                blueprint_obj = PromptBlueprint(
                    load_embedded_prompt_corpus(), file_content
                )
            except (FileNotFoundError, IOError) as err:
                logger.error(err)
                raise

        else:
            try:
                blueprint_obj = load_embedded_prompt_blueprint(blueprint_arg)
            except (FileNotFoundError, IOError, ValueError) as err:
                logger.error(err)
                raise

        prompt_content = blueprint_obj.generate_prompt(
            hide_comment=args.no_comment
        )

        # with --file FILE
        if args.file:
            with args.file as f:
                f.write(prompt_content)
        else:
            print(prompt_content)

    gen_parser.set_defaults(func=_prompt_generate_main)
