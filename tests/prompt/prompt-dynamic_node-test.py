"""
prompt-dynamic_node-test.py

Unit Tests (using pytest) for: DynamicNode
"""

import pytest

from kaye.gen_prompt.base_prompt_node import DynamicNode


# helpers  #####################################################################
class DynamicTestee(DynamicNode):

    # implement BasePromptNode  ================================================

    def content_lines(self, **kwargs):
        """
        :return: content **lines** this node as appeared in concrete prompt;
                each element in ``list`` is a single line
        :rtype: list[str]
        """
        raise NotImplementedError

    def __copy__(self):
        """
        :return: a shallow copy **without** any children
        :rtype: BasePromptNode
        """
        raise NotImplementedError


@pytest.fixture
def testee1():
    return DynamicTestee("Testee Node", None)


class TestId:  #################################################################

    def test1(_, testee1):
        print(testee1.id)
        assert testee1.id == "{Testee Node}"


class TestNoChild:  ############################################################

    def test1(_, testee1):
        with pytest.raises(TypeError) as exec_info:
            DynamicTestee("Parent", None, children=[testee1])

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == "<class 'tests.prompt.prompt-dynamic_node-test.DynamicTestee'> "
            "must be leaf node"
        )

    def test2(_, testee1):
        with pytest.raises(TypeError) as exec_info:
            parent = DynamicTestee("Parent", None)
            parent.children = [testee1]

        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == "<class 'tests.prompt.prompt-dynamic_node-test.DynamicTestee'> "
            "must be leaf node"
        )
