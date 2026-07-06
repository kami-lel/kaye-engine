"""
today_node.py

define ``TodayNode``
"""

from datetime import datetime

from .dynamic_node import DynamicNode

__all__ = ("TodayNode",)


# FIXME FIXME refactorize today node


class TodayNode(DynamicNode):
    """
    a dynamic node to provide today's **date** and current **time**


    :param parent:
    :type parent: BasePromptNode
    """

    # implement DynamicNode  ===================================================

    HEADING = "Today"

    # implement BasePromptNode  ================================================

    def content_lines(self, **kwargs):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        return ["Today: {}".format(date), "Time: {}".format(time)]

    def __copy__(self):
        return TodayNode(None)
