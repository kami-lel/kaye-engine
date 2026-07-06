# Dynamic Node Documentation

**Dynamic nodes** are corpus nodes whose content has no fixed value — it is generated at render time (e.g. today's date, abbreviation lookups from a query). Unlike sidecar nodes, dynamic nodes **are** included in the rendered prompt output by default.




## Concepts

A dynamic node is an instance of the abstract class `DynamicNode`, itself a subclass of `BasePromptNode`. Every concrete dynamic node type must:

- declare a `HEADING` class attribute (its name, without parentheses)
- be a **leaf node** — attaching children raises `TypeError`
- implement `content_lines(**kwargs)` to produce its rendered content

**Name syntax:** a dynamic node's `.name` is always its `HEADING` wrapped in parentheses, e.g. `(Today)`, `(Abbreviations)`. This is enforced by the constructor, which builds `.name` from `HEADING` automatically — a concrete subclass never sets `.name` directly.

**Rendering behavior:** dynamic nodes are attached directly to the prompt corpus tree and behave like any other node during blueprint checkmarking and rendering — no `contains_sidecar_nodes`-style opt-in is required. Compare this to conditional sidecar nodes, which are excluded unless explicitly requested; q.v. [`Sidecar Node Documentation`](sidecar_node_doc.md).

**Kwargs pass-through:** any extra keyword arguments passed to `PromptBlueprint.generate_prompt()` / `.generate_prompt_lines()` are forwarded to every node's `content_lines()`. This is how a dynamic node receives render-time input — e.g. `AbbrNode.content_lines(query=...)` uses `query` to scan for abbreviation occurrences.




## In Prompt Corpus

Dynamic nodes are **not** written in `prompt_corpus.md`. `PromptCorpusNode` explicitly rejects any heading matching the dynamic-node syntax `^\(.+\)$` — that syntax is reserved.

Instead, every registered dynamic node type is attached to the corpus tree **once**, programmatically, right after the corpus file is parsed:

```python
for node_type in DYNAMIC_NODE_TYPES:
    node_type(prompt_corpus_tree)
```

This happens inside `load_prompt_corpus_tree()` ([prompt_corpus_loader.py](../kaye/prompt/prompt_corpus_loader.py)) — each dynamic node type becomes a direct child of the tree root.

**Checkmarking behavior:** a dynamic node behaves like a regular corpus node once attached — it can be checkmarked, uncheckmarked, or included in a full/empty blueprint the same way as any `PromptCorpusNode`. There is no special exclusion rule for dynamic nodes as there is for sidecar nodes.




## Python Package `kaye/prompt/dynamic_nodes`

### `DynamicNode`

Abstract base class for all dynamic node types.

**Location:** [dynamic_node.py](../kaye/prompt/dynamic_nodes/dynamic_node.py)

**Class attributes:**

- `HEADING` (str): the node's name, without parentheses; must be set by every concrete subclass
- `_ID_PATTERN`: compiled regex `^\(.+\)$` used to recognize dynamic-node heading syntax

**Classmethods:**

#### `is_valid_dynamic_node_heading(heading)`

**Signature:**
```python
@classmethod
def is_valid_dynamic_node_heading(cls, heading: str) -> bool
```

Returns whether `heading` matches dynamic-node syntax (wrapped in parentheses). Used by `PromptCorpusNode.__init__()` to reject illegal headings when parsing corpus text.

**Constructor behavior:**

```python
def __init__(self, parent=None, **kwargs):
    heading = "(" + self.HEADING + ")"
    super().__init__(heading, parent=parent, **kwargs)
```

`.name` is always derived from `HEADING`; a subclass never passes a heading explicitly.

**Leaf-node enforcement:** `_pre_attach_children()` raises `TypeError` if any children are attached — a dynamic node is always a leaf.

**Copy behavior:** `__copy__()` returns `type(self)(None)` — a fresh instance with no parent, since dynamic node content is generated on demand rather than stored.


### Registry: `DYNAMIC_NODE_TYPES`

**Location:** [dynamic_nodes/\_\_init\_\_.py](../kaye/prompt/dynamic_nodes/__init__.py)

A tuple of every concrete `DynamicNode` subclass, attached to the corpus tree by `load_prompt_corpus_tree()`. To register a new dynamic node type, add it to this tuple.


### Concrete Dynamic Node Types

**Location:** [today_node.py](../kaye/prompt/dynamic_nodes/today_node.py), [abbr_nodes.py](../kaye/prompt/dynamic_nodes/abbr_nodes.py)

| Class | Heading | Purpose |
| --- | --- | --- |
| `TodayNode` | `(Today)` | current date and time |
| `AbbrNode` | `(Abbreviations)` | abbreviation meanings found in a `query=` string |
| `UsableAbbrNode` | `(Usable Abbreviations)` | abbreviations tagged `usable` |
| `LanguageCodeNode` | `(Languages Code)` | abbreviations tagged `language_code` |
| `PLCNode` | `(Programming Languages Code)` | abbreviations tagged `programming_language_code` |
| `UnityEngineAbbrNode` | `(Unity Engine Abbreviations)` | abbreviations tagged `unity_engine_abbr` |

#### `TodayNode`

`content_lines()` takes no meaningful arguments; returns two lines: `Today: YYYY-MM-DD` and `Time: HH:MM:SS`, computed from `datetime.now()` at render time.

#### `AbbrNode`

`content_lines(*, query="")` scans `query` using `AbbrData().automaton` to find abbreviation occurrences, verifies each match's surrounding characters via `verify_found()`, then renders matches as Markdown list entries.

#### `UsableAbbrNode`, `LanguageCodeNode`, `PLCNode`, `UnityEngineAbbrNode`

Each filters `AbbrData().abbrs` by a single `AbbrTags` flag (`usable`, `language_code`, `programming_language_code`, `unity_engine_abbr` respectively) and renders matching entries as Markdown list entries. Q.v. [`abbrs_json_doc.md`](abbrs_json_doc.md) for the `tags` field these filters key off of.
