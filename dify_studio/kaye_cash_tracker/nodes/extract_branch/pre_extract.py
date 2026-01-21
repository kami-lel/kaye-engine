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

# constants  ###################################################################
OUTPUT_USER_MSG_KEY = "user_msg"


# entry point  #################################################################
def main(
    transactions: dict,
    query: str,
):  # pylint: disable=missing-function-docstring

    user_msg = """{}

## Existing Transactions

```json
{}
```""".format(query, transactions)

    return {OUTPUT_USER_MSG_KEY: user_msg}
