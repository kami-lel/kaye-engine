"""test"""

# todo docstring

import sys


from argparse import ArgumentParser

PROGRAM_NAME = "kaye.gen_prompt"

psr = ArgumentParser(prog=PROGRAM_NAME, description=__doc__)

ls_psr = psr.add_subparsers(dest="ls")


# positional argument
# options


if __name__ == "__main__":
    args = psr.parse_args()

    # todo ls prompts
    # todo prompt name => prompt content
    # todo interactive mode
    # todo corpus from

    sys.exit()
