"""
generate prompt Environment Variables (prefixed with ``prompt_``) content
for dify app
"""

from pathlib import Path

from kaye.gen_prompt import load_embedded_prompt_blueprint

# todo printing of tree only when debugging

PRIMARY_MESSAGE_FILENAME = "prompt_primary_message.md"
PER_FILE_LONG_FILENAME = "prompt_per_file_summary_long.md"
PER_FILE_SHORT_FILENAME = "prompt_per_file_summary_short.md"
PRIMARY_MESSAGE_NODES = []

if __name__ == "__main__":
    folder = Path(__file__).parent

    with open(
        (folder / PRIMARY_MESSAGE_FILENAME).resolve(),
        "w",
        encoding="utf-8",
    ) as file:
        blueprint = load_embedded_prompt_blueprint("empty")
        blueprint.set_unset_detached_mode(False)
        blueprint.enabled_nodes_names.extend(PRIMARY_MESSAGE_NODES)
        # print for debug
        print("prompt_primary_message.md  ".zfill())
        file.write()  # TODO

    with open(
        (folder / PER_FILE_LONG_FILENAME).resolve(),
        "w",
        encoding="utf-8",
    ) as file:
        file.write()  # TODO

    with open(
        (folder / PER_FILE_SHORT_FILENAME).resolve(),
        "w",
        encoding="utf-8",
    ) as file:
        file.write()  # TODO
