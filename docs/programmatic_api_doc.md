# Kaye Programmatic API documentation

## `prompt` module

The **core** module of *Kaye Python API*, implement a systematic, dynamic, and structured framework for **prompt management and manipulation**.














### Prompt Tree Nodes `BasePromptNode`

The **prompt tree** is the structured representation parsed from *prompt corpus text* . A **node** of tree is corresponding to a section heading in the text. E.g. text in such form:

```md
# Introduction
~
## Basic
~
## Advanced
~
# Usage

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

nodes types:

- Prompt Corpus Node `PromptCorpusNode`
- dynamic nodes `DynamicNode`

  - Today Node `TodayNode`
  - Abbreviations Node `AbbrNode`
  - Languages Code Node `LanguageCodeNode`
  - Programming Languages Code Node `PLCNode`
  - Usable Abbreviations Node `UsableAbbrNode`
  - Unity Engine Abbreviations Node `UnityEngineAbbrNode`



##### name

Each node has `.name`, i.e. **section heading** which appears in *preview tree* (v.i.):

  - for `DynamicNode` instances: it must be enclosed by `{}`.

E.g.

```python
>>> corpus_node.name
"Introduction"
>>> dynamic_node.name
"{Abbreviations}"
```

> [!NOTE]
> `.name` is a property of `anytree.Node`

----

Use `.is_technical_node` property to check if a node name matches the **technical node** pattern `{name}` (e.g., dynamic nodes):

```python
>>> corpus_node.is_technical_node
False
>>> dynamic_node.is_technical_node
True
```

Technical nodes are special nodes identified by names enclosed in curly braces, such as `{Abbreviations}`, `{Today}`, etc.



##### lineage

Use `.generate_lineage()` to get a linage from root (exclusively) to current node (inclusively,) represented as a ``list`` of node's ``.name``.

> [!TIP]
> Since root is excluded from lineage, tree with different root nodes' names may produce identical lineage.

----

Use `str()` to produce a node's representation that contains the lineage.

E.g.

```python
>>> str(root)
"PromptCorpusNode()"
>>> str(corpus_node)
"PromptCorpusNode(Introduction#Data#Advanced)"
>>> str(abbr_node)
"AbbrNode(Introduction#Data#{Abbreviations})"
```

----

`hash()` of a `BasePromptNode` is also based on `.generate_lineage()`

----

`==` operator of nodes is also based on `.generate_lineage()`.
I.e. `a == b` return whether two nodes has the same lineage.

Additionally, if both nodes are roots, test whether 2 trees are identical in node name structure (node content is irrelevant.)



##### content lines

To access node's textual **content lines**, use `.content_lines()` (typed `list`.)



##### `[]` operator

Use `[]` operator to access child of `node` by:

- index (typed `int`) among all children, or
- child's name (typed `str`)

> [!NOTE]
> When using `str` as key, it will return 1st node that has a name identical to the given value.

> [!TIP]
> Use `.parent` to access node's parent, and `.parent` of a root node is ``None``



##### tree preview

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



##### support `copy`

`BasePromptNode` support Python `copy` operations.

Use `copy.copy(node)` to create a shallow copied identical node, but with no children and no parent (set to `None`)

Use `copy.deepcopy(root)` to copy a prompt tree.





#### tree creation

It is rare for end users to create individual instances, but to **create** an entire prompt tree (i.e. get the root node.) This is possible by load a tree of the **embedded** *prompt corpus text* (defined in `prompt_corpus.md`.) `load_embedded_prompt_corpus()` method will load it from filesystem at runtime:

```python
from kaye.gen_prompt import load_embedded_prompt_corpus

