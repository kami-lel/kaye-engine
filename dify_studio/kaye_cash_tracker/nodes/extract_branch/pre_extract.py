"""
create *User Message* part for Extract Node


:param transactions:
:type transactions: str
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

import json

# constants  ###################################################################
OUTPUT_USER_MSG_KEY = "user_msg"


# entry point  #################################################################
def main(
    transactions: str,
    query: str,
):  # pylint: disable=missing-function-docstring

    current_transactions = json.loads(transactions)

    user_msg = """{}


## Existing Transactions

```json
{}
```""".format(query, current_transactions)

    return {OUTPUT_USER_MSG_KEY: user_msg}
