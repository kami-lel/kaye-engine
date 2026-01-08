"""
fill the prompt template with runtime info to produce the concrete prompt
"""

from datetime import datetime

# constants  ###################################################################
OUTPUT_PROMPT_KEY = "concrete_prompt"


# entry point  #################################################################


def main(
    prompt_template_cache: str,
    transactions_array: dict,
    user_accounts,
    common_other_parties,
):  # pylint: disable=missing-function-docstring

    prompt = prompt_template_cache.format(
        TODAY=datetime.today().strftime("%Y-%m-%d"),
        TRANSACTIONS=transactions_array,
        USER_ACCOUNTS=user_accounts,
        COMMON_OTHER_PARTIES=common_other_parties,
    )

    return {
        OUTPUT_PROMPT_KEY: prompt,
    }
