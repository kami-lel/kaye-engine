"""test"""

# todo docstring

from kaye.__main__ import kaye_subpsr

prompt_psr = kaye_subpsr.add_parser("prompt")
prompt_subpsr = prompt_psr.add_subparsers()


ls_psr = prompt_subpsr.add_parser("ls")
ls_psr.set_defaults()


def prompt_main(args):
    args
    pass


if __name__ == "__main__":
    pass

# TODO TODO
