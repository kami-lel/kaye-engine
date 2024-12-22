"""
generate and save all avialble *predefined prompts*, and save for book-keeping purpose
"""


from pathlib import Path

from kaye.get_prompt import get_prompt, PROMPTS



if __name__ == '__main__':
    static_prompt_folder = Path(__file__).parent.parent / "static_prompts"

    for prompt in PROMPTS.keys():
        if prompt == 'full':
            continue

        file_path = (static_prompt_folder / (prompt + '.md')).absolute()
        with open(file_path, 'w+', encoding='utf-8', newline='') as f:
            prompt_content = get_prompt(prompt)
            f.write(prompt_content)

