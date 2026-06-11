import re
import subprocess

# Hack replaced with use all_md_filenames
RULE_FILES = [
    "Abbr Currency Symbols.md",
    "Abbr Natural Language Codes.md",
    "Abbr Prefixes.md",
    "Abbr Programming Language Codes.md",
    "Abbr Single Character.md",
    "Abbr Emoji.md",
    "Abbr Starts with A.md",
    "Abbr Starts with B.md",
    "Abbr Starts with C.md",
    "Abbr Starts with D.md",
    "Abbr Starts with Digits 0~9.md",
    "Abbr Starts with E.md",
    "Abbr Starts with F.md",
    "Abbr Starts with G.md",
    "Abbr Starts with H.md",
    "Abbr Starts with I.md",
    "Abbr Starts with K.md",
    "Abbr Starts with L.md",
    "Abbr Starts with M.md",
    "Abbr Starts with N.md",
    "Abbr Starts with O.md",
    "Abbr Starts with P.md",
    "Abbr Starts with Q.md",
    "Abbr Starts with R.md",
    "Abbr Starts with S.md",
    "Abbr Starts with T.md",
    "Abbr Starts with U.md",
    "Abbr Starts with V.md",
    "Abbr Starts with W.md",
    "Abbr Starts with X.md",
    "Abbr Starts with Y.md",
    "Abbr Starts with Non-Alphanumeric.md",
    "Abbr Suffixes.md",
    "Abbr Symbols.md",
    "Abbr Units of Measure.md",
    "Annotation Markers.md",
    "Chat.md",
    "Coder Bash.md",
    "Kaye Peer Coder.md",
    "Coder C.md",
    "Project CHANGELOG Writer.md",
    "Project AGENTS Writer.md",
    "Project README Writer.md",
    "Coder CPP.md",
    "Coder C Sharp.md",
    "Coder GDScript.md",
    "Coder HTML.md",
    "Coder JavaScript and TypeScript.md",
    "Project Structure.md",
    "Coder Python.md",
    "Coder Python Docstring Style.md",
    "Coder Python Testing Guidelines.md",
    "Coder Unity Engine.md",
    "Coder Unreal Engine.md",
    "Continue Behavior.md",
    "Date and Time Format.md",
    "Numerical Values with Units.md",
    "Style Guide.md",
]

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
