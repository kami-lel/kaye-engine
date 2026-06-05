"""Kaye HTTP API: start Flask server/app"""

from kaye.api import create_app

# constants  ###################################################################
_HOST = "0.0.0.0"
_PORT = 11255
_DEBUG_PORT = 11256


def register_cli_http_parser(  #################################################
    cli_subparser,
):  # pylint: disable=missing-function-docstring
    http_parser = cli_subparser.add_parser(
        "http", help=__doc__, description=__doc__, aliases=["h"]
    )

    http_parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="enable debug, port changed to {}".format(_DEBUG_PORT),
    )

    def _http_main(args):
        app = create_app()
        app.run(
            host=_HOST,
            port=_DEBUG_PORT if args.debug else _PORT,
            debug=args.debug,
        )

    http_parser.set_defaults(func=_http_main)
