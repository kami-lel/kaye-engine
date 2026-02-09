"""
prompt_node_preview_test.py

Unit Tests (using pytest) for:

- PromptCorpusNode.generate_prompt_tree_preview()
- PromptCorpusNode.__repr__()
"""


class TestPrompt1:  ############################################################

    STR_CONTENT = """○
└── Project Title
    ├── Description
    │   Brief overview of the project and its purpose.
    ├── Installation
    │   Clone the repo and install dependencies.
    └── License
        Licensed under the MIT License."""

    def test_norm(self, test_corpus1):
        opt = test_corpus1.generate_prompt_tree_preview()
        print(opt)
        assert opt == self.STR_CONTENT

    def test_no_content(self, test_corpus1):
        opt = test_corpus1.generate_prompt_tree_preview(content_preview_lines=0)
        print(opt)
        assert opt == """○
└── Project Title
    ├── Description
    ├── Installation
    └── License"""

    def test_limited_width(self, test_corpus1):
        opt = test_corpus1.generate_prompt_tree_preview(
            content_preview_width=12
        )
        print(opt)
        assert opt == """○
└── Project Title
    ├── Description
    │   Brie
    ├── Installation
    │   Clon
    └── License
        Lice"""

    def test_repr(self, test_corpus1):
        opt = repr(test_corpus1)
        print(opt)
        assert opt == self.STR_CONTENT


class TestPrompt2:  ############################################################

    STR_CONTENT = """○
└── Project Title
    ├── Description
    │   A brief overview of the project, its purpose, and goals.
    ├── Installation
    │   1. Clone the repo
    │   2. Install dependencies
    │   3. Run the application
    ├── Usage
    │   Provide instructions on how to use the application.
    ├── Contributing
    │   1. Fork the repo
    │   2. Create a new branch
    │   3. Submit a pull request
    └── License
        This project is licensed under the MIT License."""

    def test_norm(self, test_corpus2):
        opt = test_corpus2.generate_prompt_tree_preview()
        print(opt)
        assert opt == self.STR_CONTENT

    def test_no_content(self, test_corpus2):
        opt = test_corpus2.generate_prompt_tree_preview(content_preview_lines=0)
        print(opt)
        assert opt == """○
└── Project Title
    ├── Description
    ├── Installation
    ├── Usage
    ├── Contributing
    └── License"""

    def test_limited_line_count(self, test_corpus2):
        opt = test_corpus2.generate_prompt_tree_preview(content_preview_lines=1)
        print(opt)
        assert opt == """○
└── Project Title
    ├── Description
    │   A brief overview of the project, its purpose, and goals.
    ├── Installation
    │   1. Clone the repo
    ├── Usage
    │   Provide instructions on how to use the application.
    ├── Contributing
    │   1. Fork the repo
    └── License
        This project is licensed under the MIT License."""

    def test_limited_width(self, test_corpus2):
        opt = test_corpus2.generate_prompt_tree_preview(
            content_preview_width=15
        )
        print(opt)
        assert opt == """○
└── Project Title
    ├── Description
    │   A brief
    ├── Installation
    │   1. Clon
    │   2. Inst
    │   3. Run 
    ├── Usage
    │   Provide
    ├── Contributing
    │   1. Fork
    │   2. Crea
    │   3. Subm
    └── License
        This pr"""

    def test_repr(self, test_corpus2):
        opt = repr(test_corpus2)
        print(opt)
        assert opt == self.STR_CONTENT


class TestPrompt3:  ############################################################

    STR_CONTENT = """○
└── Main Title
    ├── Introduction
    │   Brief introduction to the topic.
    │   └── Background
    │       Context or history relevant to the topic.
    │       └── Importance
    │           Why this topic matters in the current scenario.
    │           └── Objective
    │               The primary goal of this document.
    ├── Methods
    │   Overview of the methodologies used.
    │   └── Data Collection
    │       How data was gathered for analysis.
    │       └── Tools Used
    │           List of tools utilized during the project.
    │           └── Future Work
    │               Suggestions for future research or tasks.
    └── Conclusion
        Summarizing the findings and implications."""

    def test_norm(self, test_corpus3):
        opt = test_corpus3.generate_prompt_tree_preview()
        print(opt)
        assert opt == self.STR_CONTENT

    def test_no_content(self, test_corpus3):
        opt = test_corpus3.generate_prompt_tree_preview(content_preview_lines=0)
        print(opt)
        assert opt == """○
└── Main Title
    ├── Introduction
    │   └── Background
    │       └── Importance
    │           └── Objective
    ├── Methods
    │   └── Data Collection
    │       └── Tools Used
    │           └── Future Work
    └── Conclusion"""

    def test_limited_width(self, test_corpus3):
        opt = test_corpus3.generate_prompt_tree_preview(
            content_preview_width=30
        )
        print(opt)
        assert opt == """○
└── Main Title
    ├── Introduction
    │   Brief introduction to 
    │   └── Background
    │       Context or history
    │       └── Importance
    │           Why this topic
    │           └── Objective
    │               The primar
    ├── Methods
    │   Overview of the method
    │   └── Data Collection
    │       How data was gathe
    │       └── Tools Used
    │           List of tools 
    │           └── Future Work
    │               Suggestion
    └── Conclusion
        Summarizing the findin"""
