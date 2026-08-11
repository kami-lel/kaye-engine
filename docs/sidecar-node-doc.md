# Kaye Engine: Sidecar Node Documentation

**Sidecar nodes** are corpus nodes with names enclosed in curly braces, e.g. `{description}`, `{when_to_use}`. They are attached to parent nodes in the prompt tree and hold structured metadata or conditional content about their parent. Sidecar nodes appear in the blueprint preview tree but are **not** included in the rendered prompt output by default.


































## Concepts

Sidecar nodes enable two complementary patterns:













### Descriptor Sidecars

Descriptor sidecars are metadata fields that describe a parent node's purpose, relevance, and applicable contexts. They are consumed by blueprints and exposed via `.sidecars` (a `BlueprintDescriptorSidecars` instance).





#### `{description}`

Describes the parent node's functionality — what the node represents or what it instructs. Used in blueprint discovery and documentation generation.

**Rendering behavior:** The description is **overridable** — if explicitly set on the blueprint object, it is used; otherwise, it falls back to the `{description}` node's content.

**Access:** `blueprint.sidecars.description`





#### `{when_to_use}`

Indicates when the parent node should be enabled — the conditions or contexts that make the node relevant. Used for filtering nodes in blueprint UIs and documentation.

**Rendering behavior:** `when_to_use` is **always rendered from the sidecar node content**, never overridden.

**Access:** `blueprint.sidecars.when_to_use`





#### `{globs}`

Lists file glob patterns indicating which file types or paths make the parent node relevant. Each line is treated as a separate pattern — multiple patterns are supported. Used by IDE integrations and code editors to determine when to apply the prompt context.

