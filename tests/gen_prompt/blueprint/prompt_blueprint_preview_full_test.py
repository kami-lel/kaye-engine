"""
test .generate_preview_tree(show_full_tree=True,)
"""

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode


from tests.gen_prompt.node.testees import PROMPT1, PROMPT2

# BUG update


class Test1:  # use PROMPT1

    corpus = PromptCorpusNode.parse(PROMPT1)
    dft_preview_tree = """    ○
[ ] └── Project Title
[ ]     ├── Description
        │   A brief overview of the project, its purpose, and goals.
[ ]     ├── Installation
        │   1. Clone the repo
        │   2. Install dependencies
        │   3. Run the application
[ ]     ├── Usage
        │   Provide instructions on how to use the application.
[ ]     ├── Contributing
        │   1. Fork the repo
        │   2. Create a new branch
        │   3. Submit a pull request
[ ]     └── License
            This project is licensed under the MIT License."""

    def test_dft(self):
        pt = PromptBlueprint(self.corpus)
        opt = pt.generate_preview_tree(show_full_tree=True, hide_comment=True)

        print(opt)
        assert opt == self.dft_preview_tree

    def test_no_content(self):
        pt = PromptBlueprint(self.corpus)
        opt = pt.generate_preview_tree(
            show_full_tree=True, preview_line_count=0, hide_comment=True
        )

        print(opt)
        assert opt == """    ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[ ]     ├── Contributing
[ ]     └── License"""


class Test2:  # use PROMPT2

    corpus = PromptCorpusNode.parse(PROMPT2)
    dft_preview_tree = """    ○
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

    def test_dft(self):
        pt = PromptBlueprint(self.corpus)
        opt = pt.generate_preview_tree(show_full_tree=True, hide_comment=True)

        print(opt)
        assert opt == self.dft_preview_tree

    def test_no_content(self):
        pt = PromptBlueprint(self.corpus)
        opt = pt.generate_preview_tree(
            show_full_tree=True, preview_line_count=0, hide_comment=True
        )

        print(opt)
        assert opt == """    ○
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
