import re
import subprocess

_BASIC_FORMAT_RE = re.compile(r"^---\n(.+?)---\n(.+)", re.DOTALL)


def prepare_local_config_folder(tmp_path_factory, command, folder_name):
    config_folder = tmp_path_factory.mktemp(folder_name)

    # Execute continue export command with folder path
    cmd = command + str(config_folder)
    subprocess.run(cmd, shell=True, check=True)

    rules_folder = config_folder / "rules"

    return config_folder, rules_folder


def split_rule_file_basic_format(content):
    parts = content.split("---", 2)
    frontmatter = parts[1].strip("\n").splitlines()
    body = parts[2].strip("\n")
    return frontmatter, body


def assert_rule_file_basic_format(content):
    match = _BASIC_FORMAT_RE.match(content)
    if not match:
        return False
    frontmatter = match.group(1).strip()
    body = match.group(2).strip()
    return bool(frontmatter) and bool(body)


def assert_header_line_always_apply(lines, value):
    expected = "true" if value else "false"
    return "alwaysApply: {}".format(expected) in lines
