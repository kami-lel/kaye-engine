"""
predefined prompts:

- full: entire prompt
- secretary: prompt focus on everyday activity, e.g. conversation, encyclopedic, translation, etc.
- code: prompt include all code-writing roles
- python: prompt specific for Python code assistant
- librarian: create a book label and determine DDC
- commit: take a result of git diff, then generate an appropriate git commit message
- diff: take a result of git diff, return a summary of changes
"""


from pathlib import Path

from .prompt_tree_node import PromptTreeNode


__all__ = ('get_prompt',)


# path to prompt_full.md
prompt_full_path = \
        (Path(__file__).resolve().parent.parent / 'prompt_full.md').absolute()


def _load_prompt_tree():
    with open(prompt_full_path, 'r', encoding='utf-8', newline='') as file:
        file_content = file.read()
        return PromptTreeNode(file_content)


def get_prompt(prompt_name):
    """
    generate one of the **predefined prompts** as whole or a subset of *prompt full*

    q.v. __doc__ of ``generate_prompt.py``

    :param prompt_name: name of the prompt, q.v. __doc__ of ``generate_prompt.py`` for supported prompt & function
    :type prompt_name: str
    :return: content of the generated prompt
    :rtype: str
    :raises ValueError: arg prompt_name not recognized
    """
    tree = _load_prompt_tree()

    if prompt_name == 'full':
        tree.set()


    elif prompt_name == 'secretary':
        tree['personality'].set()
        tree['conversation'].set()
        tree['format'].set()
        tree['abbreviation'].set()
        tree['role']['encyclopedic'].set()
        tree['role']['editor'].set()
        tree['role']['secretary'].set()
        tree['role']['translator'].set()


    elif prompt_name == 'code':
        tree['personality'].set()
        tree['conversation'].set()
        tree['format'].set()
        tree['abbreviation'].set()
        tree['role']['code assistant'].set()


    elif prompt_name == 'python':
        tree['personality'].set()
        tree['conversation'].set()
        tree['format'].set()
        tree['abbreviation'].set()
        tree['role']['code assistant']['Python'].set()


    elif prompt_name == 'librarian':
        tree['personality'].set()
        tree['conversation'].set()
        tree['role']['librarian'].set()


    elif prompt_name == 'commit':
        tree['personality'].set()
        tree['conversation'].set()
        tree['role']['git commit message writer'].set()


    elif prompt_name == 'diff':
        tree['personality'].set()
        tree['conversation'].set()
        tree['role']['git diff summary'].set()


    else:
        raise ValueError("{} of arg prompt_name not recognized".format(
                repr(prompt_name)))


    # perform .md render
    return str(tree)



