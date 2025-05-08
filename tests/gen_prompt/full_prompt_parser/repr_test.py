"""
test ``__repr__()`` for FullPromptParser
"""

from kaye.gen_prompt import PromptCorpusNode
from tests.gen_prompt.pcn.testee_corpus import (
    PROMPT1,
    PROMPT2,
    PROMPT3,
)


class Test1:

    def test_norm(_):
        tree = PromptCorpusNode.parse(PROMPT1)

        assert repr(tree) == """○
└── Project Title
    ├── Description
    │   Brief overview of the project and its purpose.
    ├── Installation
    │   Clone the repo and install dependencies.
    └── License
        Licensed under the MIT License."""

    def test_no_content(_):
        tree = PromptCorpusNode.parse(PROMPT1)
        result = tree.__repr__(preview_line_count=0)

        assert result == """○
└── Project Title
    ├── Description
    ├── Installation
    └── License"""

    def test_limited_width(_):
        tree = PromptCorpusNode.parse(PROMPT1)
        result = tree.__repr__(preview_line_width=3)

        assert result == """○
└── Project Title
    ├── Description
    │   Bri
    ├── Installation
    │   Clo
    └── License
        Lic"""


class Test2:

    def test_norm(_):
        tree = PromptCorpusNode.parse(PROMPT2)

        assert repr(tree) == """○
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

    def test_no_content(_):
        tree = PromptCorpusNode.parse(PROMPT2)
        result = tree.__repr__(preview_line_count=0)

        assert result == """○
└── Project Title
    ├── Description
    ├── Installation
    ├── Usage
    ├── Contributing
    └── License"""

    def test_limit_line(_):
        tree = PromptCorpusNode.parse(PROMPT2)
        result = tree.__repr__(preview_line_count=1)

        assert result == """○
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

    def test_limited_width(_):
        tree = PromptCorpusNode.parse(PROMPT2)
        result = tree.__repr__(preview_line_width=7)

        assert result == """○
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


class Test3:

    def test_norm(_):
        tree = PromptCorpusNode.parse(PROMPT3)

        assert repr(tree) == """○
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

    def test_no_content(_):
        tree = PromptCorpusNode.parse(PROMPT3)
        result = tree.__repr__(preview_line_count=0)

        assert result == """○
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

    def test_limited_width(_):
        tree = PromptCorpusNode.parse(PROMPT3)
        result = tree.__repr__(preview_line_width=5)

        assert result == """○
└── Main Title
    ├── Introduction
    │   Brief
    │   └── Background
    │       Conte
    │       └── Importance
    │           Why t
    │           └── Objective
    │               The p
    ├── Methods
    │   Overv
    │   └── Data Collection
    │       How d
    │       └── Tools Used
    │           List 
    │           └── Future Work
    │               Sugge
    └── Conclusion
        Summa"""
