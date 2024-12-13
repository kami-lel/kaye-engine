"""generate one of the predefined prompts as whole or a subset of prompt full
"""


PROGRAM_NAME = 'kaye.get_prompt'

from argparse import ArgumentParser, RawTextHelpFormatter, FileType
from sys import stderr, stdout
import errno

from .generate_prompt import get_prompt
from .generate_prompt import __doc__ as prompt_doc


psr = ArgumentParser(prog=PROGRAM_NAME,
        description=__doc__ + prompt_doc, formatter_class=RawTextHelpFormatter)


# positional arguments
psr.add_argument('PROMPT',
        help='name of a predefined prompt')


# options
psr.add_argument('-f', '--file',
        action='store',
        type=FileType('w'),
        required=False,
        metavar='DESTINATION',
        help='save the generated prompt content into DESTINATION')


if __name__ == "__main__":
    args = psr.parse_args()

    dest = args.file or stdout

    try:
        content = get_prompt(args.PROMPT)
        print(content, file=dest)

    except ValueError as err:
        print("Error: "+ err.args[0], file=stderr)
        exit(errno.EINVAL)

    exit(0)
