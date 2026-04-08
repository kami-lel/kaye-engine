import pytest


# Pytest fixtures  #############################################################
@pytest.fixture
def request_body():
    return {"pre_sense_role": "", "difficulty_override": 0}
