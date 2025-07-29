"""
test for ``load_embedded_prompt_corpus``
"""

from os.path import dirname, abspath, join, normpath

from kaye.gen_prompt import (
    load_embedded_prompt_corpus,
    get_embedded_prompt_corpus_file_path,
    PromptCorpusNode,
)


class TestGet:  # test function get_embedded_prompt_corpus_file_path

    # !!! this test change with prompt_corpus.md
    def test1(_):
        submission = get_embedded_prompt_corpus_file_path()
        solution = normpath(
            join(
                dirname(abspath(__file__)),
                "../../../kaye/kaye/prompt_corpus.md",
            )
        )
        print("submission:\t{}\nsolution:\t{}".format(submission, solution))
        assert str(submission) == solution


class TestLoad:  # test function load_embedded_prompt_corpus
    def test_type(_):
        opt = load_embedded_prompt_corpus()
        assert isinstance(opt, PromptCorpusNode)

    # !!! this test change with prompt_corpus.md
    def test_struture(_):
        root = load_embedded_prompt_corpus()

        testee = root.__repr__(preview_line_count=0)
        print(testee)

        assert testee == """○
├── Introduction
├── Personality
├── Conversation
│   └── Conversation Language
├── Format Guidelines
├── Commentary Language
├── Role
│   ├── Art Tutor
│   │   ├── A: Information Gathering
│   │   └── B: Prompt Generation
│   ├── Bibliographer
│   ├── Book Buddy
│   │   └── Reading Notes Guidelines
│   ├── Changelog Writer
│   ├── Conversation Follow Up Generation
│   ├── Conversation Tag Generation
│   │   ├── Guidelines
│   │   ├── Output
│   │   └── Chat History
│   ├── Conversation Title Generation
│   │   ├── Guidelines
│   │   ├── Output
│   │   ├── Examples
│   │   └── Chat History
│   ├── Deutschlehrer
│   ├── Editor
│   ├── Email Secretary
│   ├── Encyclopedic
│   ├── Etiquette Coach
│   ├── Event Search
│   ├── git commit message
│   ├── git diff Summary
│   ├── Grammar Checker
│   ├── Librarian
│   │   ├── label
│   │   │   ├── book title
│   │   │   ├── publish year
│   │   │   ├── authors, editors, translators
│   │   │   ├── publisher
│   │   │   ├── informational tags
│   │   │   └── label examples
│   │   ├── DDC part
│   │   └── DDC justification
│   ├── zh Librarian
│   │   ├── DDC 部分
│   │   └── DDC 說明
│   ├── Peer Coder
│   │   ├── C & C++
│   │   ├── C Sharp
│   │   ├── Unity Engine
│   │   ├── GDScript
│   │   ├── HTML
│   │   ├── JavaScript & TypeScript
│   │   │   ├── Naming Conventions
│   │   │   └── Documentation and Comments
│   │   ├── Qt
│   │   │   └── QML Coding Conventions
│   │   └── Python
│   │       ├── Docstring Style
│   │       └── Testing Guidelines
│   ├── Prompt Writer
│   ├── Renamer
│   ├── Tarot Reader
│   │   ├── 1. Information Collection Stage
│   │   ├── 2. Card Drawing Stage
│   │   ├── II: Card Name
│   │   ├── 3. Interpretation Stage
│   │   └── Tarot Card Reference
│   └── Translator
└── Abbreviation"""
