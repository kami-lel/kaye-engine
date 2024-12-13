"""modify settings.json file of VS code
"""

PROGRAM_NAME = 'kaye.update_vs_code'
SYSTEM_MESSAGE_KEY = 'genieai.systemMessage'  # in settings.json


from argparse import ArgumentParser, RawTextHelpFormatter, FileType
import platform
from os import getenv
from os.path import join, abspath, realpath, expanduser
import errno
from sys import stderr
import json

from kaye.get_prompt import get_prompt
from kaye.get_prompt.generate_prompt import __doc__ as prompt_doc


def _find_vscode_setting_json_file_default_location():
    """
    find the default location of the settings.json file for Visual Studio Code

    :return: path to the settings.json file
    :retype: str
    """
    os_type = platform.system()

    if os_type == 'Windows':
        return realpath(abspath(join(
                getenv('APPDATA'), 'Code', 'User', 'settings.json')))

    elif os_type == 'Linux':
        return realpath(abspath(expanduser(
                '~/.config/Code/User/settings.json')))

    else:
        print("Error: can not find settings.json default location on {}"
                .format(os_type), file=stderr)
        exit(errno.EPERM)


psr = ArgumentParser(prog=PROGRAM_NAME,
        description=__doc__ + prompt_doc,
        formatter_class=RawTextHelpFormatter)


# positional arguments
psr.add_argument('PROMPT',
        help='name of a predefined prompt')


# options
psr.add_argument('-f', '--file',
        action='store',
        type=FileType('r+'),
        required=False,
        metavar='SETTING_JSON',
        help='update settings.json at SETTING_JSON, instead default location')


if __name__ == "__main__":
    args = psr.parse_args()

    # generate the prompt
    try:
        content = get_prompt(args.PROMPT)
    except ValueError as err:
        print('Error: {} of arg PROMPT not recognized'
                .format(args.PROMPT), file=stderr)
        exit(errno.EINVAL)

    # decide where settings.json is
    dest = args.file.name if args.file else \
            _find_vscode_setting_json_file_default_location()

    # update the file
    try:
        with open(dest, 'r', encoding='utf-8', newline='') as file:
            data = json.load(file)

    except json.JSONDecodeError as err:
        print('Error: JSON: {}'.format(err.args[0]), file=stderr)
        exit(errno.EINVAL)
    except (FileNotFoundError, PermissionError) as err:
        print('Error: {}: {}'.format(err.args[1], dest))
        exit(err.errno)

    data[SYSTEM_MESSAGE_KEY] = content

    with open(dest, 'w', encoding='utf-8', newline='') as file:
        json.dump(data, file, indent=4)

    print('VS code settins updated: {}'.format(dest))

    exit(0)
