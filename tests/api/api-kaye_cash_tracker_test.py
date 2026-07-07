"""
api-dify_kaye_cash_tracker_test.py

Unit Tests (using pytest) for: /kaye/dify-app/kaye-cash-tracker/*
"""

import pytest

from tests import TESTEE_TODAY_CONTENT

# pytest fixtures  #############################################################


@pytest.fixture(scope="class")
def opt(flask_test_client, dify_app_endpoint):
    extract_endpoint = dify_app_endpoint + "/kaye-cash-tracker/extract"
    response = flask_test_client.get(extract_endpoint)
    return response.get_data().decode("utf-8")


# Pytest unit tests  ###########################################################


class TestExtract:  # ==========================================================

    def test_extract(_, opt):
        assert (
            """## Extract
You are a personal finance assistant handling **transaction** messages. Take the user’s text or image and return a list of transactions as a JSON 2D array. Each transaction entry must be either:

- new: transaction not present in the existing transactions; extract all required fields."""
            in opt
        )

    def test_id(_, opt):
        assert """#### id

required, numerical id, unique to each transaction entry""" in opt

    def test_date(_, opt):
        assert (
            """#### date

required, MM-dd format

use the *notification* date (often shown in small font in the chat or notification); ignore other dates"""
            in opt
        )

    def test_currency_symbol(_, opt):
        assert """#### currency_symbol

required

- $: USD
- ¥: RMB/Chinese Yuan
- HK$
- €""" in opt

    def test_amount_out_and_amount_in(_, opt):
        assert """#### amount_out & amount_in

- for a user expense: fill `amount_out` and leave `amount_in` empty""" in opt

    def test_party_from_and_party_to(_, opt):
        assert """#### party_from & party_to

both required

User Accounts:""" in opt

    def test_categories(_, opt):
        assert """#### categories

required

select the most likely category abbreviation for each transaction based on its details.

- A: Salary""" in opt

    def test_remarks(_, opt):
        assert """#### remarks

- leave as an empty string unless the information is essential; avoid recording irrelevant details
- use only short, specific phrases not duplicated in other fields""" in opt

    def test_example_rows(_, opt):
        assert """#### example rows

```json
[
  [
    "1",
    "???",
    "$",
    "36.71",
    "",
    "???",
    "Target",
    "G",
    ""
  ],""" in opt


class TestToday:  # ============================================================

    @pytest.mark.parametrize("i", range(len(TESTEE_TODAY_CONTENT)))
    def test_content(_, opt, i):
        assert TESTEE_TODAY_CONTENT[i] in opt