tree_root = load_embedded_prompt_corpus()
```













### Prompt Blueprint `PromptBlueprint`

A **prompt blueprint** represents a configurable subset of *prompt corpus tree*, such that individual node are either **checkmarked** (i.e. enabled, turned on) or **uncheckmarked** (i.e. disabled, turned off.) Then one can generate a prompt as a subset of the tree.

----

User always create a populated `PromptBlueprint` by **parsing** a blueprint text (as positional argument `blueprint_text`) by using *classmethod* `.parse()`, e.g.

```python
prompt_corpus = ~
blueprint_text = ~
blueprint = PromptBlueprint.parse(blueprint_text)
```

By default, this parse the blueprint text based on the *embedded prompt corpus text*. One might use an alternative corpus tree by providing keyword argument `corpus_override`, but this is often only used for testing purpose.

----

Additionally, one might create full/empty blueprints by *classmethod*:

- ``PromptBlueprint.create_full_blueprint()``, and
- ``PromptBlueprint.create_empty_blueprint()``

These return blueprint objects those contain all nodes (of corpus tree), and also checkmark/uncheckmark all nodes.

----

`PromptBlueprint` is a data structured based on Python `dict`.

A `PromptBlueprint` has 3 additional attributes:

- `.corpus`: corresponding prompt corpus tree root (typed `BasePromptNode`)
- `.display_name`: name of the blueprint, typed `str`, default to `''`
- `.description`: short description of the blueprint's purpose, typed `str`, default to `''`

Each entry in `PromptBlueprint` represents a node, with key being node `hash()` (typed `int`,) and value being if the node is *checkmarked*, (typed `bool`.) The *root node* is never included in blueprint, because one will assume root node is always enabled/checkmarked.



#### per node operations

There are 2 types of relationships of a prompt corpus **node** and a **blueprint**:

- if a node is **contained**/included as part of the blueprint
- if a node is **checkmarked**/enabled in the blueprint

| check by node' | contains/inclusion | is checkmarked |
| ---- | ---- | ---- |
| hash | `h in bp`, `h in bp.keys()` | `bp.is_checkmarked(h)`, `bp[h]` |
| object | `node in bp` | `bp.is_checkmarked(node)` |
| name | `name in bp` | `bp.is_checkmarked(name)` |

(`h`: hash value, `node`: node object, `bp`: blueprint)



##### checkmarking & uncheckmarking

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

`.checkmark()` and `.uncheckmark()` support keyword argument `recursively=` which allows user to (un)checkmark a node and all of its descendants.

----

Both operations allows user to provide node as node object, hash value, name.

E.g.

```python
bp.checkmark(bp.corpus[0][1])
bp.checkmark(node_hash)
bp.uncheckmark("Important Instruction")
bp.uncheckmark("{Abbreviations}")
```

However, when encounter a node findable in corpus tree, but not contained in the blueprint:

- `.checkmark()` will automatically contain the node, and then mark it checkmarked
- `.uncheckmark()` will raise a `KeyError`



#### blueprint-level operations

##### prune

Use `bp.prune()` will create a minimum version that contains only branches with checkmarked nodes.


##### merge

Use `.merge()` function to merge 2 blueprints as the union of checkmarked nodes of 2 blueprints.

Operator `|` perform identical function.

E.g.

```python
bp_left.merge(bp_right)  # or, identically
bp_left | bp_right
```


##### generate prompt

Use `.generate_prompt()` to render the **concrete prompt** that can be used as LLM system message with it content based on node's checkmarking status of this blueprint.

E.g.

```python
>>> tree = PromptBlueprint(~)
>>> tree.generate_prompt(hide_comment=True)
# Main Title
Overview of the methodologies used.
### Data Collection
How data was gathered for analysis.
## Conclusion
Summarizing the findings and implications.
```



##### generate blueprint text

User may use `.generate_blueprint()` to show a human-readable presentation of `PromptBlueprint`; the tree contains:

- tree structure of corresponding *prompt corpus tree*
- node name, i.e. section heading
- node content preview
- **checkmark status** of the node, shown with either `[x]` or `[ ]` as prefix

By default, this print an **pruned** tree, showing only branches & nodes relevant to this blueprint. By using keyword argument `show_full_tree=`, user may force it to show the full prompt corpus tree.

E.g.

```python
>>> tree = PromptBlueprint.parse(~)
>>> tree.generate_blueprint()
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
>>> tree.generate_blueprint(content_preview_lines=0, hide_comment=True)
    ○
[x] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[ ]     ├── Contributing
[x]     └── License
```

----

`repr(blueprint)` is equivalent to `blueprint.generate_blueprint()`




#### embedded blueprints

**Embedded blueprints** are defined as module-level variables in `kaye.prompt.embedded_blueprints`. Import them directly by name:

```python
from kaye.prompt.embedded_blueprints import (
    chat_blueprint,
    coder_py_blueprint,
    coder_changelog_blueprint,
)
```

All available blueprint names are listed in `__all__` of that module. Each blueprint is a `PromptBlueprint` instance with `.display_name` and `.description` already set.
