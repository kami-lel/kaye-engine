"""TODO
"""

PROGRAM_NAME = 'kaye.update_vs_code'


from argparse import ArgumentParser, RawTextHelpFormatter, FileType


from kaye.get_prompt import get_prompt
from kaye.get_prompt.generate_prompt import __doc__ as prompt_doc


psr = ArgumentParser(prog=PROGRAM_NAME,
        description=__doc__ + prompt_doc,
        formatter_class=RawTextHelpFormatter)


# positional arguments
psr.add_argument('PROMPT',
        help='name of a predefined prompt')


# options
psr.add_argument('-f', '--file',
        action='store',
        type=FileType('w'),
        required=False,
        metavar='SETTING_JSON',
        help='')  # TODO docstring



if __name__ == "__main__":
    args = psr.parse_args()

    # TODO err ini file no good

    exit(0)
