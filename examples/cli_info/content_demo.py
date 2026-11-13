"""
examples/cli_info/content_demo.py

print the commands that list a registry or print one entry's content:
``glossary``, ``exportable``, ``dynamic-substitution``, ``dynamic-node``

run from anywhere:

    python examples/cli_info/content_demo.py
"""

import sys
from pathlib import Path

# project root on the path, so the demo runs directly or with -m
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# pylint: disable=wrong-import-position
from examples.cli_info import (
    DEMO_BLUEPRINT,
    DEMO_GLOSSARY,
    DEMO_SUBSTITUTION,
    run_demo,
)

# command rows: (argv, whether the command carries -l)
CMD_ROWS = (
    (["glossary"], False),
    (["glossary", DEMO_GLOSSARY], False),
    (["exportable"], False),
    (["exportable", DEMO_BLUEPRINT], False),
    (["dynamic-substitution"], False),
    (["dynamic-substitution", DEMO_SUBSTITUTION], False),
    (["dynamic-node"], False),
    (["dynamic-node", DEMO_GLOSSARY], False),
    (["glossary", "-r", "demo"], False),
    (["glossary", "-f", "json"], False),
    (["glossary", "no-such-glossary"], False),
    (["exportable", "-N"], False),
    (["exportable", "-s", "0"], False),
    (["dynamic-node", "-r", "^today"], False),
    (["dynamic-node", "no-such-node"], False),
)


# Main Entry Point  ############################################################
if __name__ == "__main__":
    run_demo("content_demo", "glossary, exportable, dynamic-*", CMD_ROWS)
