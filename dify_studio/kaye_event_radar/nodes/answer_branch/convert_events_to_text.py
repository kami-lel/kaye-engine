"""
simple conversion of ``events`` array to flattened text


:return: ``opt`` is text (typed ``str``)
"""


def main(events: list[dict]):  # pylint: disable=missing-function-docstring
    opt = "\n\n".join("{}".format(event) for event in events)
    return {"output": opt}
