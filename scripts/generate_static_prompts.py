"""
generate and save all avialble *predefined prompts*, and save for book-keeping purpose
"""


AVAILABLE_PROMPTS = [
        'secretary',
        'code',
        'python',
        'librarian',
        'commit',
        'diff']


from pathlib import Path

from kaye.get_prompt import get_prompt



if __name__ == '__main__':
    static_prompt_folder = Path(__file__).parent.parent / "static_prompts"

    for prompt in AVAILABLE_PROMPTS:

        file_path = (static_prompt_folder / (prompt + '.md')).absolute()
        with open(file_path, 'w+', encoding='utf-8', newline='') as f:
            prompt_content = get_prompt(prompt)
            f.write(prompt_content)

