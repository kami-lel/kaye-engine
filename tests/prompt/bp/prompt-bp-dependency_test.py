"""
prompt-bp-dependency_test.py

Unit Tests (using pytest) for: PromptBlueprint

- ``dependencies`` field
- ``render_prompt()``
- ``render_blueprint()``
- ``_resolve_with_dependencies()`` cycle guard
- ``dependencies`` preserved across ``.prune()``, ``.merge()``, ``.__copy__()``
"""

import copy

import pytest

from kaye_engine.prompt import PromptBlueprint


class TestDefaultDependencies:  #################################################

    def test_init_default_is_empty_list(_, corpus_testee1):
        bp = PromptBlueprint(corpus_tree=corpus_testee1)

        assert bp.dependencies == []

    def test_default_lists_are_not_shared(_, corpus_testee1):
        bp_a = PromptBlueprint(corpus_tree=corpus_testee1)
        bp_b = PromptBlueprint(corpus_tree=corpus_testee1)

        bp_a.dependencies.append(bp_b)

        assert bp_b.dependencies == []

    def test_create_empty_blueprint_default(_, corpus_testee1):
        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1
        )

        assert bp.dependencies == []


class TestDependenciesThreadedThroughConstruction:  #############################

    def test_init(_, corpus_testee1):
        dep = PromptBlueprint(corpus_tree=corpus_testee1)

        bp = PromptBlueprint(corpus_tree=corpus_testee1, dependencies=[dep])

        assert bp.dependencies == [dep]

    def test_parse(_, corpus_testee1):
        dep = PromptBlueprint(corpus_tree=corpus_testee1)

        bp = PromptBlueprint.parse(
            "    ○\n[ ] └── Project Title",
            corpus_tree=corpus_testee1,
            dependencies=[dep],
        )

        assert bp.dependencies == [dep]

    def test_create_full_blueprint(_, corpus_testee1):
        dep = PromptBlueprint(corpus_tree=corpus_testee1)

        bp = PromptBlueprint.create_full_blueprint(
            corpus_tree=corpus_testee1, dependencies=[dep]
        )

        assert bp.dependencies == [dep]

    def test_create_empty_blueprint(_, corpus_testee1):
        dep = PromptBlueprint(corpus_tree=corpus_testee1)

        bp = PromptBlueprint.create_empty_blueprint(
            corpus_tree=corpus_testee1, dependencies=[dep]
        )

        assert bp.dependencies == [dep]

    def test_create_from_node(_, corpus_testee1):
        dep = PromptBlueprint(corpus_tree=corpus_testee1)

        bp = PromptBlueprint.create_from_node(
            "Description", corpus_tree=corpus_testee1, dependencies=[dep]
        )

        assert bp.dependencies == [dep]


class TestRenderWithoutDependencies:  ###########################################

    def test_render_prompt_equals_own_only_when_empty(_, corpus_testee1):
        bp = PromptBlueprint.create_from_node(
            "Description", corpus_tree=corpus_testee1
        )

        assert bp.render_prompt() == bp.generate_prompt_without_dependencies()

    def test_render_blueprint_equals_own_only_when_empty(_, corpus_testee1):
        bp = PromptBlueprint.create_from_node(
            "Description", corpus_tree=corpus_testee1
        )

        assert (
            bp.render_blueprint()
            == bp.generate_blueprint_without_dependencies()
        )


class TestDirectDependency:  ####################################################

    def test_render_prompt_includes_dependency_content(_, corpus_testee1):
        dep = PromptBlueprint.create_from_node(
            "License", corpus_tree=corpus_testee1
        )
        bp = PromptBlueprint.create_from_node(
            "Description", corpus_tree=corpus_testee1, dependencies=[dep]
        )

        opt = bp.render_prompt()

        assert "Brief overview of the project and its purpose." in opt
        assert "Licensed under the MIT License." in opt

    def test_render_blueprint_includes_dependency_content(_, corpus_testee1):
        dep = PromptBlueprint.create_from_node(
            "License", corpus_tree=corpus_testee1
        )
        bp = PromptBlueprint.create_from_node(
            "Description", corpus_tree=corpus_testee1, dependencies=[dep]
        )

        opt = bp.render_blueprint()

        assert "Description" in opt
        assert "License" in opt

    def test_own_only_render_excludes_dependency_content(_, corpus_testee1):
        dep = PromptBlueprint.create_from_node(
            "License", corpus_tree=corpus_testee1
        )
        bp = PromptBlueprint.create_from_node(
            "Description", corpus_tree=corpus_testee1, dependencies=[dep]
        )

        opt = bp.generate_prompt_without_dependencies()

        assert "Licensed under the MIT License." not in opt


