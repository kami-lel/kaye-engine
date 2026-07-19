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

Conditional sidecar nodes are real prompt content (e.g., instructions, rules) that are conditionally spliced into the rendered prompt based on explicit requests via the `contains_sidecar_nodes` parameter with matching flags.

#### `{prerequisite}`

Lists prerequisite instructions that apply whenever the parent node is enabled. When a parent node is checkmarked in a blueprint, its `{prerequisite}` sidecar children should typically be auto-included.

**Rendering behavior:** Pass `contains_sidecar_nodes=SidecarNodeType.PREREQUISITE` to `generate_prompt()` or `render.render_prompt_lines()` to auto-checkmark every `{prerequisite}` node whose parent is already checkmarked before rendering.

**Detection:** Use `get_sidecar_node_type(node) & SidecarNodeType.PREREQUISITE` to identify prerequisite sidecars.


#### `{for-claude-code}`

Lists Claude-specific instructions that apply whenever the parent node is enabled. Pass `contains_sidecar_nodes=SidecarNodeType.FOR_CLAUDE_CODE` (or combine with `PREREQUISITE` via `|`) to auto-checkmark these nodes during Claude exports.

**Rendering behavior:** Pass `contains_sidecar_nodes=SidecarNodeType.FOR_CLAUDE_CODE` to auto-include `{for-claude-code}` sidecars during rendering. The constant `kaye.cli.claude.CONTAINING_SIDECAR_NODES` combines both `PREREQUISITE` and `FOR_CLAUDE_CODE` flags for all Claude skill and hook exports.

**Detection:** Use `get_sidecar_node_type(node) & SidecarNodeType.FOR_CLAUDE_CODE` to identify Claude-specific sidecars.




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

## {prerequisite}

This node contains prerequisite instructions.

## {for-claude-code}

This node contains Claude-specific instructions.
```

**Heading conventions:**
- The heading level of a sidecar node (e.g., `##`, `###`) determines its depth in the tree
- A sidecar node must be **one level deeper than its parent node**
- Sidecar nodes are identified by the pattern `^\{.+\}$` (any name in curly braces)
- Unknown sidecar node types (names in `{}` that don't match descriptor or conditional types) are treated as regular nodes

**Checkmarking behavior:**
- Sidecar nodes are **never auto-checkmarked** by `create_full_blueprint()` or by `.checkmark()` with `recursively=True`
- Descriptor sidecars are generally not checkmarked at all — their content is accessed via the `.sidecars` blueprint attribute
- Conditional sidecar nodes can be auto-checkmarked only when you explicitly pass a matching `SidecarNodeType` flag to `generate_prompt()` or `render.render_prompt_lines()`
- To explicitly checkmark a sidecar node: `bp.checkmark(sidecar_node)`




## Python Package `kaye/prompt/sidecar_nodes`

### `get_sidecar_node_type(node)`

Determine the sidecar node type from a node's name.

**Signature:**
```python
def get_sidecar_node_type(node: BasePromptNode) -> SidecarNodeType
```

**Description:**
Identifies the type of a sidecar node by matching its name against known sidecar node type headings (e.g., `{description}`, `{prerequisite}`). Returns `SidecarNodeType.NONE` (which evaluates to `False` in boolean context) if the node is not a recognized sidecar node type.

**Parameters:**
- `node` (BasePromptNode): Node to check (must have a `name` attribute)

**Returns:**
- `SidecarNodeType`: Sidecar node type; `SidecarNodeType.NONE` (0) if not a sidecar node or unknown type

**Examples:**

Check if a node is any sidecar node:
```python
from kaye.prompt.sidecar_nodes import get_sidecar_node_type, SidecarNodeType

node_type = get_sidecar_node_type(node)

if bool(node_type):  # equivalent to: if node_type != NONE
    print(f"sidecar node type: {node_type.name}")
```

Check for specific sidecar type using bitwise operations:
```python
if node_type & SidecarNodeType.PREREQUISITE:
    print("this is a conditional sidecar node")

if node_type & (SidecarNodeType.PREREQUISITE | SidecarNodeType.FOR_CLAUDE_CODE):
    print("this is a conditional sidecar node (either PREREQUISITE or FOR_CLAUDE_CODE)")
```

---

### `SidecarNodeType`

Enumeration of sidecar node types using bitwise flag operations.

**Type:** `IntFlag`

**Members:**

| Name | Value | Category | Description |
| --- | --- | --- | --- |
| `NONE` | 0 | (base) | Not a sidecar node; evaluates to `False` in boolean context |
| `DESCRIPTION` | 1 | Descriptor | Metadata: node description |
| `WHEN_TO_USE` | 2 | Descriptor | Metadata: when to apply node |
| `GLOBS` | 4 | Descriptor | Metadata: file glob patterns |
| `PREREQUISITE` | 8 | Conditional | Real prompt content: prerequisites |
| `FOR_CLAUDE_CODE` | 16 | Conditional | Real prompt content: Claude-specific |

**Properties:**

#### `as_node_heading`

Render this sidecar node type as a corpus node heading.

**Signature:**
```python
@property
def as_node_heading(self) -> str
```

**Returns:**
- `str`: Heading string, e.g., `{description}`

**Raises:**
- `ValueError`: If called on `NONE` or combined flags (only single types are valid)

**Example:**
```python
SidecarNodeType.DESCRIPTION.as_node_heading  # returns "{description}"
SidecarNodeType.PREREQUISITE.as_node_heading  # returns "{prerequisite}"
```

**Usage Notes:**

- **Boolean context:** `NONE` evaluates to `False`; any other type evaluates to `True`
- **Bitwise operations:** Combine multiple types using `|` (OR) operator
  ```python
  combined = SidecarNodeType.PREREQUISITE | SidecarNodeType.FOR_CLAUDE_CODE
  if node_type & combined:
      pass  # matches either type
  ```
- **Categories:**
  - Descriptor sidecars (`DESCRIPTION`, `WHEN_TO_USE`, `GLOBS`): metadata about parent nodes
  - Conditional sidecar nodes (`PREREQUISITE`, `FOR_CLAUDE_CODE`): real prompt content conditionally included

---

### `BlueprintDescriptorSidecars`

Container for descriptor sidecar metadata extracted from a node's descriptor children.

**Location:** `kaye/prompt/sidecar_nodes/blueprint_description_sidecars.py`

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
- `when_to_use` and `globs` combine from both

**Example:**
```python
merged = bp1.sidecars | bp2.sidecars
```

**Usage in PromptBlueprint:**

Access descriptor sidecar metadata:
```python
from kaye.prompt import PromptBlueprint

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
from kaye.prompt.sidecar_nodes import SidecarNodeType

# Include prerequisites
prompt = bp.generate_prompt(
    contains_sidecar_nodes=SidecarNodeType.PREREQUISITE
)

# Include both prerequisites and Claude-specific instructions
prompt = bp.generate_prompt(
    contains_sidecar_nodes=(
        SidecarNodeType.PREREQUISITE | SidecarNodeType.FOR_CLAUDE_CODE
    )
)
```
