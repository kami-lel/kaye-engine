"""
fill the prompt with ``user_accounts`` and ``common_other_parties``


:param prompt_template: prompt template, returned by HTTP request node
:type prompt_template: str
:param user_accounts:
:type user_accounts: str
:param common_other_parties:
:type common_other_parties: str
:return: {
    "concrete_prompt": content of the system prompt used by Extract Node
}
:rtype: dict{
    "concrete_prompt": str
}
"""

from datetime import datetime

OUTPUT_PROMPT_KEY = "concrete_prompt"


def main(
    prompt_template: str,
    user_accounts: str,
    common_other_parties: str,
):  # pylint: disable=missing-function-docstring
    today = datetime.today().strftime("%Y-%m-%d")
    concrete_prompt = prompt_template.format(
        TODAY=today,  # HACK dont use TODAY
        USER_ACCOUNTS=user_accounts,
        COMMON_OTHER_PARTIES=common_other_parties,
    )
    # BUG the prompt coantains {} which will have issue
    return {OUTPUT_PROMPT_KEY: concrete_prompt}
