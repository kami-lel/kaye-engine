# pylint: disable=missing-module-docstring

# TODO unit test

# Output Keys  #################################################################

OUTPUT_TASK_KEY = "task_usages"


# Entry Point  #################################################################
def main(task_usages: dict, llm: str, usage: dict):
    """
    :param task_usages:
    :type task_usages: dict
    :param llm:
    :type llm: str
    :param usage:
    :type usage: dict
    :return: {"task_usages": created new ``task_usages``}
    :rtype: dict{"task_usages": dict}
    """

    task_usages[llm] = usage

    # Output Variables  --------------------------------------------------------
    return {OUTPUT_TASK_KEY: task_usages}
