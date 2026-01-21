"""
dify_cash_tracker_post_extract_test.py

Unit Tests (using pytest) for: post_extract.py
"""

from dify_studio.kaye_cash_tracker.nodes.extract_branch.post_extract import (
    main,
)

EMPTY_TRANSACTIONS = {"transactions": []}
EXAMPLE_TRANSACTIONS = {
    "transactions": [
        ["1", "???", "$", "36.71", "", "???", "Target", "G", ""],
        ["3", "05-10", "¥", "", "3000.00", "Amazon", "BOC", "A", "Jan salary"],
        [
            "2",
            "04-12",
            "HK$",
            "240.35",
            "",
            "ABC",
            "Amazon",
            "E",
            "buy Rode NT5",
        ],
    ]
}


# empty obj  ###################################################################
class TestEmptyCurrent:  # =====================================================

    def test1(_):
        current_transactions = EMPTY_TRANSACTIONS
        extract_transactions = {
            "transactions": [[
                "1",
                "01-01",
                "$",
                "12.50",
                "",
                "CASH",
                "Target",
                "G",
                "weekly grocery",
            ]]
        }

        opt = main(
            current_transactions=current_transactions,
            extract_obj=extract_transactions,
        )

        print(opt)

        transactions_obj = opt["transactions"]
        assert "transactions_table" in opt

        assert transactions_obj == extract_transactions

    def test2(_):
        current_transactions = EMPTY_TRANSACTIONS
        extract_transactions = {
            "transactions": [
                [
                    "2",
                    "01-05",
                    "$",
                    "",
                    "1.50",
                    "Alice",
                    "CASH",
                    "Y",
                    "",
                ],
                [
                    "1",
                    "01-01",
                    "$",
                    "12.50",
                    "",
                    "CASH",
                    "Target",
                    "G",
                    "weekly grocery",
                ],
            ]
        }

        opt = main(
            current_transactions=current_transactions,
            extract_obj=extract_transactions,
        )

        print(opt)

        transactions_obj = opt["transactions"]
        assert "transactions_table" in opt

        assert transactions_obj == extract_transactions


class TestEmptyUpdated:  # =====================================================

    def test1(_):
        current_transactions = EXAMPLE_TRANSACTIONS
        extract_transactions = EMPTY_TRANSACTIONS

        opt = main(
            current_transactions=current_transactions,
            extract_obj=extract_transactions,
        )

        print(opt)

        transactions_obj = opt["transactions"]
        assert "transactions_table" in opt

        assert transactions_obj == current_transactions


# merge  #######################################################################
class TestMergeNoUpdate:  # ====================================================

    def test1(_):
        current_transactions = EXAMPLE_TRANSACTIONS
        extract_transactions = {
            "transactions": [
                [
                    "4",
                    "10-05",
                    "$",
                    "",
                    "1.50",
                    "Alice",
                    "CASH",
                    "Y",
                    "",
                ],
                [
                    "5",
                    "10-01",
                    "$",
                    "12.50",
                    "",
                    "CASH",
                    "Target",
                    "G",
                    "weekly grocery",
                ],
            ]
        }

        opt = main(
            current_transactions=current_transactions,
            extract_obj=extract_transactions,
        )

        print(opt)

        transactions_obj = opt["transactions"]
        assert "transactions_table" in opt

        assert transactions_obj == {
            "transactions": [
                ["1", "???", "$", "36.71", "", "???", "Target", "G", ""],
                [
                    "4",
                    "10-05",
                    "$",
                    "",
                    "1.50",
                    "Alice",
                    "CASH",
                    "Y",
                    "",
                ],
                [
                    "5",
                    "10-01",
                    "$",
                    "12.50",
                    "",
                    "CASH",
                    "Target",
                    "G",
                    "weekly grocery",
                ],
                [
                    "3",
                    "05-10",
                    "¥",
                    "",
                    "3000.00",
                    "Amazon",
                    "BOC",
                    "A",
                    "Jan salary",
                ],
                [
                    "2",
                    "04-12",
                    "HK$",
                    "240.35",
                    "",
                    "ABC",
                    "Amazon",
                    "E",
                    "buy Rode NT5",
                ],
            ],
        }


