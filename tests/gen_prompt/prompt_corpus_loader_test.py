"""
test for ``load_embedded_prompt_corpus``
"""

from kaye.gen_prompt import load_embedded_prompt_corpus, PromptCorpusNode


class Test:
    def test_type(_):
        opt = load_embedded_prompt_corpus()
        assert isinstance(opt, PromptCorpusNode)

    # !!! this test change with prompt_corpus.md
    def test_struture(_):
        root = load_embedded_prompt_corpus()

        testee = root.__repr__(preview_line_count=0)
        print(testee)

        assert testee == """○
├── Personality
├── Character
├── Conversation
├── Format Guidelines
├── Abbreviation
└── Role
    ├── Biliographer
    ├── Book Buddy
    │   └── Reading Notes Guidelines
    ├── Code Assistant
    │   ├── C & C++
    │   ├── C Sharp
    │   ├── Unity Engine
    │   ├── GDScript
    │   ├── HTML
    │   ├── JavaScript & TypeScript
    │   │   ├── Naming Conventions
    │   │   └── Documentation and Comments
    │   └── Python
    │       ├── Docstring Style
    │       └── Testing Guidelines
    ├── Conversation Title Generation
    │   ├── Guidelines
    │   ├── Output
    │   ├── Examples
    │   └── Chat History
    ├── Conversation Tag Generation
    │   ├── Guidelines
    │   ├── Output
    │   └── Chat History
    ├── Deutschlehrer
    ├── Editor Role
    ├── Email Secretary
    ├── Encyclopedic
    ├── Etiquette Coach
    ├── Event Search
    ├── git commit message
    ├── git diff Summary
    ├── Grammar Checker
    ├── Librarian
    │   ├── label
    │   │   ├── book title
    │   │   ├── publish year
    │   │   ├── authors, editors, translators
    │   │   ├── publisher
    │   │   ├── informational tags
    │   │   └── label examples
    │   ├── DDC part
    │   └── DDC justification
    ├── zh Librarian
    │   ├── DDC 部分
    │   └── DDC 說明
    ├── Prompt Writer
    └── Translator"""
