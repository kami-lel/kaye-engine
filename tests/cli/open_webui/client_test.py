"""
client_test.py

Unit Tests (using pytest) for:

OpenWebUIClient, OpenWebUIError
"""

import io
import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from kaye_engine.cli.open_webui.client import (
    OpenWebUIClient,
    OpenWebUIError,
)

_URLOPEN = "kaye_engine.cli.open_webui.client.urllib.request.urlopen"


# auxiliaries  #################################################################
def _build_response(payload):
    response = MagicMock()
    response.read.return_value = json.dumps(payload).encode()
    response.__enter__.return_value = response
    return response


def _build_http_error(code, body="boom"):
    return urllib.error.HTTPError(
        "http://x", code, "msg", {}, io.BytesIO(body.encode())
    )


def _sent_request(urlopen):
    return urlopen.call_args.args[0]


@pytest.fixture
def _client():
    return OpenWebUIClient("http://host:1234/", "sk-key")


# pytest  ######################################################################
class TestRequests:

    def test_export_skills_get_with_bearer(_, _client):
        with patch(_URLOPEN, return_value=_build_response([])) as urlopen:
            result = _client.export_skills()

        request = _sent_request(urlopen)
        assert result == []
        assert request.full_url == "http://host:1234/api/v1/skills/export"
        assert request.get_method() == "GET"
        assert request.get_header("Authorization") == "Bearer sk-key"
        assert request.data is None

    def test_create_skill_posts_json_body(_, _client):
        form = {"id": "a-b", "name": "A B"}
        with patch(_URLOPEN, return_value=_build_response(form)) as urlopen:
            _client.create_skill(form)

        request = _sent_request(urlopen)
        assert request.full_url == "http://host:1234/api/v1/skills/create"
        assert request.get_method() == "POST"
        assert json.loads(request.data) == form
        assert request.get_header("Content-type") == "application/json"

    def test_update_skill_posts_to_id_path(_, _client):
        form = {"id": "a-b", "name": "A B"}
        with patch(_URLOPEN, return_value=_build_response(form)) as urlopen:
            _client.update_skill(form)

        request = _sent_request(urlopen)
        assert request.full_url == (
            "http://host:1234/api/v1/skills/id/a-b/update"
        )
        assert request.get_method() == "POST"
        assert json.loads(request.data) == form

    def test_delete_skill_uses_delete_method(_, _client):
        with patch(_URLOPEN, return_value=_build_response(True)) as urlopen:
            result = _client.delete_skill("a-b")

        request = _sent_request(urlopen)
        assert result is True
        assert request.full_url == (
            "http://host:1234/api/v1/skills/id/a-b/delete"
        )
        assert request.get_method() == "DELETE"


class TestErrorMapping:

    @pytest.mark.parametrize("code", [400, 401, 404])
    def test_http_error_carries_status_and_body(_, _client, code):
        with patch(_URLOPEN, side_effect=_build_http_error(code, "nope")):
            with pytest.raises(OpenWebUIError) as info:
                _client.export_skills()

        assert info.value.status == code
        assert info.value.body == "nope"

    def test_network_failure_has_no_status(_, _client):
        with patch(
            _URLOPEN, side_effect=urllib.error.URLError("refused")
        ):
            with pytest.raises(OpenWebUIError) as info:
                _client.export_skills()

        assert info.value.status is None
        assert info.value.body == "refused"
