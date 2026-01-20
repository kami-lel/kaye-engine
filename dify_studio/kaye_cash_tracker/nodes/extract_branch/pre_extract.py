"""
fill the prompt template with runtime info to produce the concrete prompt

TODO add params
"""

from datetime import datetime

# constants  ###################################################################
OUTPUT_USER_MSG_KEY = "user_msg"


# entry point  #################################################################


def main(
    transactions: dict,
    user_accounts: str,
    common_other_parties: str,
    query: str,
):  # pylint: disable=missing-function-docstring
    """
    create *User Message* part for Extract Node


    :param transactions:
    :type transactions: dict
    :param user_accounts:
    :type user_accounts: str
    :param common_other_parties:
    :type common_other_parties: str
    :param query:
    :type query: str
    :return: {
        "user_msg": content used for User Account
    }
    :rtype: dict{
        "user_msg": str
    }
    """

    # prompt = prompt_template_cache.format(
    #     TODAY=datetime.today().strftime("%Y-%m-%d"),
    #     TRANSACTIONS=transactions_array,
    #     USER_ACCOUNTS=user_accounts,
    #     COMMON_OTHER_PARTIES=common_other_parties,
    # )

    user_msg = ""
    # TODO contains: transactions, today, & parties

    return {OUTPUT_USER_MSG_KEY: user_msg}
