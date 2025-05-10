"""
define the CLI for ``kaye``
"""

# fixme better __doc__

# TODO TODO

import argparse

# setup main parser


def _kaye_main(_):
    """
    main behvaior when calling ``python -m kaye``
    """
    kaye_psr.print_help()


kaye_psr = argparse.ArgumentParser(prog="kaye", description=__doc__)
kaye_psr.set_defaults(func=_kaye_main)
kaye_subpsr = kaye_psr.add_subparsers()


# setup subparser: kaye prompt
def _prompt_main(_):
    """
    main behvaior when calling ``python -m kaye prompt``
    """
    prompt_psr.print_help()


prompt_psr = kaye_subpsr.add_parser("prompt")
prompt_psr.set_defaults(func=_prompt_main)


# setup subparser: kaye prompt ls


if __name__ == "__main__":
    args = kaye_psr.parse_args()
    args.func(args)
