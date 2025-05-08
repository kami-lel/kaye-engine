"""test"""

# Todo docstring

import sys


from argparse import ArgumentParser

PROGRAM_NAME = "kaye.gen_prompt"

psr = ArgumentParser(prog=PROGRAM_NAME, description=__doc__)

ls_psr = psr.add_subparsers(dest="ls")


# positional argument
# options


if __name__ == "__main__":
    args = psr.parse_args()

    # TODO ls prompts
    # TODO prompt name => prompt content
    # TODO interactive mode
    # TODO corpus from

    sys.exit()