**Rendering behavior:** `globs` requires **fence-block parsing** (e.g., code blocks with ` ```glob ` delimiters). The patterns are extracted and stored in `blueprint.sidecars.globs`.

**Access:** `blueprint.sidecars.globs` (returns list of glob patterns)













### Conditional Sidecar Nodes

Conditional sidecar nodes are real prompt content (e.g., instructions, rules) that are conditionally spliced into the rendered prompt based on explicit requests via the `contains_sidecars` parameter, a plain collection of sidecar names. Unlike descriptor sidecars, there is no fixed set of conditional names — any `{name}` heading can be requested this way, including reserved descriptor names.

**Rendering behavior:** Pass `contains_sidecars=(...)` to auto-include sidecars of the given name(s) during rendering.

Q.v. [`claude-doc.md`](claude-doc.md) for the list of `{Claude Tool:...}` sidecars, which Claude export surface includes each of these, and the underlying API.






#### `{explicit}`

A persona-intensifier sidecar supplementing a personality node; not tool-specific and currently has no code consumer (no `CLAUDE_*_SIDECARS` constant references it yet).



#### Affordance Sidecars (Usage / Lack)

A second, independent auto-checkmark mechanism for a common case: acknowledging whether a platform capability is available at all, rather than splicing in arbitrary named content.

A consumer registers each capability once, engine-level and platform-agnostic, via `register_affordance(canonical_name, display_name, remark="")` (`kaye_engine/prompt/affordance_registry.py`) — this has nothing to do with Claude, Chat, Cowork, Code, or VSC specifically; any consumer project can register any capability under any name. A corpus author then pairs a `{canonical_name Usage}` / `{canonical_name Lack}` sidecar under a checkmarked node, describing respectively what to do when the capability is present or absent.

**Rendering behavior:** pass `affordances=(...)` to `generate_prompt()` / `render_prompt_lines()` — a plain collection of canonical names. For every entry in `affordance_registry`, its `Usage` sidecar is checkmarked if the entry's `canonical_name` is in `affordances`, else its `Lack` sidecar is checkmarked; either way, only if the sidecar's parent is already checkmarked. This pass is independent of `contains_sidecars` — both may apply to the same render. `affordances=None` (the default) disables the pass entirely; `affordances=()` enables it with every affordance treated as unavailable (every registered `Lack` sidecar wins).

How a consumer's own CLI determines what to pass as `affordances` for a given invocation is entirely up to that consumer — the engine has no concept of "surface" or "which affordances apply where."

Q.v. [`claude-doc.md`](claude-doc.md) for how kaye-vault, a consumer project, uses this mechanism for Claude platform tools specifically.


## In Prompt Corpus

Sidecar nodes follow the standard Markdown heading format in `prompt_corpus.md`:

```markdown
# Parent Node

Content of parent node.

## {description}

This node describes the parent.

## {when_to_use}

This node indicates when to use the parent.

## {globs}

```glob
**/*.py
```

## {Claude Tool:TodoWrite}

This node contains TodoWrite-specific instructions.
```

**Heading conventions:**
- The heading level of a sidecar node (e.g., `##`, `###`) determines its depth in the tree
- A sidecar node must be **one level deeper than its parent node**
- Sidecar nodes are identified by the pattern `^\{.+\}$` (any name in curly braces) — there is no fixed vocabulary; any name is a valid sidecar
- `description`, `when_to_use`, and `globs` are reserved names consumed as metadata by `BlueprintDescriptorSidecars`; every other name is available for conditional content inclusion

**Checkmarking behavior:**
- Sidecar nodes are **never auto-checkmarked** by `create_full_blueprint()` or by `.checkmark()` with `recursively=True`
- Descriptor sidecars are generally not checkmarked at all — their content is accessed via the `.sidecars` blueprint attribute
- Conditional sidecar nodes can be auto-checkmarked only when you explicitly pass their name in the `contains_sidecars` collection to `generate_prompt()` or `render.render_prompt_lines()`
- To explicitly checkmark a sidecar node: `bp.checkmark(sidecar_node)`




## Python Module `kaye_engine/prompt/sidecar_node.py`

### `get_sidecar_name(node)`

Determine a node's sidecar name from its heading.

**Signature:**
```python
def get_sidecar_name(node: BasePromptNode) -> str | None
```

**Description:**
Identifies a sidecar node by its `{name}` heading convention and returns the name inside the braces (e.g., `description`, `globs`). Returns `None` if the node is not a sidecar node. There is no fixed vocabulary — any `{name}` heading is a valid sidecar name.

**Parameters:**
- `node` (BasePromptNode): Node to check (must have a `name` attribute)

**Returns:**
- `str | None`: The sidecar name, or `None` if not a sidecar node

**Examples:**

Check if a node is any sidecar node:
```python
from kaye_engine.prompt.sidecar_node import get_sidecar_name

name = get_sidecar_name(node)

if name is not None:
    print(f"sidecar name: {name}")
```

Check for specific sidecar names:
```python
if name == "Claude Tool:TodoWrite":
    print("this is a conditional sidecar node")
```

---

### `BlueprintDescriptorSidecars`

Container for descriptor sidecar metadata extracted from a node's descriptor children.

**Location:** `kaye_engine/prompt/sidecar_node.py`

**Description:**
Represents the structured metadata (description, when_to_use, globs) derived from a node's sidecar children. These are accessed via `blueprint.sidecars` and never rendered to the prompt output — they exist purely for discovery, documentation, and conditional inclusion logic.

**Attributes:**

#### `description`

The description metadata from the node's `{description}` sidecar child.

**Type:** `str`

**Behavior:** Overridable via setter. If explicitly set, that value is used; otherwise, content from the `{description}` sidecar node is used as fallback.

**Example:**
```python
blueprint.sidecars.description = "Custom description"
print(blueprint.sidecars.description)  # "Custom description"
```

#### `when_to_use`

The when_to_use metadata from the node's `{when_to_use}` sidecar child.

**Type:** `str`

**Behavior:** Always rendered from the sidecar node content; cannot be overridden.

**Example:**
```python
print(blueprint.sidecars.when_to_use)  # content of {when_to_use} node
```

#### `globs`

The file glob patterns from the node's `{globs}` sidecar child.

**Type:** `list[str]`

**Behavior:** Extracted via fence-block parsing (e.g., ` ```glob ` code blocks). Each line becomes a separate pattern.

**Example:**
```python
patterns = blueprint.sidecars.globs
# e.g., ["**/*.py", "**/*.pyi"]
```

#### `description_and_when_to_use`

Derived property combining both description and when_to_use fields.

**Type:** `str`

**Behavior:** When the description is not overridden, returns the
description and when-to-use node content concatenated with appropriate
separators. When the description *is* explicitly overridden, returns
that override alone — the when-to-use content is not appended in that
case.

**Example:**
```python
combined = blueprint.sidecars.description_and_when_to_use
```

**Methods:**

#### `__or__(other)`

Merge two `BlueprintDescriptorSidecars` instances using the `|` operator.

**Signature:**
```python
def __or__(self, other: BlueprintDescriptorSidecars) -> BlueprintDescriptorSidecars
```

**Behavior:**
- Creates a new instance merging metadata from both operands
- `description` takes from self if set, otherwise from other
- `when_to_use` and `globs` take from self if set, otherwise from other

**Example:**
```python
merged = bp1.sidecars | bp2.sidecars
```

**Usage in PromptBlueprint:**

Access descriptor sidecar metadata:
```python
from kaye_engine.prompt import PromptBlueprint

bp = PromptBlueprint.parse(blueprint_text)

# Access descriptor sidecars
print(bp.sidecars.description)
print(bp.sidecars.when_to_use)
print(bp.sidecars.globs)

# Use combined field
print(bp.sidecars.description_and_when_to_use)
```

Merge blueprints:
```python
merged_bp = bp1 | bp2
# merged_bp.sidecars combines metadata from both
```

Conditional rendering with conditional sidecar nodes:
```python
# Include arbitrary named sidecar content
prompt = bp.generate_prompt(contains_sidecars=("Claude Tool:TodoWrite",))
```

Conditional rendering with affordance sidecars:
```python
# Usage/Lack checkmarking for every registered affordance
prompt = bp.generate_prompt(affordances=("Claude Tool:TodoWrite",))
```

---

## Python Module `kaye_engine/prompt/affordance_registry.py`

### `Affordance`

A single registered platform capability, and the two sidecar names derived from its `canonical_name`.

**Fields:**
- `canonical_name` (str): unique identifier for this affordance; also the shared root of its `Usage`/`Lack` sidecar names, and the string an `affordances=(...)` collection names to mark it available
- `display_name` (str): human-readable name, used in generated documentation
- `remark` (str, optional): one-line description of what this affordance does

**Properties:**
- `usage_sidecar_name` → `"{canonical_name} Usage"`
- `lack_sidecar_name` → `"{canonical_name} Lack"`

### `register_affordance(canonical_name, display_name, remark="")`

Construct an `Affordance` and insert it into `affordance_registry` under its `canonical_name`.

**Raises:** `ValueError` if `canonical_name` is already registered.

**Example:**
```python
from kaye_engine.prompt.affordance_registry import register_affordance

register_affordance(
    "Claude Tool:TodoWrite", "TodoWrite",
    remark="maintains a task/todo list for the session",
)
```

### `get_affordance(canonical_name)`

**Raises:** `KeyError` if no affordance is registered under `canonical_name`.

**Returns:** the registry entry stored under `canonical_name`.

### `affordance_registry`

Module-level `dict[str, Affordance]` — every affordance registered so far, keyed by `canonical_name`.
