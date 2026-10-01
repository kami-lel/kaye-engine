# Kaye Engine: Sidecar Node Documentation

**Sidecar nodes** are corpus nodes with names enclosed in curly braces, e.g. `{description}`, `{when_to_use}`. They are attached to parent nodes in the prompt tree and hold structured metadata or conditional content about their parent. Sidecar nodes appear in the blueprint preview tree but are **not** included in the rendered prompt output by default.


































## Concepts

Sidecar nodes enable two complementary patterns, plus affordances, a third mechanism that checkmarks sidecars naming a platform capability, covered in [`affordance-doc.md`](affordance-doc.md):













### Descriptor Sidecars

Descriptor sidecars are metadata fields that describe a parent node's purpose, relevance, and applicable contexts. They are consumed through a blueprint's `.meta` (a `BlueprintMeta`), which points at the sidecar nodes by path.





#### `{description}`

Describes the parent node's functionality — what the node represents or what it instructs. Used in blueprint discovery and documentation generation.

**Rendering behavior:** The description is **overridable** — if the blueprint's `meta.description` literal is set, it is used; otherwise, it falls back to the content of the node at `meta.description_node`.

**Access:** `show_description(blueprint)`





#### `{when_to_use}`

Indicates when the parent node should be enabled — the conditions or contexts that make the node relevant. Used for filtering nodes in blueprint UIs and documentation.

**Rendering behavior:** `when_to_use` is **always rendered from the sidecar node content**, never overridden.

**Access:** `show_when_to_use(blueprint)`





#### `{globs}`

Lists file glob patterns indicating which file types or paths make the parent node relevant. Each line is treated as a separate pattern — multiple patterns are supported. Used by IDE integrations and code editors to determine when to apply the prompt context.

