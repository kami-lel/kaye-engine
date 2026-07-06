# Sidecar Node Documentation

**Sidecar nodes** are corpus nodes with names enclosed in curly braces, e.g. `{description}`, `{when_to_use}`. They are attached to parent nodes in the prompt tree and hold structured metadata or conditional content about their parent. Sidecar nodes appear in the blueprint preview tree but are **not** included in the rendered prompt output by default.

## Overview

Sidecar nodes enable two complementary patterns:

1. **Descriptor Sidecars**: structured metadata fields (`{description}`, `{when_to_use}`, `{globs}`) that describe a node's purpose, relevance conditions, and applicable file patterns — used for blueprint discovery and skill documentation generation.

2. **Conditional Sidecar Nodes** (`{prerequisite}`, `{for_claude}`): real prompt content conditionally spliced into rendered output only when explicitly requested via the `contains_sidecar_nodes` parameter with matching `SidecarNodeType` flags.

## Identification

A sidecar node is identified by a **name enclosed in curly braces**. The pattern is:

```regex
^\{.+\}$
```

Example sidecar node names:

- `{description}`
- `{when_to_use}`
- `{globs}`
- `{prerequisite}`
- `{for_claude}`

Use the function `is_sidecar_node(node)` from `kaye.prompt.sidecar_nodes` to check if a node is a sidecar node.


## Sidecar Node Types

Five sidecar node types are defined. They are categorized into two groups:


### Descriptor Sidecars

Descriptor sidecars are metadata fields that describe a parent node's purpose, relevance, and applicable contexts. They are consumed by blueprints and exposed via `.sidecars` (a `BlueprintDescriptorSidecars` instance).


#### `{description}`

Describes the parent node's functionality — what the node represents or what it instructs. Used in blueprint discovery and documentation generation.

**Example:**

```markdown
# Python Style Guide

## {description}

Guidelines and conventions for writing Python code that follows PEP 8 and project-specific standards.

## Setup

...content of Setup section...
```

In a parsed blueprint, access via:

```python
blueprint.sidecars.description
```

**Rendering behavior:** The description is **overridable** — if explicitly set on the blueprint object, it is used; otherwise, it falls back to the `{description}` node's content.


#### `{when_to_use}`

Indicates when the parent node should be enabled — the conditions or contexts that make the node relevant. Used for filtering nodes in blueprint UIs and documentation.

**Example:**

```markdown
# Python Style Guide

## {when_to_use}

Enabled when working with Python projects to enforce consistent code style.

## Setup

...content...
```

In a parsed blueprint, access via:

```python
blueprint.sidecars.when_to_use
```

**Rendering behavior:** `when_to_use` is **always rendered from the sidecar node content**, never overridden.


#### `{globs}`

Lists file glob patterns indicating which file types or paths make the parent node relevant. Each line is treated as a separate pattern — multiple patterns are supported. Used by IDE integrations and code editors to determine when to apply the prompt context.

**Example:**

```markdown
# Python Files

## {globs}

```glob
**/*.py
**/*.pyi
```

## Python Setup

...content...
```

In a parsed blueprint, access via:

```python
blueprint.sidecars.globs  # returns list of glob patterns
```

