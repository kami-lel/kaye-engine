"""generate concrete prompt from blueprint"""

from argparse import FileType, ArgumentParser
from pathlib import Path

from kaye import PROGRAM_NAME, kamilog
from kaye.gen_prompt.prompt_blueprint import PromptBlueprint
from kaye.gen_prompt.prompt_blueprint_loader import (
    load_embedded_prompt_blueprint,
)
from kaye.gen_prompt.prompt_corpus_loader import load_embedded_prompt_corpus

logger = kamilog.getLogger(PROGRAM_NAME)

# base parsers  ----------------------------------------------------------------
# defining args shared by gen_parser and show_parser
base_gen_show_parser = ArgumentParser(add_help=False)
# positional argument
base_gen_show_parser.add_argument(
    "BLUEPRINT",
    help="embedded blueprints name",
    type=str,
)
# options
base_gen_show_parser.add_argument(
    "-f",
    "--destination-file",
    metavar="FILE",
    type=FileType(mode="w"),
    nargs="?",
    help="save result to FILE",
)
base_gen_show_parser.add_argument(
    "-s",
    "--source-file",
    action="store_true",
    help="load blueprint from path BLUEPRINT",
)
base_gen_show_parser.add_argument(
    "-C",
    "--no-comment",
    action="store_true",
    help="disable last-line comment in result",
)


def create_blueprint_from_generate_show(args):
    """
    :param args: parsed from ``gen_parser`` or ``show_parser``
    :type args: argparse.Namespace
    :return: create a blueprint object from cli,
            shared by ``gen_parser`` and ``show_parser``
    :rtype: PromptBlueprint
    """

    blueprint_arg = args.BLUEPRINT

    if args.source_file:  # load from file
        try:
            with open(blueprint_arg, "r", encoding="utf-8") as file:
                file_content = file.read()

        except (FileNotFoundError, OSError) as err:
            err2 = ValueError(
                'bad filename "{}" of BLUEPRINT with --source-file'.format(
                    blueprint_arg
                )
            )
            err2.__cause__ = err
            logger.critical(err2)
            raise

        filename = Path(blueprint_arg).stem

        try:
            return PromptBlueprint(
                load_embedded_prompt_corpus(),
                file_content,
                display_name=filename,
            )
        except (FileNotFoundError, IOError, ValueError) as err:
            logger.error(err)
            raise

    else:  # embedded blueprints
        try:
            return load_embedded_prompt_blueprint(blueprint_arg)
        except (FileNotFoundError, IOError, ValueError) as err:
            logger.error(err)
            raise


def register_cli_prompt_generate_parser(cli_prompt_subparser):
    """
    create cli parser for ``kaye prompt generate``,
    and add it to ``cli_prompt_ls_parser``
    """

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

        blueprint = create_blueprint_from_generate_show(args)

        prompt_content = blueprint.generate_prompt(
            hide_comment=args.no_comment
        )

        # with --destination-file FILE
        if args.destination_file:
            with args.destination_file as f:
                f.write(prompt_content)

            logger.debug(
                "rendered blueprint prompt save to: %s",
                args.destination_file.name,
            )

        else:
            logger.debug("render blueprint prompt")
            print(prompt_content)

    gen_parser.set_defaults(func=_prompt_generate_main)
