"""
today_node.py

define ``TodayNode``
"""

from datetime import datetime

from .base_prompt_node import DynamicNode

TODAY_NODE_HEADING = "Today"


class TodayNode(DynamicNode):
    """
    a dynamic node to provide today's **date** and current **time**


    :param parent:
    :type parent: BasePromptNode
    """

    # constructor  =============================================================

    def __init__(self, parent):
        super().__init__(TODAY_NODE_HEADING, parent)

    # implement BasePromptNode  ================================================
    @property
    def content_lines(self):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        return ["Today: {}".format(date), "Time: {}".format(time)]
