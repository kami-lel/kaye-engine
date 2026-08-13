"""
prompt-dynamic_node-test.py

Unit Tests (using pytest) for: DynamicNode
"""

import pytest

from kaye_engine.prompt.dynamic_nodes import DynamicNode


# helpers  #####################################################################
class DynamicTestee(DynamicNode):

    # implement DynamicNode  ===================================================

    NAME = "testee-node"

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
    return DynamicTestee(None)


class TestName:  #################################################################

    def test1(_, testee1):
        opt = testee1.name
        print(opt)
        assert opt == "(testee-node)"


class TestNoChild:  ############################################################

    def test1(_, testee1):
        with pytest.raises(TypeError) as exec_info:
            DynamicTestee(None, children=[testee1])

        opt = exec_info.value.args[0]
        print(opt)
        assert (
            opt
            == "<class 'prompt-dn-dynamic_node_test.DynamicTestee'> "
            "must be leaf node"
        )

    def test2(_, testee1):
        with pytest.raises(TypeError) as exec_info:
            parent = DynamicTestee(None)
            parent.children = [testee1]

        opt = exec_info.value.args[0]
        print(opt)

        assert (
            opt
            == "<class 'prompt-dn-dynamic_node_test.DynamicTestee'> "
            "must be leaf node"
        )
