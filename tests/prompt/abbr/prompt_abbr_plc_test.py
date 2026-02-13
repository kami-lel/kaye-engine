"""
prompt_plc_test.py

Unit Tests (using pytest) for:

- PLCNode
"""

import pytest

from kaye.gen_prompt.abbr_nodes import PLCNode


@pytest.fixture
def plc_node_testee1(corpus_testee1):
    return PLCNode(corpus_testee1)


class TestPLC:

    def test_init(self, plc_node_testee1, corpus_testee1):
        plc_node_testee1.parent is corpus_testee1
        plc_node_testee1.name == "Programming Languages Code"
        plc_node_testee1.id == "{Programming Languages Code}"

    def test_preview(self, corpus_testee1, plc_node_testee1):
        plc_node_testee1  # force call to add self to tree
        opt = corpus_testee1.generate_prompt_tree_preview(
            content_preview_lines=0
        )
        print(opt)
        assert opt == """○
├── Project Title
│   ├── Description
│   ├── Installation
│   └── License
└── Programming Languages Code"""

    def test_content_lines(self, plc_node_testee1):
        lines = plc_node_testee1.content_lines()
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
