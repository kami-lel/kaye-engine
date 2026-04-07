# pylint: disable=missing-module-docstring


# Output Keys  #################################################################

OUTPUT_ANSWER_KEY = "flattened_answers"


# Entry Point  #################################################################
def main(iteration_output: list[list]):
    """
    :param iteration_output:
    :type iteration_output: list[list]
    """

    for i, (llm, usage, answer) in enumerate(iteration_output, 1):
        pass  # TODO

    answers = "\n----\n".join(
        "# Answer {}\n{}".format(i, answer)
        for i, answer in enumerate(task_answers)
    )

    # Output Variables  --------------------------------------------------------
    return {OUTPUT_ANSWER_KEY: str(answers)}
