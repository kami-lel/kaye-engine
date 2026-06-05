"""
Entry Point for Kaye Flask HTTP API
"""

import argparse

from kaye import PROGRAM_NAME

from kaye.api import create_app

from kaye.cli.cli_main import cli_parser

# constants  ###################################################################
HOST = "0.0.0.0"
PORT = 11255
DEBUG_PORT = 11256


# argparse  ####################################################################
parser = argparse.ArgumentParser(prog=PROGRAM_NAME)
parser.add_argument(
    "-d",
    "--debug",
    action="store_true",
    help="enable debug, port changed to {}".format(DEBUG_PORT),
)


# Entry Point  #################################################################
if __name__ == "__main__":
    # FIXME make sub parser: kaye api
    # args = parser.parse_args()

    # app = create_app()
    # app.run(
    #     host=HOST, port=DEBUG_PORT if args.debug else PORT, debug=args.debug
    # )

    parsed_args = cli_parser.parse_args()
    parsed_args.func(parsed_args)  # call respective main function
