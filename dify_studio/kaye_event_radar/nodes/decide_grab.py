def main(user_query: str, grab_trigger_keyword: str):
    opt = grab_trigger_keyword in user_query
    return {"output": opt}
