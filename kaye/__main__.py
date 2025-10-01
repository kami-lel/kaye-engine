"""
CLI for Python module ``kaye``
"""

# HACK rm
# from argparse import ArgumentParser, FileType
# import pathlib
# import os
# import importlib

# import yaml


# from kaye.gen_prompt.prompt_blueprint_loader import (
#     PromptBlueprint,
#     get_embedded_prompt_blueprints_names,
#     load_embedded_prompt_blueprint,
#     load_embedded_prompt_corpus,
# )

PROGRAM_NAME = "kaye"


# todo make import/export json file for OpenWebUI

if __name__ == "__main__":
    parsed_args = kaye_psr.parse_args()  # BUG
    parsed_args.func(parsed_args)  # call respective main function