**Rendering behavior:** `globs` requires **fence-block parsing** (e.g., code blocks with ` ```glob ` delimiters). The patterns are extracted from the node at `meta.globs_node`.

**Access:** `show_globs(blueprint)` (returns list of glob patterns)




### Negative-Instruction Sidecar

`{avoid}` is neither a descriptor sidecar nor a conditional one — it is
never reachable through `.meta`, and it is never spliced into a rendered
prompt by naming it in `conditional_sidecars` (though that splice
mechanism still works structurally on it like on any other name,
independent of the render below). Instead, `{avoid}` content is
discovered automatically, at any depth, by
`kaye_engine.prompt.blueprint.render.render_negative_prompt_lines()`,
reached by setting `RenderMode.NEGATIVE` on a render profile, which
picks it in place of the positive render; q.v.
[`render-profile-doc.md`](render-profile-doc.md#negative-prompt).




#### `{avoid}`

Carries negative-instruction/negative-example content for the parent
node — what the parent's positive content should *not* produce.

**Rendering behavior:** a node's own `{avoid}` child contributes to
the negative prompt, under that node's own heading, only when the
node itself is checkmarked; the literal `{avoid}` heading itself is
never shown. Descendants are always walked regardless of an
ancestor's own checkmark, so a checkmarked descendant below an
unchecked ancestor still contributes. A node with no `{avoid}`
content of its own is transparent: its contributing descendants'
rendered blocks splice in directly, with no heading of this node's
own. A node with no `{avoid}` child and no contributing descendant is
omitted entirely. It is never included in the *positive* prompt unless
explicitly named via `conditional_sidecars`.

**Access:** `RenderMode.NEGATIVE` only — there is no
`render_avoid` function or `.meta` field.













### Conditional Sidecar Nodes

Conditional sidecar nodes are real prompt content (e.g., instructions, rules) that are conditionally spliced into the rendered prompt based on explicit requests via a render profile's `conditional_sidecars` field, a plain collection of sidecar names. Unlike descriptor sidecars, there is no fixed set of conditional names — any `{name}` heading can be requested this way, including reserved descriptor names.

**Rendering behavior:** name the sidecars in a render profile's `conditional_sidecars` to auto-include them during rendering, q.v. [`render-profile-doc.md`](render-profile-doc.md#conditional-sidecars).

Q.v. [`claude-doc.md`](claude-doc.md) for the list of `{[ClaudeCode:...]}`/`{[ClaudeChat:...]}` sidecars, which Claude export surface includes each of these, and the underlying API.

A conditional sidecar can itself carry sidecar children — e.g. its own `{description}` — since detection and depth placement apply per-node, independent of the parent's own type.






























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

    ## {[ClaudeCode:TodoWrite]}

    This node contains TodoWrite-specific instructions.
    ```

**Heading conventions:**
- The heading level of a sidecar node (e.g., `##`, `###`) determines its depth in the tree
- A sidecar node must be **one level deeper than its parent node**
- Sidecar nodes are identified by the pattern `^\{.+\}$` (any name in curly braces) — there is no fixed vocabulary; any name is a valid sidecar
- `description`, `when_to_use`, and `globs` are reserved names consumed as metadata through `BlueprintMeta`; `avoid` is reserved too, but discovered directly by `render.render_negative_prompt_lines()` (via `RenderMode.NEGATIVE`) instead (q.v. [Negative-Instruction Sidecar](#negative-instruction-sidecar)); every other name is available for conditional content inclusion

**Checkmarking behavior:**
- Sidecar nodes are **never auto-checkmarked** by `create_blueprint(is_full=True)` or by `checkmark_nodes()` with `is_recursive=True`
- Descriptor sidecars are generally not checkmarked at all — their content is accessed through the blueprint's `.meta`
- Conditional sidecar nodes can be auto-checkmarked only when you explicitly list their name in a render profile's `conditional_sidecars`, q.v. [`render-profile-doc.md`](render-profile-doc.md#conditional-sidecars)
- To explicitly checkmark a sidecar node: `bp = checkmark_nodes(bp, sidecar_node)`











































## Programmatic API

### `kaye_engine/prompt/sidecar_node.py`

#### `get_sidecar_name(node)`

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
if name == "[ClaudeCode:TodoWrite]":
    print("this is a conditional sidecar node")
```

---

#### `BlueprintMeta`

Frozen container pointing at the descriptor sidecar nodes of a blueprint.

**Location:** `kaye_engine/prompt/blueprint/data.py`

**Description:**
Holds the descriptors (description, when_to_use, globs) of a blueprint as **node paths**, never node objects. They are never rendered into the prompt output — they exist purely for discovery, documentation, and export. `create_blueprint_from_node()` fills them from the node's own sidecar children; `replace_meta()` replaces any of them.

**Fields:**

- `description`: `str or None`, a literal description that takes priority over the node
- `description_node`: `NodePath or None`, path of the node holding the description
- `when_to_use_node`: `NodePath or None`, path of the node holding the when-to-use
- `globs_node`: `NodePath or None`, path of the node holding the glob patterns

**Reading the descriptors:**

All three are functions of `kaye_engine.prompt.blueprint.render` (re-exported from `kaye_engine.prompt`), and need the corpus loaded:

- `show_description(blueprint)`: the literal `description` when set, else the description node's content as one line, else `""`
- `show_when_to_use(blueprint)`: the when-to-use node's content as one line, else `""`
- `show_description_and_when_to_use(blueprint)`: the literal `description` alone when set, else the description and when-to-use node content joined by the replacement newline symbol
- `show_globs(blueprint)`: the patterns of the globs node's first fenced `glob` block, one per line

**Example:**
```python
from kaye_engine.prompt import (
    create_blueprint_from_node,
    show_globs,
    show_description,
    show_when_to_use,
    replace_meta,
)

bp = create_blueprint_from_node("Coder Python")

print(show_description(bp))
print(show_when_to_use(bp))
print(show_globs(bp))  # e.g., ["**/*.py", "**/*.pyi"]

bp = replace_meta(bp, description="Custom description")
print(show_description(bp))  # "Custom description"
```

**Merging:**

`merge_blueprints(left, right)` merges the metadata too: `left` wins every field it sets, `right` fills the rest.

Conditional rendering with conditional sidecar nodes: q.v. [`render-profile-doc.md`](render-profile-doc.md#conditional-sidecars).
