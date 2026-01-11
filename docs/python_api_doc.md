# Kaye Python API documentation

## `gen_prompt` module

The **core** module of *Kaye Python API*, implement a systematic, dynamic, and structured framework for **prompt management and manipulation**.













### Prompt Node `PromptCorpusNode`

A `PromptCorpusNode` encapsule a single node in the *prompt corpus tree*.

The **prompt corpus tree** is the structured representation parsed from *prompt corpus text* . A **node** of tree is corresponding to a section heading in the text. E.g. text in such form:

```md
## Introduction
~
### Basic
~
### Advanced
~
## Usage
~
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





#### node operation





#### node inspection













### Prompt Blueprint `PromptBlueprint`


A **prompt blueprint** defines a specific subset of the prompt corpus.

The ``PromptBlueprint`` class encapsulates prompt blueprint structure.

The supporting function ``load_embedded_prompt_blueprint(prompt_blueprint_name)``
retrieves and loads a selected *embedded* blueprint stored in
``kaye/gen_prompt/prompt_blueprints/`` at runtime.

<!-- TODO write Python API documentation -->