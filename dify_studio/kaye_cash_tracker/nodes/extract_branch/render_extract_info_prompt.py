def main(
    prompt_extract_info: str,
    today: str,
    transactions_array: dict,
    user_accounts,
    common_other_parties,
):
    opt = prompt_extract_info.format(
        TODAY=today,
        TRANSACTIONS=transactions_array,
        USER_ACCOUNTS=user_accounts,
        COMMON_OTHER_PARTIES=common_other_parties,
    )

    return {"result": opt}
