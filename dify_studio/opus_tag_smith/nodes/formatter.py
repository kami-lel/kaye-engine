# pylint: disable=missing-module-docstring


# Output Keys  #################################################################
OUTPUT_RESPONSE_KEY = "response"


# Entry Point  #################################################################
def main(extract: dict, target: str):
    """
    :param extract:
    :type extract: dict
    :param target: target/mode of operation, "Opus" or "Athenaeum"
    :type target: str
    :return: {
        "response": response formatted in md
    }
    :rtype: dict{"response": str}
    """
    # TODO
    response = ""
    return {OUTPUT_RESPONSE_KEY: response}
