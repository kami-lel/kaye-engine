"""
prompt-bp-registry_test.py

Unit Tests (using pytest) for:

- register_blueprint()
- BlueprintRegistry
"""

import pytest

from kaye_engine.prompt.blueprint import PromptBlueprint
from kaye_engine.prompt.blueprint.registry import (
    BlueprintRegistry,
    register_blueprint,
    blueprint_registry,
)


@pytest.fixture
def registered_names():
    names = []
    yield names
    for name in names:
        blueprint_registry.pop(name, None)


class TestRegisterBlueprint:  ###################################################

    def test_dft(_, corpus_testee1, registered_names):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )

        reg = register_blueprint("test-registry-dft", "Test Registry Dft", bp)
        registered_names.append(reg.name)

        assert isinstance(reg, BlueprintRegistry)
        assert reg.name == "test-registry-dft"
        assert reg.display_name == "Test Registry Dft"
        assert reg.blueprint is bp
        assert reg.skill_exportable is False
        assert reg.continue_exportable is False
        assert reg.always_apply is False
        assert reg.user_invokable is True
        assert reg.llm_invokable is True
        assert blueprint_registry["test-registry-dft"] is reg

    def test_flags(_, corpus_testee1, registered_names):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )

        reg = register_blueprint(
            "test-registry-flags",
            "Test Registry Flags",
            bp,
            skill_exportable=True,
            continue_exportable=True,
            always_apply=True,
            user_invokable=False,
            llm_invokable=False,
        )
        registered_names.append(reg.name)

        assert reg.skill_exportable is True
        assert reg.continue_exportable is True
        assert reg.always_apply is True
        assert reg.user_invokable is False
        assert reg.llm_invokable is False

    def test_duplicate_name(_, corpus_testee1, registered_names):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )

        reg = register_blueprint("test-registry-dup", "Test Registry Dup", bp)
        registered_names.append(reg.name)

        with pytest.raises(ValueError) as exec_info:
            register_blueprint("test-registry-dup", "Another Name", bp)

        opt = exec_info.value.args[0]
        print(opt)
        assert opt == "duplicate blueprint registry name: test-registry-dup"


class TestSkillName:  ###########################################################

    def test_slugify(_, corpus_testee1, registered_names):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )

        reg = register_blueprint(
            "test-registry-skill-name", "Abbr Starts with Digits 0~9", bp
        )
        registered_names.append(reg.name)

        assert reg.skill_name == "abbr-starts-with-digits-0-9"
