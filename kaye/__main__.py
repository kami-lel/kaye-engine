"""
CLI entry point for Python module ``kaye``
"""

from kaye.cli.cli_main import cli_parser

if __name__ == "__main__":
    parsed_args = cli_parser.parse_args()
    parsed_args.func(parsed_args)  # call respective main function
