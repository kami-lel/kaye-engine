ENV_VAR_TOKEN = "VSC_SETTING_JSON_PATH"

__doc__ = """modify settings.json file of VS code, 
specified by an enviornment variable {}
""".format(ENV_VAR_TOKEN)


PROGRAM_NAME = "kaye.update_vsc"
SYSTEM_MESSAGE_KEY = "genieai.systemMessage"  # in settings.json
COMMIT_MESSAGE_KEY = "genieai.promptPrefix.commit-message"


from argparse import ArgumentParser, RawTextHelpFormatter, FileType
from os import getenv
import errno
from sys import stderr
import json

from kaye.get_prompt import get_prompt, PROMPTS, PROMPT_DOC


psr = ArgumentParser(
    prog=PROGRAM_NAME,
    description=__doc__ + PROMPT_DOC,
    formatter_class=RawTextHelpFormatter,
)


# positional arguments
psr.add_argument(
    "PROMPT", choices=list(PROMPTS.keys()), help="name of a predefined prompt"
)


# options
psr.add_argument(
    "-f",
    "--file",
    action="store",
    type=FileType("r+"),
    required=False,
    metavar="SETTING_JSON",
    help="update settings.json at SETTING_JSON, instead default location",
)
psr.add_argument(
    "-c",
    "--change-commit-message",
    action="store_true",
    help="update Commit Message",
)
psr.add_argument("-v", "--verbose", action="store_true", required=False)


if __name__ == "__main__":
    args = psr.parse_args()

    # generate the prompt
    try:
        content = get_prompt(args.PROMPT)
    except ValueError as err:
        print(
            "Error: {} of arg PROMPT not recognized".format(args.PROMPT),
            file=stderr,
        )
        exit(errno.EINVAL)

    # decide where settings.json is
    if args.file:
        dest = args.file.name
    elif getenv(ENV_VAR_TOKEN):
        dest = getenv(ENV_VAR_TOKEN)
    else:
        print(
            "Error: enviornment variable {} not set".format(ENV_VAR_TOKEN),
            file=stderr,
        )
        exit(errno.ENONET)

    # update the file
    try:
        with open(dest, "r", encoding="utf-8", newline="") as file:
            data = json.load(file)

    except json.JSONDecodeError as err:
        print("Error: JSON: {}".format(err.args[0]), file=stderr)
        exit(errno.EINVAL)
    except (FileNotFoundError, PermissionError) as err:
        print("Error: {}: {}".format(err.args[1], dest))
        exit(err.errno)

    key = (
        COMMIT_MESSAGE_KEY
        if args.change_commit_message
        else SYSTEM_MESSAGE_KEY
    )
    data[key] = content

    with open(dest, "w", encoding="utf-8", newline="") as file:
        json.dump(data, file, indent=4)

    if args.verbose:
        print(
            "prompt {} saved into VS code settins: {}".format(
                args.PROMPT, dest
            )
        )

    exit(0)
