"""
Entry Point for Kaye Flask HTTP API
"""

from kaye_engine.cli.cli_main import cli_parser


# pylint: disable-next=missing-function-docstring
def main():
    parsed_args = cli_parser.parse_args()
    parsed_args.func(parsed_args)  # call respective main function


# Entry Point  #################################################################
if __name__ == "__main__":
    main()
