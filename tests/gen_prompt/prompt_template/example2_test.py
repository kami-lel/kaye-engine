"""
tests features of ``PromptTemplate`` using a 2nd example full prompt
"""

from kaye.gen_prompt import PromptTemplate, FullPromptParserNode

FULL_PROMPT = """
# Main Title

## Introduction
Brief introduction to the topic.

### Background
Context or history relevant to the topic.

#### Importance
Why this topic matters in the current scenario.

##### Objective
The primary goal of this document.

## Methods
Overview of the methodologies used.

### Data Collection
How data was gathered for analysis.

#### Tools Used
List of tools utilized during the project.

##### Future Work
Suggestions for future research or tasks.

## Conclusion
Summarizing the findings and implications.
"""


example_tree = FullPromptParserNode.parse(FULL_PROMPT)


class TestRepr:

    def test_dft(_):
        pt = PromptTemplate(full_prompt_tree=example_tree)
        opt = repr(pt)
        print(opt)
        assert opt == """[x] ○
[ ] └── Main Title
[ ]     ├── Introduction
        │   Brief introduction to the topic.
[ ]     │   └── Background
        │       Context or history relevant to the topic.
[ ]     │       └── Importance
        │           Why this topic matters in the current scenario.
[ ]     │           └── Objective
        │               The primary goal of this document.
[ ]     ├── Methods
        │   Overview of the methodologies used.
[ ]     │   └── Data Collection
        │       How data was gathered for analysis.
[ ]     │       └── Tools Used
        │           List of tools utilized during the project.
[ ]     │           └── Future Work
        │               Suggestions for future research or tasks.
[ ]     └── Conclusion
            Summarizing the findings and implications."""

    def test_no_content(_):
        pt = PromptTemplate(full_prompt_tree=example_tree)
        opt = pt.__repr__(preview_line_count=0)
        print(opt)
        assert opt == """[x] ○
[ ] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[ ]     └── Conclusion"""


class TestDetachedMode:  # test detached mdoe

    def test_init_set(_):
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=True)
        assert "○" not in pt.enabled_nodes_names

    def test_init_unset(_):
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=False)
        assert "○" in pt.enabled_nodes_names

    def test_init_dft(_):
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=False)
        assert "○" in pt.enabled_nodes_names

    def test_set1(_):  # set by set_unset_detached_mode()
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=False)
        assert "○" in pt.enabled_nodes_names
        pt.set_unset_detached_mode(True)
        assert "○" not in pt.enabled_nodes_names

    def test_set2(_):
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=True)
        assert "○" not in pt.enabled_nodes_names
        pt.set_unset_detached_mode(True)
        assert "○" not in pt.enabled_nodes_names

    def test_unset1(_):  # unset by set_unset_detached_mode()
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=True)
        assert "○" not in pt.enabled_nodes_names
        pt.set_unset_detached_mode(False)
        assert "○" in pt.enabled_nodes_names

    def test_unset2(_):
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=False)
        assert "○" in pt.enabled_nodes_names
        pt.set_unset_detached_mode(False)
        assert "○" in pt.enabled_nodes_names

    def test_is_dm1(_):  # test is_detached_mode
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=True)
        assert pt.is_detached_mode

    def test_is_dm2(_):
        pt = PromptTemplate(full_prompt_tree=example_tree, detached_mode=False)
        assert not pt.is_detached_mode


