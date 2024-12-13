"""TODO
"""

PROGRAM_NAME = 'kaye.update_vs_code'


from argparse import ArgumentParser, RawTextHelpFormatter


from get_prompt import get_prompt


# TODO update vscode prompts & update model


psr = ArgumentParser(prog=PROGRAM_NAME,
        description=__doc__, formatter_class=RawTextHelpFormatter)


# positional arguments
psr.add_argument('PROMPT',
        help='PROMPT name')


if __name__ == "__main__":
    args = psr.parse_args()


    exit(0)
