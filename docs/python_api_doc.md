# Kaye Python API documentation

## `gen_prompt` module

The **core** module of *Kaye Python API*, implement a systematic, dynamic, and structured framework for **prompt management and manipulation**.













### Prompt Node `PromptCorpusNode`

A `PromptCorpusNode` encapsule a single node in the *prompt corpus tree*.

The **prompt corpus tree** is the structured representation parsed from *prompt corpus text* . A **node** of tree is corresponding to a section heading in the text. E.g. text in such form:

```md
# Introduction
~~~
## Basic
~~~
## Advanced
~~~
# Usage
~~~
```

is equivalent to tree structure:

```
○
├── Introduction
│   ├── Basic
│   └── Advanced
└── Usage
```

A *node* represent a branch of the tree. If the node is *root*, it represents an instance of entire prompt corpus tree.

The class `PromptCorpusNode` is a subclass of `anytree.Node`, q.v. [anytree Documentation](https://anytree.readthedocs.io/en/stable/)





#### tree creation

When deal with `PromptCorpusNode`, it is rare for end users to create individual instances, but to **create** an entire prompt corpus tree (i.e. get the root node.) This is possible by *classmethod* `.parse()`:

```python
from kaye.gen_prompt import PromptCorpusNode

text = ~~~
tree_root = PromptCorpusNode.parse(text)
```

Or to directly load a tree of the **embedded** *prompt corpus text* (defined in `prompt_corpus.md`.) `load_embedded_prompt_corpus()` method will load it from filesystem at runtime:

```python
from kaye.gen_prompt import load_embedded_prompt_corpus

tree_root = load_embedded_prompt_corpus()
```





#### node properties

###### name

To access node **name**, i.e. **section heading**:

```python
node = ~~~
assert node.name == "Introduction"
```

###### parent

To access node **parent**:

```python
node.parent  # or
node[None]
```

The `.parent` of a root node is ``None``

###### content

To access node's textual **content lines**, use `.content` (typed `list`.) E.g. with prompt corpus text:

```python
prompt_corpus_text = """
# Introduction
~~~
## Basic
Hi, my name is Alice.
It is nice to see you.

What is your name?

## Advanced
~~~
"""

introduction_basic_node = ~~~
introduction_basic_node.content == [
    "Hi, my name is Alice.",
    "It is nice to see you.",
    "",
    "What is your name?",
]
```




#### node inspection

###### path of names

The node store a **path of names**, describing a path from root to this node, with node's ancestors and the parent in between.

E.g. consider this tree:

```
○
├── Introduction
│   ├── Basic
│   └── Advanced
│       └── Additional Info
└── Usage
```

`.path_of_names` store such path as a `tuple` of `str`.

```python
assert root_node.path_of_names == tuple()  # empty
assert intro_node.path_of_names == "Introduction"
assert basic_node.path_of_names == ("Introduction", "Basic")
assert add_node.path_of_names == (
    "Introduction",
    "Advanced",
    "Additional Info",
)
```

----

Use `repr(node)` also yield similar result:

```python
assert repr(root_node) == "PromptCorpusNode()"
assert repr(intro_node) == "PromptCorpusNode(Introduction)"
assert repr(basic_node) == "PromptCorpusNode(Introduction#Basic)"
assert (
    repr(add_note)
    == "PromptCorpusNode("
    "Introduction#Advanced#Additional Info)"
)
```





###### preview tree

Use `.generate_preview_tree()` to show a human-readable representation which shows:

- tree structure
- node name, i.e. section heading
- node content preview

E.g.

```python
>>> tree.generate_preview_tree()
○
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
        This project is licensed under the MIT License.
```

As shown above, it contains *content preview*, which can be customized by arguments `preview_line_count` and `preview_line_width`, e.g.

```python
>>> tree.generate_preview_tree(preview_line_count=0)
○
└── Project Title
    ├── Description
    ├── Installation
    ├── Usage
    ├── Contributing
    └── License
```

----

`str(node)` is equivalent to ``node.generate_preview_tree()``













### Prompt Blueprint `PromptBlueprint`

A **prompt blueprint** represents a configurable subset of *prompt corpus tree*, such that individual node are either **checkmarked** (i.e. enabled, turned on) or **uncheckmarked** (i.e. disabled, turned off.) Then one can generate a prompt as a subset of the tree.

----

One might **create** a populated `PromptBlueprint` by **parsing** a preview-tree text (v.i.) by using *classmethod* `.parse()`, e.g.

```python
prompt_corpus = ~~~
blueprint_text = ~~~
blueprint = Blueprint.parse(prompt_corpus, blueprint_text)
```

Additionally, one might create full/empty blueprints by *classmethods*:

- ``Blueprint.create_full_blueprint()``, and
- ``Blueprint.create_empty_blueprint()``

----

`PromptBlueprint` is a data structured based on Python `dict`.

A `PromptBlueprint` has 2 additional attributes:

- `.corpus`: corresponding prompt corpus tree root (typed `PromptCorpusNode`)
- `.display_name`: name of the blueprint, typed `str`, default to `''`

Each entry in `PromptBlueprint` represents a node, with key being node `hash()` (typed `int`,) and value being if the node is *checkmarked*, (typed `bool`.)





#### generate prompt

Use `.generate_prompt()` (or `str()`) to render
a **concrete prompt** composed of all enabled nodes

```python
>>> tree = PromptBlueprint(...)
>>> tree.generate_prompt(hide_comment=True)
# Main Title
Overview of the methodologies used.
### Data Collection
How data was gathered for analysis.
## Conclusion
Summarizing the findings and implications.
```

<!-- TODO write Python API documentation -->




#### preview tree

Like `PromptCorpusNode`, one may use `.generate_preview_tree()` to show a human-readable presentation of `PromptBlueprint`; the tree contains:

- tree structure of corresponding *prompt corpus tree*
- node name, i.e. section heading
- node content preview
- **checkmark status** of the node, shown with either `[x]` or `[ ]` as prefix

By default, this print an **pruned** tree, showing only branches & nodes relevant to this blueprint. By using keyword argument `show_full_tree=`, user may force it to show the full prompt corpus tree.

E.g.

```python
>>> tree = PromptBlueprint(~~~)
>>> tree.generate_preview_tree()
    ○
[x] └── Project Title
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
[x]     └── License
            This project is licensed under the MIT License.
(blueprint:conversation; Kaye v1.2.3)
>>> tree.generate_preview_tree(preview_line_count=0, hide_comment=True)
    ○
[x] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[ ]     ├── Contributing
[x]     └── License
```

----

`str(blueprint)` is equivalent to `blueprint.generate_preview_tree()`




#### embedded blueprints

The supporting function ``load_embedded_prompt_blueprint(prompt_blueprint_name)``
retrieves and loads a selected *embedded* blueprint stored in
``kaye/gen_prompt/prompt_blueprints/`` at runtime.

<!-- TODO write Python API documentation -->