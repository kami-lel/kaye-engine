# TODO


def main(google_sheet_name: str):  # pylint: disable=missing-function-docstring
    result = '["{}!A:A"]'.format(google_sheet_name)
    return {"result": result}
