"""
tests/consumer_helper.py

define ``TEST_CONSUMER`` -- the consumer every test exportable belongs
to -- and registration wrappers binding it
"""

import contextlib
import functools

from kaye_engine.abbr_collection import (
    register_abbr_glossary as _register_abbr_glossary,
)
from kaye_engine import consumer
from kaye_engine.consumer import iter_consumers, register_consumer
from kaye_engine.prompt.blueprint.registry import (
    register_blueprint as _register_blueprint,
)

__all__ = (
    "TEST_CONSUMER",
    "ensure_test_consumer",
    "isolated_consumers",
    "register_abbr_glossary",
    "register_blueprint",
)

TEST_CONSUMER = "test-consumer"


def ensure_test_consumer():
    """
    register ``TEST_CONSUMER`` unless already registered
    """
    if TEST_CONSUMER not in {c.canonical_name for c in iter_consumers()}:
        register_consumer("Test Consumer", TEST_CONSUMER, "0.0.0")


register_blueprint = functools.partial(
    _register_blueprint, consumer=TEST_CONSUMER
)
register_abbr_glossary = functools.partial(
    _register_abbr_glossary, consumer=TEST_CONSUMER
)


@contextlib.contextmanager
def isolated_consumers():
    """
    snapshot the registered consumers and the entry consumer, restoring
    both on exit, so a test may register its own
    """
    # pylint: disable=protected-access
    saved = (dict(consumer._consumers), consumer._entry_canonical_name)
    try:
        yield
    finally:
        consumer._consumers.clear()
        consumer._consumers.update(saved[0])
        consumer._entry_canonical_name = saved[1]
