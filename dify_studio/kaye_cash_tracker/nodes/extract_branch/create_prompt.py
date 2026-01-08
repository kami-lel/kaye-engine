"""
access Kaye Flask API to get prompt template,
cache the template locally

then fill the template with runtime info to produce the concrete prompt
"""

import requests

# constants  ###################################################################
OUTPUT_PROMPT_KEY = "concrete_prompt"
OUTPUT_TEMPLATE_KEY = "updated_prompt_template_cache"
KAYE_API_URL = "http://localhost:11255/kaye/dify-app/kaye-cash-tracker/"
REQUEST_TIMEOUT = 10


# entry point  #################################################################
def main(
    prompt_template_cache: str,
    today: str,
    transactions_array: dict,
    user_accounts,
    common_other_parties,
):  # pylint: disable=missing-function-docstring

    if not prompt_template_cache:  # when not locally cached
        # get prompt template by API  ------------------------------------------
        try:
            response = requests.get(KAYE_API_URL, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            prompt_template_cache = response.text

        except requests.RequestException as err:
            raise ValueError(
                "fail to GET prompt: {}".format(err.args[0])
            ) from err

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
