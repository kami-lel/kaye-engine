"""
blueprint_io_parser.py

define ``blueprint_io_parser``
"""

from argparse import FileType, ArgumentParser

# defining args shared by generate_parser and show_parser
blueprint_io_parser = ArgumentParser(add_help=False)
# positional argument
blueprint_io_parser.add_argument(
    "BLUEPRINT",
    help="embedded blueprints name",
    type=str,
)
# options
blueprint_io_parser.add_argument(
    "-f",
    "--source-file",
    action="store_true",
    help="load blueprint from path BLUEPRINT",
)
blueprint_io_parser.add_argument(
    "-F",
    "--target-file",
    metavar="FILE",
    type=FileType(mode="w"),
    nargs="?",
    help="save result to FILE",
)
blueprint_io_parser.add_argument(
    "-C",
    "--no-comment",
    action="store_true",
    help="disable last-line comment in result",
)
