# pylint: disable=missing-module-docstring


# Output Keys  #################################################################

OUTPUT_ANSWER_KEY = "flattened_answers"


# Entry Point  #################################################################
def main(task_answers: list[str]):
    """
    :param task_answers:
    :type task_answers: list[str]
    :return: {"flattened_answers": answers of different LLMs flattened}
    :rtype: dict{"flattened_answers": str}
    """

    answers = "\n----\n".join(
        "# Answer {}\n{}".format(i, answer)
        for i, answer in enumerate(task_answers)
    )

    # Output Variables  --------------------------------------------------------
    return {OUTPUT_ANSWER_KEY: str(answers)}
