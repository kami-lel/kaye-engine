def main(google_sheet_name: str):
    result = '["{}!A:A"]'.format(google_sheet_name)
    return {"result": result}
