"""
export_user_file.py

define ``export_user_system_prompt_file``
"""

from pathlib import Path

from kaye.prompt.embedded_blueprints import chat_blueprint


def export_user_system_prompt_file(file_path):
    """
    export Chat blueprint as Claude user/system prompt to CLAUDE.md file

    renders the Chat blueprint and writes the prompt to the given file path

    :param file_path: destination file path for CLAUDE.md
    :type file_path: Path-like
    """
    file_path = Path(file_path).resolve()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    prompt = chat_blueprint.generate_prompt()

    file_path.write_text(prompt, encoding="utf-8")