class TestTransitiveDependency:  ################################################

    def test_chain_pulls_in_grandparent_dependency(_, corpus_testee1):
        # A -> B -> C
        c = PromptBlueprint.create_from_node(
            "License", corpus_tree=corpus_testee1
        )
        b = PromptBlueprint.create_from_node(
            "Installation", corpus_tree=corpus_testee1, dependencies=[c]
        )
        a = PromptBlueprint.create_from_node(
            "Description", corpus_tree=corpus_testee1, dependencies=[b]
        )

        opt = a.render_prompt()

        assert "Brief overview of the project and its purpose." in opt
        assert "Clone the repo and install dependencies." in opt
        assert "Licensed under the MIT License." in opt


class TestDiamondDependency:  ###################################################

    def test_diamond_does_not_duplicate_shared_dependency(_, corpus_testee1):
        # A depends on B and D, both depending on C
        c = PromptBlueprint.create_from_node(
            "License", corpus_tree=corpus_testee1
        )
        b = PromptBlueprint.create_from_node(
            "Installation", corpus_tree=corpus_testee1, dependencies=[c]
        )
        d = PromptBlueprint.create_from_node(
            "Description", corpus_tree=corpus_testee1, dependencies=[c]
        )
        a = PromptBlueprint(
            corpus_tree=corpus_testee1, dependencies=[b, d]
        )

        opt = a.render_prompt()

        assert opt.count("Licensed under the MIT License.") == 1


class TestCycleDetection:  ######################################################

    def test_direct_self_cycle_raises(_, corpus_testee1):
        bp = PromptBlueprint(corpus_tree=corpus_testee1)
        bp.dependencies.append(bp)

        with pytest.raises(ValueError):
            bp.render_prompt()

    def test_mutual_cycle_raises(_, corpus_testee1):
        a = PromptBlueprint(corpus_tree=corpus_testee1)
        b = PromptBlueprint(corpus_tree=corpus_testee1)
        a.dependencies.append(b)
        b.dependencies.append(a)

        with pytest.raises(ValueError):
            a.render_prompt()


class TestDependenciesPreservedAcrossOps:  ######################################

    def test_prune_preserves_dependencies(_, corpus_testee1):
        dep = PromptBlueprint(corpus_tree=corpus_testee1)
        bp = PromptBlueprint.create_from_node(
            "Description", corpus_tree=corpus_testee1, dependencies=[dep]
        )

        pruned = bp.prune()

        assert pruned.dependencies == [dep]

    def test_merge_unions_dependencies(_, corpus_testee1):
        dep_a = PromptBlueprint(corpus_tree=corpus_testee1)
        dep_b = PromptBlueprint(corpus_tree=corpus_testee1)
        bp_a = PromptBlueprint(
            corpus_tree=corpus_testee1, dependencies=[dep_a]
        )
        bp_b = PromptBlueprint(
            corpus_tree=corpus_testee1, dependencies=[dep_b]
        )

        merged = bp_a.merge(bp_b)

        assert merged.dependencies == [dep_a, dep_b]

    def test_merge_deduplicates_shared_dependency(_, corpus_testee1):
        shared = PromptBlueprint(corpus_tree=corpus_testee1)
        bp_a = PromptBlueprint(
            corpus_tree=corpus_testee1, dependencies=[shared]
        )
        bp_b = PromptBlueprint(
            corpus_tree=corpus_testee1, dependencies=[shared]
        )

        merged = bp_a.merge(bp_b)

        assert merged.dependencies == [shared]

    def test_copy_preserves_dependencies(_, corpus_testee1):
        dep = PromptBlueprint(corpus_tree=corpus_testee1)
        bp = PromptBlueprint(corpus_tree=corpus_testee1, dependencies=[dep])

        copied = copy.copy(bp)

        assert copied.dependencies == [dep]
