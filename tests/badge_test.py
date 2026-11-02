"""
badge_test.py

Unit Tests (using pytest) for:

native badge name constants
"""

import pytest

from kaye_engine import badge

# native badge names, per the kamilog badge documentation
_NATIVE_BADGES = frozenset(
    {
        "dry", "chk", "mock", "sandbox",
        "force", "undo", "grant", "elevated", "legacy", "unstable",
        "new", "owr", "del", "mv", "cp", "cached", "stale",
        "auto", "fresh", "resume", "offline",
        "watch", "bg",
        "retry", "fallback", "timeout", "abort",
    }
)


# pytest  ######################################################################
class TestBadgeNames:

    @pytest.mark.parametrize("name", badge.__all__)
    def test_constant_is_a_native_badge(_, name):
        assert getattr(badge, name) in _NATIVE_BADGES

    def test_constants_are_distinct(_):
        values = [getattr(badge, name) for name in badge.__all__]
        assert len(values) == len(set(values))