**Rendering behavior:** `globs` requires **fence-block parsing** (e.g., code blocks with ` ```glob ` delimiters). The patterns are extracted and stored in `blueprint.sidecars.globs`.

---

### Conditional Sidecar Nodes

Conditional sidecar nodes are real prompt content (e.g., instructions, rules) that are conditionally spliced into the rendered prompt based on explicit requests via the `contains_sidecar_nodes` parameter with matching flags.


#### `{prerequisite}`

Lists prerequisite instructions that apply whenever the parent node is enabled. When a parent node is checkmarked in a blueprint, its `{prerequisite}` sidecar children should typically be auto-included.

**Example:**

```markdown
# Data Processing

## {prerequisite}

Before using data processing functions, ensure the data source is initialized and validated.

Set up error handling:
```python
try:
    process_data()
except DataError as e:
    log_error(e)
```

## Main Content

...content...
```

**Rendering behavior:** Pass `contains_sidecar_nodes=SidecarNodeType.PREREQUISITE` to `generate_prompt()` or `generate_prompt_lines()` to auto-checkmark every `{prerequisite}` node whose parent is already checkmarked before rendering.

**Detection:** Use `SidecarNodeType.is_sidecar_node_of_type(node, SidecarNodeType.PREREQUISITE)` to identify prerequisite sidecars.


#### `{for_claude}`

Lists Claude-specific instructions that apply whenever the parent node is enabled. Pass `contains_sidecar_nodes=SidecarNodeType.FOR_CLAUDE` (or combine with `PREREQUISITE` via `|`) to auto-checkmark these nodes during Claude exports.

**Example:**

```markdown
# Task: Code Review

## {for_claude}

When reviewing code, focus on:
- Correctness and safety
- Readability and maintainability
- Performance implications

Always provide actionable feedback.

## Implementation

...content...
```

**Rendering behavior:** Pass `contains_sidecar_nodes=SidecarNodeType.FOR_CLAUDE` to auto-include `{for_claude}` sidecars during rendering. The constant `kaye.cli.claude.CONTAINING_SIDECAR_NODES` combines both `PREREQUISITE` and `FOR_CLAUDE` flags for all Claude skill and hook exports.

**Detection:** Use `SidecarNodeType.is_sidecar_node_of_type(node, SidecarNodeType.FOR_CLAUDE)` to identify Claude-specific sidecars.


## Blueprint Sidecar Metadata

A `PromptBlueprint` instance has a `.sidecars` attribute (typed `BlueprintDescriptorSidecars`) that exposes:

- `.description` — description of the blueprint's parent node (overridable)
- `.when_to_use` — when the blueprint should be applied
- `.globs` — list of file glob patterns for which the blueprint is relevant
- `.description_and_when_to_use` — derived property combining both fields

**Example:**

```python
from kaye.prompt import PromptBlueprint

bp = PromptBlueprint.parse(blueprint_text)

# Access descriptor sidecars
print(bp.sidecars.description)
print(bp.sidecars.when_to_use)
print(bp.sidecars.globs)

# Combine description and when_to_use
print(bp.sidecars.description_and_when_to_use)
```

## Checkmarking Behavior

Sidecar nodes are **never auto-checkmarked** by `create_full_blueprint()` or by `.checkmark()` with `recursively=True`.

- **Descriptor sidecars** (`{description}`, `{when_to_use}`, `{globs}`) are generally not checkmarked at all — their content is accessed via the `.sidecars` blueprint attribute, not rendered.
- **Conditional sidecar nodes** (`{prerequisite}`, `{for_claude}`) can be auto-checkmarked only if you explicitly pass a matching `SidecarNodeType` flag to `generate_prompt()` or `generate_prompt_lines()`.

To explicitly checkmark a sidecar node:

```python
bp.checkmark(sidecar_node)  # explicit checkmark
```


## Programmatic Usage

### Detecting Sidecar Nodes

```python
from kaye.prompt.sidecar_nodes import is_sidecar_node

if is_sidecar_node(node):
    print(f"{node.name} is a sidecar node")
```

### Detecting Sidecar Node Types

```python
from kaye.prompt.sidecar_nodes import SidecarNodeType

if SidecarNodeType.is_sidecar_node_of_type(
    node, SidecarNodeType.PREREQUISITE
):
    print("This is a prerequisite sidecar")
```

### Conditional Rendering

```python
from kaye.prompt.sidecar_nodes import SidecarNodeType

# Include prerequisites when rendering
prompt = bp.generate_prompt(
    contains_sidecar_nodes=SidecarNodeType.PREREQUISITE
)

# Include both prerequisites and Claude-specific instructions
prompt = bp.generate_prompt(
    contains_sidecar_nodes=(
        SidecarNodeType.PREREQUISITE | SidecarNodeType.FOR_CLAUDE
    )
)
```

## Corpus Format

In `prompt_corpus.md`, sidecar nodes follow the standard Markdown heading format:

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

## {for_claude}

This node contains Claude-specific instructions.
```

The heading level of a sidecar node (e.g., `##`, `###`) determines its depth in the tree; it must be **one level deeper than its parent node**.


## Key Differences from Regular Nodes

| Aspect | Regular Nodes | Sidecar Nodes |
| --- | --- | --- |
| **Identification** | Plain text name | Name in `{}` |
| **Rendered output** | Included in generated prompt | Excluded by default |
| **Auto-checkmarking** | Auto-checkmarked in full blueprints | Never auto-checkmarked |
| **Content type** | Free-form text | Metadata or conditional instructions |
| **Access** | Via checkmark status and rendering | Via `.sidecars` attribute or `contains_sidecar_nodes` flag |
| **Parent relationship** | Optional children of any node | Exclusively children of prompt nodes |

