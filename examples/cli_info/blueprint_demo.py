"""
examples/cli_info/blueprint_demo.py

print the ``kaye-engine blueprint`` commands: list, show, preview,
validate, render

run from anywhere:

    python examples/cli_info/blueprint_demo.py
"""

import sys
from pathlib import Path

# project root on the path, so the demo runs directly or with -m
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# pylint: disable=wrong-import-position
from examples.cli_info import DEMO_BLUEPRINT, run_demo

# command rows: (argv, whether the command carries -l)
CMD_ROWS = (
    (["blueprint", "list"], False),
    (["blueprint", "show", DEMO_BLUEPRINT], False),
    (["blueprint", "preview", DEMO_BLUEPRINT], False),
    (["blueprint", "validate", DEMO_BLUEPRINT], False),
    (["blueprint", "render", DEMO_BLUEPRINT], False),
)


# Main Entry Point  ############################################################
if __name__ == "__main__":
    run_demo("blueprint_demo", "kaye-engine blueprint", CMD_ROWS)
