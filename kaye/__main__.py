"""
Entry Point for Kaye Flask HTTP API
"""

from kaye.cli.cli_main import cli_parser

# Entry Point  #################################################################
if __name__ == "__main__":
    parsed_args = cli_parser.parse_args()
    parsed_args.func(parsed_args)  # call respective main function
