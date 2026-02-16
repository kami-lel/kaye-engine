# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_ROLE_KEY = "role"


# Entry Point  #################################################################


def main(role_override):
    return {OUTPUT_ROLE_KEY: role_override}
