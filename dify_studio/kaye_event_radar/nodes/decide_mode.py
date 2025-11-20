def main(user_query: str, grab_trigger_keyword: str):
    """
    decide operating mode for this round of conversation

    :param user_query:
    :type user_query: str
    :param grab_trigger_keyword:
    :type grab_trigger_keyword: str
    :return: value of ``"output"`` is an ``int``:

    - ``0``: scan events provided by user
    - ``1``: scan events by grabbing webs

    :rtype: dict
    """
    opt = int(grab_trigger_keyword in user_query)
    return {"output": opt}
