# pylint: disable=missing-module-docstring


# Output Keys  #################################################################

OUTPUT_ANSWER_KEY = "flattened_answers"
OUTPUT_TASK_KEY = "task_usages"


# Entry Point  #################################################################
def main(iteration_output: list[list]):
    """
    :param iteration_output:
    :type iteration_output: list[list]
    :return: {
        "flattened_answers":    all LLMs' answer flattened as single md document
        "task_usages":          task usages of all LLMs
    }
    :rtype: dict{
        "flattened_answers":    str
        "task_usages":          dict
    }
    """

    answer_parts = []
    task_usages = {}

    for i, (llm, usage, answer) in enumerate(iteration_output, 1):
        answer_parts.append("# Answer {}\n{}".format(i, answer))
        task_usages[llm] = usage

    answers = "\n----\n".join(answer_parts)

    # Output Variables  --------------------------------------------------------
    return {OUTPUT_ANSWER_KEY: str(answers), OUTPUT_TASK_KEY: task_usages}