class TestParseSavable:

    def test_empty(_):
        savable_prompt_template = """[x] ○
[ ] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[ ]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        assert len(pt.enabled_nodes_names) == 1
        assert "○" in pt.enabled_nodes_names
        assert "Main Title" not in pt.enabled_nodes_names
        assert "Introduction" not in pt.enabled_nodes_names
        assert "Background" not in pt.enabled_nodes_names
        assert "Importance" not in pt.enabled_nodes_names
        assert "Objective" not in pt.enabled_nodes_names
        assert "Methods" not in pt.enabled_nodes_names
        assert "Data Collection" not in pt.enabled_nodes_names
        assert "Tools Used" not in pt.enabled_nodes_names
        assert "Future Work" not in pt.enabled_nodes_names
        assert "Conclusion" not in pt.enabled_nodes_names

        assert not pt.is_detached_mode

    def test_full(_):
        savable_prompt_template = """[x] ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[x]     ├── Methods
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        assert len(pt.enabled_nodes_names) == 11
        assert "○" in pt.enabled_nodes_names
        assert "Main Title" in pt.enabled_nodes_names
        assert "Introduction" in pt.enabled_nodes_names
        assert "Background" in pt.enabled_nodes_names
        assert "Importance" in pt.enabled_nodes_names
        assert "Objective" in pt.enabled_nodes_names
        assert "Methods" in pt.enabled_nodes_names
        assert "Data Collection" in pt.enabled_nodes_names
        assert "Tools Used" in pt.enabled_nodes_names
        assert "Future Work" in pt.enabled_nodes_names
        assert "Conclusion" in pt.enabled_nodes_names

        assert not pt.is_detached_mode

    def test1(_):
        savable_prompt_template = """[x] ○
[x] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        assert len(pt.enabled_nodes_names) == 5
        assert "○" in pt.enabled_nodes_names
        assert "Main Title" in pt.enabled_nodes_names
        assert "Introduction" not in pt.enabled_nodes_names
        assert "Background" not in pt.enabled_nodes_names
        assert "Importance" not in pt.enabled_nodes_names
        assert "Objective" in pt.enabled_nodes_names
        assert "Methods" not in pt.enabled_nodes_names
        assert "Data Collection" not in pt.enabled_nodes_names
        assert "Tools Used" not in pt.enabled_nodes_names
        assert "Future Work" in pt.enabled_nodes_names
        assert "Conclusion" in pt.enabled_nodes_names

        assert not pt.is_detached_mode

    def test2(_):
        savable_prompt_template = """[x] ○
[ ] └── Main Title
[ ]     ├── Introduction
[x]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[x]     ├── Methods
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[ ]     │           └── Future Work
[ ]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        assert len(pt.enabled_nodes_names) == 5
        assert "○" in pt.enabled_nodes_names
        assert "Main Title" not in pt.enabled_nodes_names
        assert "Introduction" not in pt.enabled_nodes_names
        assert "Background" in pt.enabled_nodes_names
        assert "Importance" not in pt.enabled_nodes_names
        assert "Objective" not in pt.enabled_nodes_names
        assert "Methods" in pt.enabled_nodes_names
        assert "Data Collection" in pt.enabled_nodes_names
        assert "Tools Used" in pt.enabled_nodes_names
        assert "Future Work" not in pt.enabled_nodes_names
        assert "Conclusion" not in pt.enabled_nodes_names

        assert not pt.is_detached_mode

    def test_detached_mode(_):
        savable_prompt_template = """[ ] ○
[x] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        assert len(pt.enabled_nodes_names) == 4
        assert "○" not in pt.enabled_nodes_names
        assert "Main Title" in pt.enabled_nodes_names
        assert "Introduction" not in pt.enabled_nodes_names
        assert "Background" not in pt.enabled_nodes_names
        assert "Importance" not in pt.enabled_nodes_names
        assert "Objective" in pt.enabled_nodes_names
        assert "Methods" not in pt.enabled_nodes_names
        assert "Data Collection" not in pt.enabled_nodes_names
        assert "Tools Used" not in pt.enabled_nodes_names
        assert "Future Work" in pt.enabled_nodes_names
        assert "Conclusion" in pt.enabled_nodes_names

        assert pt.is_detached_mode


class TestStr:

    def test1(_):
        savable_prompt_template = """[x] ○
[ ] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[ ]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        opt = str(pt)
        print(opt)
        assert opt == ""

    def test2(_):
        savable_prompt_template = """[x] ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        opt = str(pt)
        print(opt)
        assert opt == """# Main Title
