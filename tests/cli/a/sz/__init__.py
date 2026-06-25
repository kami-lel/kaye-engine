import re
import subprocess


def convert_folder_path2skill_file_path(folder_path):
    return folder_path / "SKILL.md"


def prepare_root_folder(tmp_path_factory, command, folder_name):
    skills_folder = tmp_path_factory.mktemp(folder_name)

    # execute continue export command with folder path
    cmd = command + str(skills_folder)
    subprocess.run(cmd, shell=True, check=True)

    return skills_folder


VERSION_LINE_PATTERN = re.compile(r"^  version: [a-z0-9.\-]+$")
