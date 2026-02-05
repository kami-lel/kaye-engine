# Kaye Python API documentation

## `gen_prompt` module

The **core** module of *Kaye Python API*, implement a systematic, dynamic, and structured framework for **prompt management and manipulation**.

----

The **prompt tree** is the structured representation parsed from *prompt corpus text* . A **node** of tree is corresponding to a section heading in the text. E.g. text in such form:

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

A *node* in prompt tree is an instance of abstract class ``BasePromptNode``, which is a subclass of `anytree.Node`, q.v. [anytree Documentation](https://anytree.readthedocs.io/en/stable/)















### Prompt Corpus Node `PromptCorpusNode`

#### tree creation

When deal with `PromptCorpusNode`, it is rare for end users to create individual instances, but to **create** an entire prompt tree (i.e. get the root node.) This is possible by *classmethod* `.parse()`:

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
assert node.id == "Introduction"
```

> [!NOTE]
> `.name` and `.id` return identical result for `PromptCorpusNode`


###### parent

To access node **parent**:

```python
node.parent  # or
node[None]
```

The `.parent` of a root node is ``None``

###### content

To access node's textual **content lines**, use `.content_lines` (typed `list`.) E.g. with prompt corpus text:

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
introduction_basic_node.content_lines == [
    "Hi, my name is Alice.",
    "It is nice to see you.",
    "",
    "What is your name?",
]
```




#### tree preview

Use `.generate_prompt_tree_preview()` on **root** instance to show a human-readable representation which shows:

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

As shown above, it contains *content preview*, which can be customized by arguments `content_preview_lines` and `content_preview_width`, e.g.

```python
>>> tree.generate_preview_tree(content_preview_lines=0)
○
└── Project Title
    ├── Description
    ├── Installation
    ├── Usage
    ├── Contributing
    └── License
```

----

`repr(node)` is equivalent to ``node.generate_preview_tree()``













### Abbreviation Node

<!-- TODO -->













### Prompt Blueprint `PromptBlueprint`

A **prompt blueprint** represents a configurable subset of *prompt corpus tree*, such that individual node are either **checkmarked** (i.e. enabled, turned on) or **uncheckmarked** (i.e. disabled, turned off.) Then one can generate a prompt as a subset of the tree.

----

One might **create** a populated `PromptBlueprint` by **parsing** a preview-tree text (v.i.) (positional argument `blueprint_text`) by using *classmethod* `.parse()`, e.g.

```python
prompt_corpus = ~~~
blueprint_text = ~~~
blueprint = PromptBlueprint.parse(prompt_corpus, blueprint_text)
```

Additionally, one might create full/empty blueprints by *classmethod*:

- ``Blueprint.create_full_blueprint()``, and
- ``Blueprint.create_empty_blueprint()``

----

`PromptBlueprint` is a data structured based on Python `dict`.

A `PromptBlueprint` has 2 additional attributes:

- `.corpus`: corresponding prompt corpus tree root (typed `PromptCorpusNode`)
- `.display_name`: name of the blueprint, typed `str`, default to `''`

Each entry in `PromptBlueprint` represents a node, with key being node `hash()` (typed `int`,) and value being if the node is *checkmarked*, (typed `bool`.) The *root node* is never included in blueprint, because one will assume root node is always enabled/checkmarked.





#### node membership

There are 2 types of relationships of a prompt corpus **node** and a **blueprint**:

- if a node is **contained**/included as part of the blueprint
- if a node is **checkmarked**/enabled in the blueprint

| check for: | contains/inclusion | is checkmarked |
| ---- | ---- | ---- |
| by node hash | `h in bp`, `h in bp.keys()` | `bp.is_checkmarked(h)`, `bp[h]` |
| by node object | `node in bp` | `bp.is_checkmarked(node)` |

(`h`: hash value, `node`: node object, `bp`: blueprint)





#### checkmarking & uncheckmarking

One might **checkmark** a node in a blueprint, and such node must be from blueprint's corpus tree:

```python
blueprint.checkmark(node)
blueprint += node  # identical
```

And one might **uncheckmark** a node already in the blueprint:

```python
blueprint.uncheckmark(node)
blueprint -= node  # identical
```




#### merging

Merge 2 blueprints (of the same corpus tree,) such that:

- contains all nodes from both blueprints
- node is checkmarked: they are checkmarked in either blueprint

```python
left_bp = ~~~
right_bp = ~~~

merged_bp = left_bp.merge(right_bp)  # or identically
left_bp *= right_bp
```






#### generate prompt

Use `.generate_prompt()` to render the **concrete prompt** that can be used as LLM system message with it content based on node's checkmarking status of this blueprint.

E.g.

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
>>> tree.generate_preview_tree(content_preview_lines=0, hide_comment=True)
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

**Embedded blueprints** are saved under `./kaye/kaye/gen_prompt/embedded_blueprints`. Programmatically, one might use these functions to load them from filesystem:

```python
from kaye.gen_prompt import (
    load_embedded_prompt_blueprint,
    load_empty_prompt_blueprint,
    load_full_prompt_blueprint,
)


empty_blueprint = load_embedded_prompt_blueprint()
full_blueprint = load_full_prompt_blueprint()
chat_blueprint = load_embedded_prompt_blueprint("chat")
```