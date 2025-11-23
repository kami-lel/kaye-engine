def main(events: list[dict]):
    """
    simple conversion of ``events`` array to flattened text


    :return: ``opt`` is text (typed ``str``)
    """
    opt = "\n\n".join("{}".format(event) for event in events)
    return {"output": opt}
