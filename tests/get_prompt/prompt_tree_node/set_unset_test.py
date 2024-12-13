
from kaye.get_prompt.prompt_tree_node import PromptTreeNode


src = \
"""
# Main Title

## Intro
Brief introduction to the topic.

### Background
Context or history relevant to the topic.

#### Importance
Why this topic matters in the current scenario.

##### Obj
The primary goal of this document.

## Methods
Overview of the methodologies used.

### Data Collection
How data was gathered for analysis.

#### TU
List of tools utilized during the project.

##### FW
Suggestions for future research or tasks.

## Conclusion
Summarizing the findings and implications.
"""


tree = PromptTreeNode(src)
proj = tree['Main Title']



class TestRoot:

    def test_set(_):
        tree.set()

        assert tree.enable
        assert proj.enable
        assert proj['Intro'].enable
        assert proj['Intro']['Background'].enable
        assert proj['Intro']['Background']['Importance'].enable
        assert proj['Intro']['Background']['Importance']['Obj'].enable
        assert proj['Methods'].enable
        assert proj['Methods']['Data Collection'].enable
        assert proj['Methods']['Data Collection']['TU'].enable
        assert proj['Methods']['Data Collection']['TU']['FW'].enable
        assert proj['Conclusion'].enable

    def test_unset(_):
        tree.unset()

        assert not tree.enable
        assert not proj.enable
        assert not proj['Intro'].enable
        assert not proj['Intro']['Background'].enable
        assert not proj['Intro']['Background']['Importance'].enable
        assert not proj['Intro']['Background']['Importance']['Obj'].enable
        assert not proj['Methods'].enable
        assert not proj['Methods']['Data Collection'].enable
        assert not proj['Methods']['Data Collection']['TU'].enable
        assert not proj['Methods']['Data Collection']['TU']['FW'].enable
        assert not proj['Conclusion'].enable


class TestPart:

    def test_intro(_):
        tree.unset()  # init tree

        proj['Intro'].set()

        assert tree.enable
        assert proj.enable
        assert proj['Intro'].enable
        assert proj['Intro']['Background'].enable
        assert proj['Intro']['Background']['Importance'].enable
        assert proj['Intro']['Background']['Importance']['Obj'].enable
        assert not proj['Methods'].enable
        assert not proj['Methods']['Data Collection'].enable
        assert not proj['Methods']['Data Collection']['TU'].enable
        assert not proj['Methods']['Data Collection']['TU']['FW'].enable
        assert not proj['Conclusion'].enable
