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

OUTPUT_PROMPT_KEY = "concrete_prompt"


def main(
    prompt_template: str,
    user_accounts: str,
    common_other_parties: str,
):  # pylint: disable=missing-function-docstring
    concrete_prompt = prompt_template.format(
        USER_ACCOUNTS=user_accounts, COMMON_OTHER_PARTIES=common_other_parties
    )
    return {OUTPUT_PROMPT_KEY: concrete_prompt}
