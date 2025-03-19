"""
test for ``load_current_full_prompt_tree``
"""

from kaye.gen_prompt import load_current_full_prompt_tree, FullPromptParserNode


class Test:
    def test_type(_):
        opt = load_current_full_prompt_tree()
        assert isinstance(opt, FullPromptParserNode)

    def test_struture(_):
        root = load_current_full_prompt_tree()

        assert root.__repr__(preview_line_count=0) == """○
├── Personality
├── Character
├── Conversation
├── Format Guidelines
├── Abbreviation
└── Role
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
    ├── Editor
    ├── Email Secretary
    ├── Encyclopedic
    ├── Etiquette Coach
    ├── Event Search
    ├── git commit message
    ├── git diff Summary
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
