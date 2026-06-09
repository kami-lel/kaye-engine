import re
import subprocess

RULE_FILES = [
    "abbr-currency_symbol.md",
    "abbr-language_code.md",
    "abbr-prefix.md",
    "abbr-programming_language_code.md",
    "abbr-starts_with-a.md",
    "abbr-starts_with-b.md",
    "abbr-starts_with-c.md",
    "abbr-starts_with-d.md",
    "abbr-starts_with-digits.md",
    "abbr-starts_with-e.md",
    "abbr-starts_with-f.md",
    "abbr-starts_with-g.md",
    "abbr-starts_with-h.md",
    "abbr-starts_with-i.md",
    "abbr-starts_with-k.md",
    "abbr-starts_with-l.md",
    "abbr-starts_with-m.md",
    "abbr-starts_with-n.md",
    "abbr-starts_with-o.md",
    "abbr-starts_with-other.md",
    "abbr-starts_with-p.md",
    "abbr-starts_with-q.md",
    "abbr-starts_with-r.md",
    "abbr-starts_with-s.md",
    "abbr-starts_with-t.md",
    "abbr-starts_with-u.md",
    "abbr-starts_with-v.md",
    "abbr-starts_with-w.md",
    "abbr-starts_with-x.md",
    "abbr-starts_with-y.md",
    "abbr-suffix.md",
    "abbr-symbol.md",
    "abbr-unit_of_measure.md",
    "Annotation Markers.md",
    "Chat.md",
    "Coder Bash.md",
    "Kaye Peer Coder.md",
    "Coder C.md",
    "Coder CHANGELOG Writer.md",
    "Coder AGENTS Writer.md",
    "Coder README Writer.md",
    "Coder CPP.md",
    "Coder C Sharp.md",
    "Coder GDScript.md",
    "Coder HTML.md",
    "Coder JavaScript and TypeScript.md",
    "Coder Project Structure.md",
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
