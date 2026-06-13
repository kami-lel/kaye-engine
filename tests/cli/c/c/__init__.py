import subprocess

from tests.cli import (
    split_frontmatter_md_file,
    assert_frontmatter_md_file_basic_structure,
    assert_header_line_always_apply,
)

# Aliases for backward compatibility
split_rule_file_basic_format = split_frontmatter_md_file
assert_rule_file_basic_format = assert_frontmatter_md_file_basic_structure


def prepare_local_config_folder(tmp_path_factory, command, folder_name):
    config_folder = tmp_path_factory.mktemp(folder_name)

    # Execute continue export command with folder path
    cmd = command + str(config_folder)
    subprocess.run(cmd, shell=True, check=True)

    rules_folder = config_folder / "rules"

    return config_folder, rules_folder


# Re-export for backward compatibility
__all__ = [
    "split_frontmatter_md_file",
    "assert_frontmatter_md_file_basic_structure",
    "split_rule_file_basic_format",
    "assert_rule_file_basic_format",
    "assert_header_line_always_apply",
    "prepare_local_config_folder",
]
