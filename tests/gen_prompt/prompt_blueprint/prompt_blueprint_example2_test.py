"""
tests features of ``PromptBlueprint`` using a full PROMPT2
"""

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode

from tests.gen_prompt.prompt_blueprint.testees import PROMPT2

example_corpus = PromptCorpusNode.parse(PROMPT2)


class TestDetachedMode:  # test detached mdoe

    def test_init_set(_):
        pt = PromptBlueprint(example_corpus, detached_mode=True)
        assert "○" not in pt.enabled_nodes_names

    def test_init_unset(_):
        pt = PromptBlueprint(example_corpus, detached_mode=False)
        assert "○" in pt.enabled_nodes_names

    def test_init_dft(_):
        pt = PromptBlueprint(example_corpus, detached_mode=False)
        assert "○" in pt.enabled_nodes_names

    def test_set1(_):  # set by set_unset_detached_mode()
        pt = PromptBlueprint(example_corpus, detached_mode=False)
        assert "○" in pt.enabled_nodes_names
        pt.set_unset_detached_mode(True)
        assert "○" not in pt.enabled_nodes_names

    def test_set2(_):
        pt = PromptBlueprint(example_corpus, detached_mode=True)
        assert "○" not in pt.enabled_nodes_names
        pt.set_unset_detached_mode(True)
        assert "○" not in pt.enabled_nodes_names

    def test_unset1(_):  # unset by set_unset_detached_mode()
        pt = PromptBlueprint(example_corpus, detached_mode=True)
        assert "○" not in pt.enabled_nodes_names
        pt.set_unset_detached_mode(False)
        assert "○" in pt.enabled_nodes_names

    def test_unset2(_):
        pt = PromptBlueprint(example_corpus, detached_mode=False)
        assert "○" in pt.enabled_nodes_names
        pt.set_unset_detached_mode(False)
        assert "○" in pt.enabled_nodes_names

    def test_is_dm1(_):  # test is_detached_mode
        pt = PromptBlueprint(example_corpus, detached_mode=True)
        assert pt.is_detached_mode

    def test_is_dm2(_):
        pt = PromptBlueprint(example_corpus, detached_mode=False)
        assert not pt.is_detached_mode


class TestStr:

    def test1(_):
        blueprint_text = """    ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == ""

    def test2(_):
        blueprint_text = """    ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
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

    def test2_no_ver(_):
        blueprint_text = """    ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
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
        blueprint_text = """    ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
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
        blueprint_text = """    ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == """# Main Title
## Methods
Overview of the methodologies used.
### Data Collection
How data was gathered for analysis.
## Conclusion
Summarizing the findings and implications."""

    def test_full(_):
        blueprint_text = """    ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
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
        blueprint_text = """[ ] ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
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
        blueprint_text = """[ ] ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == ""

    def test_empty_version(_):
        blueprint_text = """[ ] ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == ""

    def test1(_):
        blueprint_text = """[ ] ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
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
        blueprint_text = """[ ] ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
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

    def test2_no_ver(_):
        blueprint_text = """[ ] ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
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
        blueprint_text = """[ ] ○
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

        pt = PromptBlueprint(example_corpus, blueprint_text)

        opt = pt.generate_prompt(hide_comment=True)
        print(opt)
        assert opt == """# Main Title
### Background
Context or history relevant to the topic.
## Methods
Overview of the methodologies used.
##### Future Work
Suggestions for future research or tasks."""