class TestMergeWithUpdate:  # ==================================================

    def test1(_):
        current_transactions = EXAMPLE_TRANSACTIONS
        extract_transactions = {
            "transactions": [
                ["1", "01-01", "$", "36.71", "", "CASH", "Target", "G", ""],
            ]
        }

        opt = main(
            current_transactions=current_transactions,
            extract_obj=extract_transactions,
        )

        print(opt)

        transactions_obj = opt["transactions"]
        assert "transactions_table" in opt

        assert transactions_obj == {
            "transactions": [
                [
                    "3",
                    "05-10",
                    "¥",
                    "",
                    "3000.00",
                    "Amazon",
                    "BOC",
                    "A",
                    "Jan salary",
                ],
                [
                    "2",
                    "04-12",
                    "HK$",
                    "240.35",
                    "",
                    "ABC",
                    "Amazon",
                    "E",
                    "buy Rode NT5",
                ],
                ["1", "01-01", "$", "36.71", "", "CASH", "Target", "G", ""],
            ]
        }

    def test2(_):
        current_transactions = EXAMPLE_TRANSACTIONS
        extract_transactions = {
            "transactions": [
                ["1", "01-01", "$", "36.71", "", "CASH", "Target", "G", ""],
                [
                    "2",
                    "01-02",
                    "HK$",
                    "240.35",
                    "",
                    "ABC",
                    "Amazon",
                    "E",
                    "purchase Rode NT5",
                ],
            ]
        }

        opt = main(
            current_transactions=current_transactions,
            extract_obj=extract_transactions,
        )

        print(opt)

        transactions_obj = opt["transactions"]
        assert "transactions_table" in opt

        assert transactions_obj == {
            "transactions": [
                [
                    "3",
                    "05-10",
                    "¥",
                    "",
                    "3000.00",
                    "Amazon",
                    "BOC",
                    "A",
                    "Jan salary",
                ],
                [
                    "2",
                    "01-02",
                    "HK$",
                    "240.35",
                    "",
                    "ABC",
                    "Amazon",
                    "E",
                    "purchase Rode NT5",
                ],
                ["1", "01-01", "$", "36.71", "", "CASH", "Target", "G", ""],
            ]
        }

    def test3(_):
        current_transactions = EXAMPLE_TRANSACTIONS
        extract_transactions = {
            "transactions": [
                ["1", "01-01", "$", "36.71", "", "CASH", "Target", "G", ""],
                [
                    "2",
                    "01-02",
                    "HK$",
                    "240.35",
                    "",
                    "ABC",
                    "Amazon",
                    "E",
                    "purchase Rode NT5",
                ],
                [
                    "5",
                    "10-01",
                    "$",
                    "12.50",
                    "",
                    "CASH",
                    "Target",
                    "G",
                    "weekly grocery",
                ],
            ]
        }

        opt = main(
            current_transactions=current_transactions,
            extract_obj=extract_transactions,
        )

        print(opt)

        transactions_obj = opt["transactions"]
        assert "transactions_table" in opt

        assert transactions_obj == {
            "transactions": [
                [
                    "5",
                    "10-01",
                    "$",
                    "12.50",
                    "",
                    "CASH",
                    "Target",
                    "G",
                    "weekly grocery",
                ],
                [
                    "3",
                    "05-10",
                    "¥",
                    "",
                    "3000.00",
                    "Amazon",
                    "BOC",
                    "A",
                    "Jan salary",
                ],
                [
                    "2",
                    "01-02",
                    "HK$",
                    "240.35",
                    "",
                    "ABC",
                    "Amazon",
                    "E",
                    "purchase Rode NT5",
                ],
                ["1", "01-01", "$", "36.71", "", "CASH", "Target", "G", ""],
            ]
        }


# table  #######################################################################


class TestTable:

    def test1(_):
        current_transactions = EXAMPLE_TRANSACTIONS
        extract_transactions = {
            "transactions": [
                [
                    "4",
                    "10-05",
                    "$",
                    "",
                    "1.50",
                    "Alice",
                    "CASH",
                    "Y",
                    "",
                ],
                [
                    "5",
                    "10-01",
                    "$",
                    "12.50",
                    "",
                    "CASH",
                    "Target",
                    "G",
                    "weekly grocery",
                ],
            ]
        }

        obj = main(
            current_transactions=current_transactions,
            extract_obj=extract_transactions,
        )

        opt = obj["transactions_table"]

        print(opt)

        assert opt == """|  | ¤ | Out | In | From | To |  | Remarks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ??? | $ | 36.71 |  | ??? | Target | G |  |
| 10-05 | $ |  | 1.50 | Alice | CASH | Y |  |
| 10-01 | $ | 12.50 |  | CASH | Target | G | weekly grocery |
| 05-10 | ¥ |  | 3000.00 | Amazon | BOC | A | Jan salary |
| 04-12 | HK$ | 240.35 |  | ABC | Amazon | E | buy Rode NT5 |"""
