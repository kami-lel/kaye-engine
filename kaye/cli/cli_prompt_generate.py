"""generate concrete prompt from blueprint"""

from argparse import FileType

from kaye.gen_prompt.prompt_blueprint import PromptBlueprint
from kaye.gen_prompt.prompt_blueprint_loader import (
    load_embedded_prompt_blueprint,
)
from kaye.gen_prompt.prompt_corpus_loader import load_embedded_prompt_corpus

# Todo use logger to handle print & raise


def register_cli_prompt_generate_parser(cli_prompt_subparser):
    """
    create cli parser for ``kaye prompt generate``,
    and add it to ``cli_prompt_ls_parser``
    """

    gen_parser = cli_prompt_subparser.add_parser(
        "generate", help=__doc__, description=__doc__, aliases=["gen"]
    )

    # add arguments  -----------------------------------------------------------
    # positional argument
    gen_parser.add_argument(
        "BLUEPRINT",
        help="name of any embedded blueprints",
        type=str,
    )
    # options
    gen_parser.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        type=FileType(mode="w"),
        nargs="?",
        help="save the result to file",
    )
    gen_parser.add_argument(
        "-l",
        "--preview-line-count",
        metavar="LINE_COUNT",
        type=int,
        nargs="?",
        help="maximum line count for each entry in blueprint preview",
        default=None,
    )
    gen_parser.add_argument(
        "-w",
        "--preview-line-width",
        metavar="LINE_WIDTH",
        type=int,
        nargs="?",
        help="maximum line width for each entry in blueprint preview",
        default=None,
    )
    gen_parser.add_argument(
        "-F",
        "--source-file",
        action="store_true",
        help="provide blueprint as source file of prompt blueprint",
    )
    gen_parser.add_argument(
        "-C",
        "--no-comment",
        action="store_true",
        help="disable last-line prompt comment in result",
    )

    # define main function  ----------------------------------------------------
    def _prompt_generate_main(args):
        # when calling ``python -m kaye prompt gen``
        # todo interactive mode which allow user set preview line, etc.

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

            blueprint_obj = PromptBlueprint(
                load_embedded_prompt_corpus(), file_content
            )

        else:
            blueprint_obj = load_embedded_prompt_blueprint(blueprint_arg)

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
