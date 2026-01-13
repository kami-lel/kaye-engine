"""
test __init__() && .generate_preview_tree() / __repr__()

with partial blueprint input, and prune_trivial_branches() (ie partial output)
"""

# HACK HACK rm

from kaye.gen_prompt import PromptBlueprint, PromptCorpusNode


from tests.gen_prompt.node.testees import PROMPT1, PROMPT2


def _remove_last_line(text):
    return "\n".join(text.split("\n")[:-1])


# BUG BUG update


class Test1:  # use PROMPT1

    corpus = PromptCorpusNode.parse(PROMPT1)

    def test_empty(self):
        blueprint_text = """    ○
[ ] └── Project Title
[ ]     └── License"""

        pt = PromptBlueprint(self.corpus, blueprint_text)
        enabled_names_path = [node.names_path for node in pt.enabled]

        preview_tree = pt.generate_preview_tree(
            show_full_tree=False, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == """    ○"""

        assert len(pt.enabled) == 0
        assert ("Project Title",) not in enabled_names_path
        assert ("Project Title", "Description") not in enabled_names_path
        assert ("Project Title", "Installation") not in enabled_names_path
        assert ("Project Title", "Usage") not in enabled_names_path
        assert ("Project Title", "Contributing") not in enabled_names_path
        assert ("Project Title", "License") not in enabled_names_path

    blueprint1_full = """    ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[x]     ├── Contributing
[ ]     └── License"""

    blueprint1_significant = """    ○
[ ] └── Project Title
[x]     └── Contributing"""

    blueprint1_repr = """    ○
[ ] └── Project Title
[x]     └── Contributing
            1. Fork the repo
            2. Create a new branch
            3. Submit a pull request"""

    def test1_part2full(self):  # input partial tree, gen full tree
        input = self.blueprint1_significant
        output = self.blueprint1_full

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = tree.generate_preview_tree(
            show_full_tree=True, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == output

        enabled_names_path = [node.names_path for node in tree.enabled]

        assert len(tree.enabled) == 1
        assert ("Project Title",) not in enabled_names_path
        assert ("Project Title", "Description") not in enabled_names_path
        assert ("Project Title", "Installation") not in enabled_names_path
        assert ("Project Title", "Usage") not in enabled_names_path
        assert ("Project Title", "Contributing") in enabled_names_path
        assert ("Project Title", "License") not in enabled_names_path

    def test1_full2part(self):  # input full tree, gen partial tree
        input = self.blueprint1_full
        output = self.blueprint1_significant

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = tree.generate_preview_tree(
            show_full_tree=False, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == output

    def test1_part2part(self):  # input part tree, gen partial tree
        input = self.blueprint1_significant
        output = self.blueprint1_significant

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = tree.generate_preview_tree(
            show_full_tree=False, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == output

    def test1_full2repr(self):  # test __repr__()
        input = self.blueprint1_full
        output = self.blueprint1_repr

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = repr(tree)

        print(preview_tree)
        assert _remove_last_line(preview_tree) == output

    blueprint2_full = """    ○
[x] └── Project Title
[ ]     ├── Description
[x]     ├── Installation
[ ]     ├── Usage
[x]     ├── Contributing
[ ]     └── License"""

    blueprint2_partial = """    ○
[x] └── Project Title
[x]     ├── Installation
[x]     ├── Contributing
[ ]     └── License"""

    blueprint2_significant = """    ○
[x] └── Project Title
[x]     ├── Installation
[x]     └── Contributing"""

    blueprint2_repr = """    ○
[x] └── Project Title
[x]     ├── Installation
        │   1. Clone the repo
        │   2. Install dependencies
        │   3. Run the application
[x]     └── Contributing
            1. Fork the repo
            2. Create a new branch
            3. Submit a pull request"""

    def test2_part2full(self):  # input partial tree, gen full tree
        input = self.blueprint2_partial
        output = self.blueprint2_full

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = tree.generate_preview_tree(
            show_full_tree=True, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == output

        enabled_names_path = [node.names_path for node in tree.enabled]

        assert len(tree.enabled) == 3
        assert ("Project Title",) in enabled_names_path
        assert ("Project Title", "Description") not in enabled_names_path
        assert ("Project Title", "Installation") in enabled_names_path
        assert ("Project Title", "Usage") not in enabled_names_path
        assert ("Project Title", "Contributing") in enabled_names_path
        assert ("Project Title", "License") not in enabled_names_path

    def test2_full2part(self):  # input full tree, gen partial tree
        input = self.blueprint2_full
        output = self.blueprint2_significant

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = tree.generate_preview_tree(
            show_full_tree=False, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == output

    def test2_part2part(self):  # input part tree, gen partial tree
        input = self.blueprint2_significant
        output = self.blueprint2_significant

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = tree.generate_preview_tree(
            show_full_tree=False, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == output

    def test2_full2repr(self):  # test __repr__()
        input = self.blueprint2_full
        output = self.blueprint2_repr

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = repr(tree)

        print(preview_tree)
        assert _remove_last_line(preview_tree) == output


class Test2:  # use PROMPT2

    corpus = PromptCorpusNode.parse(PROMPT2)

    def test_empty(self):
        blueprint_text = """    ○
[ ] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[ ]     └── Conclusion"""

        tree = PromptBlueprint(self.corpus, blueprint_text)

        assert len(tree.enabled) == 0

    blueprint1_full = """    ○
[x] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""

    blueprint1_significant = """    ○
[x] └── Main Title
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""

    blueprint1_repr = """    ○
[x] └── Main Title
[ ]     ├── Methods
        │   Overview of the methodologies used.
[ ]     │   └── Data Collection
        │       How data was gathered for analysis.
[ ]     │       └── Tools Used
        │           List of tools utilized during the project.
[x]     │           └── Future Work
        │               Suggestions for future research or tasks.
[x]     └── Conclusion
            Summarizing the findings and implications."""

    def test1_part2full(self):  # input partial tree, gen full tree
        input = self.blueprint1_significant
        output = self.blueprint1_full

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = tree.generate_preview_tree(
            show_full_tree=True, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == output

        enabled_names_path = [node.names_path for node in tree.enabled]

        assert len(tree.enabled) == 3
        assert ("Main Title",) in enabled_names_path
        assert ("Main Title", "Introduction") not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
            "Objective",
        ) not in enabled_names_path
        assert ("Main Title", "Methods") not in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
            "Future Work",
        ) in enabled_names_path
        assert ("Main Title", "Conclusion") in enabled_names_path

    def test1_full2part(self):  # input full tree, gen partial tree
        input = self.blueprint1_full
        output = self.blueprint1_significant

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = tree.generate_preview_tree(
            show_full_tree=False, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == output

    def test1_part2part(self):  # input part tree, gen partial tree
        input = self.blueprint1_significant
        output = self.blueprint1_significant

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = tree.generate_preview_tree(
            show_full_tree=False, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == output

    def test1_full2repr(self):  # test __repr__()
        input = self.blueprint1_full
        output = self.blueprint1_repr

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = repr(tree)

        print(preview_tree)
        assert _remove_last_line(preview_tree) == output

    blueprint2_full = """    ○
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

    blueprint2_partial = """    ○
[ ] └── Main Title
[ ]     ├── Introduction
[x]     │   └── Background
[x]     ├── Methods
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[ ]     └── Conclusion"""

    blueprint2_significant = """    ○
[ ] └── Main Title
[ ]     ├── Introduction
[x]     │   └── Background
[x]     └── Methods
[x]         └── Data Collection
[x]             └── Tools Used"""

    blueprint2_repr = """    ○
[ ] └── Main Title
[ ]     ├── Introduction
        │   Brief introduction to the topic.
[x]     │   └── Background
        │       Context or history relevant to the topic.
[x]     └── Methods
            Overview of the methodologies used.
[x]         └── Data Collection
                How data was gathered for analysis.
[x]             └── Tools Used
                    List of tools utilized during the project."""

    def test2_part2full(self):  # input partial tree, gen full tree
        input = self.blueprint2_partial
        output = self.blueprint2_full

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = tree.generate_preview_tree(
            show_full_tree=True, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == output

        enabled_names_path = [node.names_path for node in tree.enabled]

        assert len(tree.enabled) == 4
        assert ("Main Title",) not in enabled_names_path
        assert ("Main Title", "Introduction") not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
        ) in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
        ) not in enabled_names_path
        assert (
            "Main Title",
            "Introduction",
            "Background",
            "Importance",
            "Objective",
        ) not in enabled_names_path
        assert ("Main Title", "Methods") in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
        ) in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
        ) in enabled_names_path
        assert (
            "Main Title",
            "Methods",
            "Data Collection",
            "Tools Used",
            "Future Work",
        ) not in enabled_names_path
        assert ("Main Title", "Conclusion") not in enabled_names_path

    def test2_full2part(self):  # input full tree, gen partial tree
        input = self.blueprint2_full
        output = self.blueprint2_significant

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = tree.generate_preview_tree(
            show_full_tree=False, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == output

    def test2_part2part(self):  # input part tree, gen partial tree
        input = self.blueprint2_significant
        output = self.blueprint2_significant

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = tree.generate_preview_tree(
            show_full_tree=False, preview_line_count=0, hide_comment=True
        )

        print(preview_tree)
        assert preview_tree == output

    def test2_full2repr(self):  # test __repr__()
        input = self.blueprint2_full
        output = self.blueprint2_repr

        tree = PromptBlueprint(self.corpus, input)
        preview_tree = repr(tree)

        print(preview_tree)
        assert _remove_last_line(preview_tree) == output
