# Dynamic Node Documentation

**Dynamic nodes** are corpus nodes whose content has no fixed value — it is generated at render time (e.g. today's date, abbreviation lookups from a query). Unlike sidecar nodes, dynamic nodes **are** included in the rendered prompt output by default.

<!-- Fixme require proof reading -->




## Concepts

A dynamic node is an instance of the abstract class `DynamicNode`, itself a subclass of `BasePromptNode`. Every concrete dynamic node type must:

- declare a `HEADING` class attribute (its name, without parentheses)
- be a **leaf node** — attaching children raises `TypeError`
- implement `content_lines(**kwargs)` to produce its rendered content

**Name syntax:** a dynamic node's `.name` is always its `HEADING` wrapped in parentheses, e.g. `(Today)`, `(Abbreviations)`. This is enforced by the constructor, which builds `.name` from `HEADING` automatically — a concrete subclass never sets `.name` directly.

**Preface:** the constructor also accepts a `preface` argument (an iterable of lines, defaulting to empty) stored as `self._preface`. Every concrete `content_lines()` implementation prepends `self._preface` to its generated lines. This lets a dynamic node carry over introductory text written by a corpus author; q.v. "In Prompt Corpus" below for how `preface` gets populated.

**Rendering behavior:** dynamic nodes are attached directly to the prompt corpus tree and behave like any other node during blueprint checkmarking and rendering — no `contains_sidecar_nodes`-style opt-in is required. Compare this to conditional sidecar nodes, which are excluded unless explicitly requested; q.v. [`Sidecar Node Documentation`](sidecar_node_doc.md).

**Kwargs pass-through:** any extra keyword arguments passed to `PromptBlueprint.generate_prompt()` / `.generate_prompt_lines()` are forwarded to every node's `content_lines()`. This is how a dynamic node receives render-time input — e.g. `AbbrNode.content_lines(query=...)` uses `query` to scan for abbreviation occurrences.




## In Prompt Corpus

Dynamic nodes are **not** written in `prompt_corpus.md`. `PromptCorpusNode` explicitly rejects any heading matching the dynamic-node syntax `^\(.+\)$` — that syntax is reserved.

Instead, every registered dynamic node type is attached to the corpus tree **once**, programmatically, right after the corpus file is parsed, via `_attach_dynamic_node()`:

```python
for node_type in DYNAMIC_NODE_TYPES:
    _attach_dynamic_node(prompt_corpus_tree, node_type)
```

This happens inside `load_prompt_corpus_tree()` ([prompt_corpus_loader.py](../kaye/prompt/prompt_corpus_loader.py)) — each dynamic node type becomes a direct child of the tree root.

**Preface carry-over:** `_attach_dynamic_node()` first checks whether a statically-authored `PromptCorpusNode` sharing the dynamic node's heading (e.g. `(Today)`, `(Usable Abbreviations)`) already exists among the root's children. If so, that static node is detached and its `content_lines()` becomes the new dynamic node's `preface` — letting a corpus author write introductory text above dynamically-generated entries instead of it being silently dropped.

**Checkmarking behavior:** a dynamic node behaves like a regular corpus node once attached — it can be checkmarked, uncheckmarked, or included in a full/empty blueprint the same way as any `PromptCorpusNode`. There is no special exclusion rule for dynamic nodes as there is for sidecar nodes.




## Python Package `kaye/prompt/dynamic_nodes`

### `DynamicNode`

Abstract base class for all dynamic node types.

**Location:** [dynamic_node.py](../kaye/prompt/dynamic_nodes/dynamic_node.py)

**Class attributes:**

- `HEADING` (str): the node's name, without parentheses; must be set by every concrete subclass

**Constructor behavior:**

```python
def __init__(self, parent=None, preface=(), **kwargs):
    heading = "(" + self.HEADING + ")"
    super().__init__(heading, parent=parent, **kwargs)

    self._preface = list(preface)
```

`.name` is always derived from `HEADING`; a subclass never passes a heading explicitly. `preface` is stored as `self._preface` for `content_lines()` implementations to prepend.

**Leaf-node enforcement:** `_pre_attach_children()` raises `TypeError` if any children are attached — a dynamic node is always a leaf.

**Copy behavior:** `__copy__()` returns `type(self)(None, preface=self._preface)` — a fresh instance with no parent, carrying the same preface, since dynamic node content is generated on demand rather than stored.


### Registry: `DYNAMIC_NODE_TYPES`

**Location:** [dynamic_nodes/\_\_init\_\_.py](../kaye/prompt/dynamic_nodes/__init__.py)

A tuple of every concrete `DynamicNode` subclass, attached to the corpus tree by `load_prompt_corpus_tree()`. To register a new dynamic node type, add it to this tuple.


### Concrete Dynamic Node Types

**Location:** [today_node.py](../kaye/prompt/dynamic_nodes/today_node.py), [abbr_nodes.py](../kaye/prompt/dynamic_nodes/abbr_nodes.py), [abbr_tag_nodes.py](../kaye/prompt/dynamic_nodes/abbr_tag_nodes.py)

| Class | Heading | Purpose |
| --- | --- | --- |
| `TodayNode` | `(Today)` | current date and time |
| `AbbrNode` | `(Abbreviations)` | abbreviation meanings found in a `query=` string, or every `always_understand`-tagged entry when `query` is empty |
| `UsableAbbrNode` | `(Usable Abbreviations)` | abbreviations tagged `usable_in_brief` |
| `CodingTermsNode` | `(Coding Terms)` | abbreviations tagged `coding` |
| `LanguageCodeNode` | `(Languages Code)` | abbreviations tagged `language_code` |
| `PLCNode` | `(Programming Languages Code)` | abbreviations tagged `programming_language_code` |
| `UnityEngineAbbrNode` | `(Unity Engine Abbreviations)` | abbreviations tagged `unity_engine_abbr` |

#### `TodayNode`

`content_lines()` takes no meaningful arguments; returns two lines: `Date: YYYY-MM-DD` and `Time: HH:MM:SS`, computed from `datetime.now()` at render time.

#### `AbbrNode`

`content_lines(*, query="")` behaves in one of two ways:

- if `query` is given, it scans `query` using `AbbrData().automaton` to find abbreviation occurrences, verifies each match's surrounding characters via `verify_found()`, then renders matches as Markdown list entries
- if `query` is empty, it falls back to every `AbbrData().abbrs` entry tagged `AbbrTags.always_understand`, via the shared `gen_abbrs_content_lines()` helper

#### `gen_abbrs_content_lines(abbr_tag)`

**Location:** [abbr_tag_nodes.py](../kaye/prompt/dynamic_nodes/abbr_tag_nodes.py)

Shared helper that filters `AbbrData().abbrs` by a single `AbbrTags` flag and renders matching entries as Markdown list entries. Backs every tag-filtered node below, and `AbbrNode`'s empty-`query` fallback.

#### `UsableAbbrNode`, `CodingTermsNode`, `LanguageCodeNode`, `PLCNode`, `UnityEngineAbbrNode`

Each is a thin `_AbbrTagNodeBase` subclass declaring a single `ABBR_TAG` (`usable_in_brief`, `coding`, `language_code`, `programming_language_code`, `unity_engine_abbr` respectively); `content_lines()` returns `self._preface + gen_abbrs_content_lines(self.ABBR_TAG)`. Q.v. [`abbrs_json_doc.md`](abbrs_json_doc.md) for the `tags` field these filters key off of.
