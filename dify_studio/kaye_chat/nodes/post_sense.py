# pylint: disable=missing-module-docstring


# output keys  #################################################################
OUTPUT_COMBINED_KEY = "combined_pls"


# constant  ####################################################################
SPLITTER = ","


# Entry Point  #################################################################
def main(current_pls: str, sensed_pls: dict):
    combined_set = set(current_pls.split(SPLITTER)) | set(
        sensed_pls.split(SPLITTER)
    )
    combined_pls = SPLITTER.join(combined_set)

    return {OUTPUT_COMBINED_KEY: combined_pls}
