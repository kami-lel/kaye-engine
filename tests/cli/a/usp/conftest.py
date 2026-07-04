import subprocess

import pytest

# Pytest fixtures  #############################################################


def export_claude_md(tmp_path_factory, cli_claude_command, flags=""):
    """
    run ``kaye claude user-system-prompt`` with the given flags and return the
    path to the written CLAUDE.md

    :param tmp_path_factory: pytest ``tmp_path_factory`` fixture
    :param cli_claude_command: ``python -m kaye claude `` command prefix
    :type cli_claude_command: str
    :param flags: extra flags inserted before PROMPT_FILE, e.g. ``"-r -c"``
    :type flags: str
    :return: path to the written CLAUDE.md
    :rtype: Path-like
    """
    tmp_folder = tmp_path_factory.mktemp("claude_user_prompt")
    claude_md_path = tmp_folder / "CLAUDE.md"

    cmd = cli_claude_command + "user-system-prompt "
    if flags:
        cmd += flags + " "
    cmd += str(claude_md_path)
    subprocess.run(cmd, shell=True, check=True)

    return claude_md_path


@pytest.fixture(scope="session")
def chat_path(tmp_path_factory, cli_claude_command):
    return export_claude_md(tmp_path_factory, cli_claude_command)


@pytest.fixture(scope="session")
def chat_content(chat_path):
    with open(chat_path) as f:
        return f.read()


@pytest.fixture(scope="session")
def rapid_path(tmp_path_factory, cli_claude_command):
    return export_claude_md(tmp_path_factory, cli_claude_command, "-r")


@pytest.fixture(scope="session")
def rapid_content(rapid_path):
    with open(rapid_path) as f:
        return f.read()


@pytest.fixture(scope="session")
def coder_path(tmp_path_factory, cli_claude_command):
    return export_claude_md(tmp_path_factory, cli_claude_command, "-c")


@pytest.fixture(scope="session")
def coder_content(coder_path):
    with open(coder_path) as f:
        return f.read()


@pytest.fixture(scope="session")
def rapid_coder_path(tmp_path_factory, cli_claude_command):
    return export_claude_md(tmp_path_factory, cli_claude_command, "-r -c")


@pytest.fixture(scope="session")
def rapid_coder_content(rapid_coder_path):
    with open(rapid_coder_path) as f:
        return f.read()
