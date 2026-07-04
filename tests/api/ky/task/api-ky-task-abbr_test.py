"""
api-ky-task-abbr_test.py

Unit Tests (using pytest) for:

/kaye/dify-api/ky/task with abbreviations
"""

import json

import pytest

from tests import TESTEE_TRIAGE_TAG_BASE_CONTENT
from tests.api.ky.task import *

# pytest fixtures  #############################################################


@pytest.fixture(scope="module")
def opt_coder(flask_test_client, task_endpoint):
    query = "afx"
    payload = {"role": "coder", "query": query}
    return create_opt_from_payload(flask_test_client, task_endpoint, payload)


# TT (Triage Tags)  #############################################################


class TestTriageTags:  # ========================================================

    @pytest.mark.parametrize("i", range(len(TESTEE_TRIAGE_TAG_BASE_CONTENT)))
    def test_tt_content(_, opt_coder, i):
        assert TESTEE_TRIAGE_TAG_BASE_CONTENT[i] in opt_coder


# Pytest unit tests  ###########################################################


class TestSingle:  # ===========================================================

    def test_chat(self, flask_test_client, task_endpoint):
        query = "afx"
        payload = {"role": "chat", "query": query}

        opt = create_opt_from_payload(flask_test_client, task_endpoint, payload)

        print(opt)

        assert_abbr_heading(opt)
        assert "- afx:affect,affected,affectedly,affectation" in opt

    def test_rapid(self, flask_test_client, task_endpoint):
        query = "afx"
        payload = {"role": "rapid", "query": query}

        opt = create_opt_from_payload(flask_test_client, task_endpoint, payload)

        print(opt)

        assert_abbr_heading(opt)
        assert "- afx:affect,affected,affectedly,affectation" in opt

    def test_coder(self, opt_coder):
        opt = opt_coder

        print(opt)

        assert_abbr_heading(opt)
        assert "- afx:affect,affected,affectedly,affectation" in opt

    def test_barista(self, flask_test_client, task_endpoint):
        query = "afx"
        payload = {"role": "barista", "query": query}

        opt = create_opt_from_payload(flask_test_client, task_endpoint, payload)

        print(opt)

        assert_abbr_heading(opt)
        assert "- afx:affect,affected,affectedly,affectation" in opt

    def test_editor(self, flask_test_client, task_endpoint):
        query = "afx"
        payload = {"role": "editor", "query": query}

        opt = create_opt_from_payload(flask_test_client, task_endpoint, payload)

        print(opt)

        assert_abbr_heading(opt)
        assert "- afx:affect,affected,affectedly,affectation" in opt

    def test_secretary(self, flask_test_client, task_endpoint):
        query = "afx"
        payload = {"role": "secretary", "query": query}

        opt = create_opt_from_payload(flask_test_client, task_endpoint, payload)

        print(opt)

        assert_abbr_heading(opt)
        assert "- afx:affect,affected,affectedly,affectation" in opt


class TestMux:  # ==============================================================

    def test1(self, flask_test_client, task_endpoint):
        query = "something achv aknlg w/ admin"
        payload = {"role": "rapid", "query": query}

        opt = create_opt_from_payload(flask_test_client, task_endpoint, payload)

        print(opt)

        assert_abbr_heading(opt)

        assert "- achv:achieve,achieved,achievement" in opt
        assert "- admin:administrate,administrator,administration" in opt
        assert "- w/:with" in opt
        assert "- aknlg:acknowledge" in opt
