"""
Entry Point for Kaye Flask HTTP API
"""

import argparse

from kaye import PROGRAM_NAME

from kaye.api import create_app

# constants  ###################################################################
HOST = "0.0.0.0"
PORT = 11255
DEBUG_PORT = 11256


# argparse  ####################################################################
parser = argparse.ArgumentParser(prog=PROGRAM_NAME)
parser.add_argument(
    "-x",
    "--debug",
    action="store_true",
    help="enable debug, port changed to {}".format(DEBUG_PORT),
)


# Entry Point  #################################################################
if __name__ == "__main__":
    args = parser.parse_args()

    app = create_app()
    app.run(
        host=HOST, port=DEBUG_PORT if args.debug else PORT, debug=args.debug
    )
