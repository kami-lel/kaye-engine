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

----

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

Use `.generate_preview_tree()` to create a tree formatted representation

<!-- fixme improve update details -->

----

`str(node)` is equivalent to ``node.generate_preview_tree()``













### Prompt Blueprint `PromptBlueprint`


A **prompt blueprint** defines a specific subset of the prompt corpus.

The ``PromptBlueprint`` class encapsulates prompt blueprint structure.

The supporting function ``load_embedded_prompt_blueprint(prompt_blueprint_name)``
retrieves and loads a selected *embedded* blueprint stored in
``kaye/gen_prompt/prompt_blueprints/`` at runtime.

<!-- TODO write Python API documentation -->