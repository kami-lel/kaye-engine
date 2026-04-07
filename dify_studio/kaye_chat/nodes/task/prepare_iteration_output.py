# pylint: disable=missing-module-docstring


# Output Keys  #################################################################

OUTPUT_OUTPUT_KEY = "iteration_output"


# Entry Point  #################################################################
def main(llm: str, usage: dict, answer: str):
    """
    :param llm:
    :type llm: str
    :param usage:
    :type usage: dict
    :param answer:
    :type answer: str
    """

    output = [llm, usage, answer]

    # Output Variables  --------------------------------------------------------
    return {OUTPUT_OUTPUT_KEY: output}
