"""
tests/repo_test.py

test:
- set_repo_name, set_repo_version and their getters
- rejection of a non-kebab name and an empty version
- each unset getter exiting 1
"""

import pytest

from kaye_engine.repo import (
    get_repo_name,
    get_repo_version,
    set_repo_name,
    set_repo_version,
)

from tests.consumer_helper import isolated_repo


@pytest.fixture(autouse=True)
def _isolate():
    with isolated_repo():
        # pylint: disable=import-outside-toplevel
        from kaye_engine import repo

        repo._clear_repo()  # pylint: disable=protected-access
        yield


class TestRepoName:

    def test_round_trip(_):
        set_repo_name("some-repo")

        assert get_repo_name() == "some-repo"

    def test_later_call_wins(_):
        set_repo_name("a")
        set_repo_name("b-2")

        assert get_repo_name() == "b-2"

    @pytest.mark.parametrize(
        "bad", ["Some-Repo", "some_repo", "-a", "a-", "a--b", "", " ", None, 3]
    )
    def test_non_kebab_rejected(_, bad):
        with pytest.raises(ValueError):
            set_repo_name(bad)

    def test_unset_exits_1(_):
        with pytest.raises(SystemExit) as info:
            get_repo_name()

        assert info.value.code == 1


class TestRepoVersion:

    def test_round_trip(_):
        set_repo_version("1.2.3a0")

        assert get_repo_version() == "1.2.3a0"

    def test_later_call_wins(_):
        set_repo_version("1")
        set_repo_version("2")

        assert get_repo_version() == "2"

    @pytest.mark.parametrize("bad", ["", "  ", None, 1])
    def test_empty_rejected(_, bad):
        with pytest.raises(ValueError):
            set_repo_version(bad)

    def test_unset_exits_1(_):
        with pytest.raises(SystemExit) as info:
            get_repo_version()

        assert info.value.code == 1

    def test_name_and_version_independent(_):
        set_repo_name("a")

        with pytest.raises(SystemExit):
            get_repo_version()
