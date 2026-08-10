"""
Entry Point for Kaye Engine CLI
"""

from kaye_engine.cli.cli_main import register_cli_main_parser

# Todo support --version


# pylint: disable-next=missing-function-docstring
def main():
    cli_parser, _ = register_cli_main_parser()
    parsed_args = cli_parser.parse_args()
    parsed_args.func(parsed_args)  # call respective main function


# Main Entry Point  ############################################################
if __name__ == "__main__":
    main()
