"""TODO
"""



# TODO dynamically generate prompt
# todo dynamically generated prompt should remove uncessary spaces


PROG_NAME = 'kaye.gen_prompt'
# relative path to prompt full file
PROMPT_FULL_FILE_PATH = './prompt_full.md'
PROMPT_FULL_FILE_PATH = './prompt_full_no.md'  # HACK


from argparse import ArgumentParser, RawTextHelpFormatter
from collections import OrderedDict
import errno



class _PromptTreeNode(OrderedDict):

    def __new__(cls, text, level=0):
        return super().__new__(cls, {})  # new as empty dict

    def __init__(self, text, level=0):
        self.level = level
        pass

    @staticmethod
    def _level_split(text, level):
        pass


def gen_prompt(prompt_name):
    pass




psr = ArgumentParser(prog=PROG_NAME,
        description= __doc__, formatter_class=RawTextHelpFormatter)


if __name__ == "__main__":
    args = psr.parse_args()

    a = _PromptTreeNode(text='123', level=5)

