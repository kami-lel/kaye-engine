
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

##### Obj2
The secondary goal of this document.





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



def test_render_all():
    tree.set()

    assert str(tree) == \
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

##### Obj2
The secondary goal of this document.

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


def test_render_intro():
    tree.unset()
    tree['Main Title']['Intro'].set()

    assert str(tree) == \
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

##### Obj2
The secondary goal of this document.
"""


def test_render_obj():
    tree.unset()
    tree['Main Title']['Intro']['Background']['Importance']['Obj2'].set()

    assert str(tree) == \
"""
# Main Title

## Intro
Brief introduction to the topic.

### Background
Context or history relevant to the topic.

#### Importance
Why this topic matters in the current scenario.

##### Obj2
The secondary goal of this document.
"""
