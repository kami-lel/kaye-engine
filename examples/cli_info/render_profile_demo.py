"""
examples/cli_info/render_profile_demo.py

print ``kaye-engine render-profile``, plain and with ``-l``

run from anywhere:

    python examples/cli_info/render_profile_demo.py
"""

import sys
from pathlib import Path

# project root on the path, so the demo runs directly or with -m
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# pylint: disable=wrong-import-position
from examples.cli_info import run_demo

# command rows: (argv, whether the command carries -l)
CMD_ROWS = (
    (["render-profile"], True),
)


# Main Entry Point  ############################################################
if __name__ == "__main__":
    run_demo(
        "render_profile_demo",
        "kaye-engine render-profile",
        CMD_ROWS,
    )
