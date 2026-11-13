"""
examples/cli_info/affordance_demo.py

print ``kaye-engine affordance``, plain and with ``-l``

run from anywhere:

    python examples/cli_info/affordance_demo.py
"""

import sys
from pathlib import Path

# project root on the path, so the demo runs directly or with -m
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# pylint: disable=wrong-import-position
from examples.cli_info import run_demo

# command rows: (argv, whether the command carries -l)
CMD_ROWS = (
    (["affordance"], True),
    (["affordance", "-N"], False),
    (["affordance", "-f", "json", "-r", "^agent$"], False),
)


# Main Entry Point  ############################################################
if __name__ == "__main__":
    run_demo(
        "affordance_demo",
        "kaye-engine affordance",
        CMD_ROWS,
    )