## Introduction
Brief introduction to the topic.
### Background
Context or history relevant to the topic.
#### Importance
Why this topic matters in the current scenario.
##### Objective
The primary goal of this document.
## Conclusion
Summarizing the findings and implications."""

    def test3(_):
        savable_prompt_template = """[x] ○
[x] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[x]     ├── Methods
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        opt = str(pt)
        print(opt)
        assert opt == """# Main Title
## Methods
Overview of the methodologies used.
### Data Collection
How data was gathered for analysis.
#### Tools Used
List of tools utilized during the project.
##### Future Work
Suggestions for future research or tasks.
## Conclusion
Summarizing the findings and implications."""

    def test4(_):
        savable_prompt_template = """[x] ○
[x] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[x]     ├── Methods
[x]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        opt = str(pt)
        print(opt)
        assert opt == """# Main Title
## Methods
Overview of the methodologies used.
### Data Collection
How data was gathered for analysis.
## Conclusion
Summarizing the findings and implications."""

    def test_full(_):
        savable_prompt_template = """[x] ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[x]     ├── Methods
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        opt = str(pt)
        print(opt)
        assert opt == """# Main Title
## Introduction
Brief introduction to the topic.
### Background
Context or history relevant to the topic.
#### Importance
Why this topic matters in the current scenario.
##### Objective
The primary goal of this document.
## Methods
Overview of the methodologies used.
### Data Collection
How data was gathered for analysis.
#### Tools Used
List of tools utilized during the project.
##### Future Work
Suggestions for future research or tasks.
## Conclusion
Summarizing the findings and implications."""


class TestStrDetach:  # test detached mode

    def test_full(_):
        savable_prompt_template = """[ ] ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[x]     ├── Methods
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        opt = str(pt)
        print(opt)
        assert opt == """# Main Title
## Introduction
Brief introduction to the topic.
### Background
Context or history relevant to the topic.
#### Importance
Why this topic matters in the current scenario.
##### Objective
The primary goal of this document.
## Methods
Overview of the methodologies used.
### Data Collection
How data was gathered for analysis.
#### Tools Used
List of tools utilized during the project.
##### Future Work
Suggestions for future research or tasks.
## Conclusion
Summarizing the findings and implications."""

    def test_empty(_):
        savable_prompt_template = """[ ] ○
[ ] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[ ]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        opt = str(pt)
        print(opt)
        assert opt == ""

    def test1(_):
        savable_prompt_template = """[ ] ○
[ ] └── Main Title
[x]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[x]     │       └── Tools Used
[ ]     │           └── Future Work
[x]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        opt = str(pt)
        print(opt)
        assert opt == """## Introduction
Brief introduction to the topic.
##### Objective
The primary goal of this document.
#### Tools Used
List of tools utilized during the project.
## Conclusion
Summarizing the findings and implications."""

    def test2(_):
        savable_prompt_template = """[ ] ○
[ ] └── Main Title
[x]     ├── Introduction
[ ]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[x]     │       └── Tools Used
[x]     │           └── Future Work
[ ]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        opt = str(pt)
        print(opt)
        assert opt == """## Introduction
Brief introduction to the topic.
#### Importance
Why this topic matters in the current scenario.
##### Objective
The primary goal of this document.
#### Tools Used
List of tools utilized during the project.
##### Future Work
Suggestions for future research or tasks."""

    def test3(_):
        savable_prompt_template = """[ ] ○
[x] └── Main Title
[ ]     ├── Introduction
[x]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[x]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[x]     │           └── Future Work
[ ]     └── Conclusion"""

        pt = PromptTemplate(
            savable_prompt_template, full_prompt_tree=example_tree
        )

        opt = str(pt)
        print(opt)
        assert opt == """# Main Title
### Background
Context or history relevant to the topic.
## Methods
Overview of the methodologies used.
##### Future Work
Suggestions for future research or tasks."""
