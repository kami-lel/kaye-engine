# pylint: disable=missing-module-docstring


# Output Keys  #################################################################

OUTPUT_TASK_KEY = "task_usages"


# Entry Point  #################################################################
def main(current_llms: list[str], usage: dict):
    """
    :param current_llms:
    :type current_llms: list[str]
    :param usage:
    :type usage: dict
    :return: {"task_usages": created new ``task_usages``}
    :rtype: dict{"task_usages": dict}
    """

    task_llm = current_llms[0]
    task_usages = {task_llm: usage}

    # Output Variables  --------------------------------------------------------
    return {OUTPUT_TASK_KEY: task_usages}
