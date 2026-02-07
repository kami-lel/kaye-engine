"""
prompt_plc_test.py

Unit Tests (using pytest) for:

- PLCNode
"""

from kaye.gen_prompt import PromptCorpusNode
from kaye.gen_prompt.abbr_nodes import PLCNode


from tests.prompt import PROMPT1

tree = PromptCorpusNode.parse(PROMPT1)


class TestPLC:

    node = PLCNode(tree)

    def test_init(self):
        self.node.parent is tree
        self.node.name == "Programming Languages Code"
        self.node.id == "{Programming Languages Code}"

    def test_preview(self):
        opt = tree.generate_prompt_tree_preview(content_preview_lines=0)
        print(opt)
        assert opt == """○
├── Project Title
│   ├── Description
│   ├── Installation
│   └── License
└── Programming Languages Code"""

    def test_content_lines(self):
        lines = self.node.content_lines()
        print(lines)
        assert lines == [
            "-`console`:any types of terminal console & log message",
            "-`c`:C language",
            "-`csharp`:C Sharp",
            "-`cpp`:C++",
            "-`css`:CSS",
            "-`gdscript`:GDScript used by Godot Engine",
            "-`html`:HTML",
            "-`js`:JavaScript",
            "-`py`:Python",
            "-`qt`:Qt framework",
            "-`qml`:QT Meta-object Language",
            "-`ts`:TypeScript",
            "-`u3d`:Unity Engine code using C#",
            "-`ue`:Unreal Engine code using C++",
        ]
