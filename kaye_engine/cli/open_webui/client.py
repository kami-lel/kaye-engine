"""
client.py

define ``OpenWebUIClient``, ``OpenWebUIError``
"""

import json
import urllib.error
import urllib.parse
import urllib.request

__all__ = ("DEFAULT_BASE_URL", "OpenWebUIClient", "OpenWebUIError")

# constants  ###################################################################
DEFAULT_BASE_URL = "http://localhost:8080"

_SKILLS_PREFIX = "/api/v1/skills"
_TIMEOUT_SECONDS = 30


class OpenWebUIError(Exception):
    """
    an Open WebUI request that failed, over HTTP or the network


    :param status: HTTP status code; ``None`` for a network failure
    :type status: int, optional
    :param body: response body, or the network failure reason
    :type body: str
    """

    def __init__(self, status, body):
        super().__init__("HTTP {}: {}".format(status, body))
        self.status = status
        self.body = body


class OpenWebUIClient:
    """
    minimal client for the Open WebUI Skills REST API, over ``urllib``


    :param base_url: server root, without the ``/api/v1/skills`` prefix
    :type base_url: str
    :param api_key: Bearer token sent with every request
    :type api_key: str
    """

    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    # Public Methods  ----------------------------------------------------------

    def export_skills(self):
        """
        fetch every skill on the server


        :return: skill records
        :rtype: list[dict]
        """
        return self._request("GET", "/export")

    def create_skill(self, form):
        """
        create a skill from a full form


        :param form: ``SkillForm`` fields
        :type form: dict
        :return: the created record
        :rtype: dict
        """
        return self._request("POST", "/create", form)

    def update_skill(self, form):
        """
        overwrite the skill named by ``form["id"]`` with a full form


        :param form: ``SkillForm`` fields
        :type form: dict
        :return: the updated record
        :rtype: dict
        """
        return self._request(
            "POST", "/id/{}/update".format(self._quote(form["id"])), form
        )

    def delete_skill(self, skill_id):
        """
        delete one skill


        :param skill_id: id of the skill to delete
        :type skill_id: str
        :return: server confirmation
        :rtype: bool
        """
        return self._request(
            "DELETE", "/id/{}/delete".format(self._quote(skill_id))
        )

    # auxiliaries  -------------------------------------------------------------

    @staticmethod
    def _quote(skill_id):
        return urllib.parse.quote(skill_id, safe="")

    def _request(self, method, path, payload=None):
        data = None if payload is None else json.dumps(payload).encode()
        request = urllib.request.Request(
            self.base_url + _SKILLS_PREFIX + path,
            data=data,
            method=method,
            headers={
                "Authorization": "Bearer " + self.api_key,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(
                request, timeout=_TIMEOUT_SECONDS
            ) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            raise OpenWebUIError(
                err.code, err.read().decode("utf-8", "replace")
            ) from err
        except urllib.error.URLError as err:
            raise OpenWebUIError(None, str(err.reason)) from err
