"""
access Kaye Flask API to get prompt template,
cache the template locally

then fill the template with runtime info to produce the concrete prompt
"""

OUTPUT_PROMPT_KEY = "concrete_prompt"
OUTPUT_TEMPLATE_KEY = "updated_prompt_template_cache"


def main(
    prompt_template_cache: str,
    today: str,
    transactions_array: dict,
    user_accounts,
    common_other_parties,
):
    # get prompt template by API  ----------------------------------------------
    if not prompt_template_cache:  # when not locally cached
        pass  # TODO

    # fill template w/ runtime info  -------------------------------------------
    prompt = prompt_template_cache.format(
        TODAY=today,
        TRANSACTIONS=transactions_array,
        USER_ACCOUNTS=user_accounts,
        COMMON_OTHER_PARTIES=common_other_parties,
    )

    return {
        OUTPUT_PROMPT_KEY: prompt,
        OUTPUT_TEMPLATE_KEY: prompt_template_cache,
    }
