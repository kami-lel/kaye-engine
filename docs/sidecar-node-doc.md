# Sidecar Node Documentation

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

**Behavior:** Returns both fields concatenated with appropriate separators.

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
from kaye_engine.cli.claude import CLAUDE_CODE_SIDECARS

# Include Claude Code tool instructions
prompt = bp.generate_prompt(contains_sidecars=CLAUDE_CODE_SIDECARS)
```
