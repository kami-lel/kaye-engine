"""
define the CLI for ``kaye``
"""

# fixme better __doc__


import argparse

# fixme better
kaye_psr = argparse.ArgumentParser(prog="Kaye", description=__doc__)


if __name__ == "__main__":
    args = kaye_psr.parse_args()
