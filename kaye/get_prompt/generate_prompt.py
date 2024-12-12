
# TODO script to generate static prompts for saving purpose

# relative path to prompt full file
PROMPT_FULL_FILE_PATH = '../prompt_full.md'


from os.path import join, abspath, dirname

from prompt_tree_node import PromptTreeNode


__all__ = ('get_prompt')



def _load_prompt_tree():
    with open(
            abspath(join(dirname(__file__), PROMPT_FULL_FILE_PATH)),
            'r') as file:
        file_content = file.read()
        return PromptTreeNode(file_content)



def get_prompt(prompt_name):
    # TODO docstring
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


    elif prompt_name == 'commit message writer':
        tree['personality'].set()
        tree['conversation'].set()
        tree['role']['commit message writer'].set()


    else:
        raise KeyError()  # TODO



    # perform .md render
    return str(tree)
