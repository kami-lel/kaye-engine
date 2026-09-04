# Kaye Engine: Affordance Documentation

**Affordances** are a second, independent auto-checkmark mechanism for a common case: acknowledging whether a platform capability is available at all, rather than splicing in arbitrary named content. Every sidecar name this mechanism derives is still a `{brace}`-headed [sidecar node](sidecar-node-doc.md), checkmarked under the same "only under an already-checkmarked parent" rule — but its names and checkmark rules come from a purpose-built two-level registry (`kaye_engine/prompt/affordance_registry.py`) instead of a flat, caller-supplied name list.












## Concepts

The mechanism is two-level:

- **Affordance**: a conceptual capability family (e.g. `ask-user-question`)
- **Variant**: one concrete implementation of that family (e.g. `ask_user_input_v0`, `AskUserQuestion`)

A family may hold a single variant, standing in for a one-off capability with no siblings. A variant always belongs to exactly one affordance, named by its `affordance_name`.












## Corpus Authoring

Each level derives its own `Usage` sidecar plus one mirror-opposite sidecar:

| level | sidecar | checkmarked when |
| --- | --- | --- |
| variant | `{[variant canonical_name] Usage}` | that specific variant is present |
| variant | `{[variant canonical_name] Lack}` | that specific variant is absent |
| affordance | `{[affordance canonical_name] Usage}` | at least one of its registered variants is present |
| affordance | `{[affordance canonical_name] Fallback}` | every one of its registered variants is absent |

Author each sidecar under a checkmarked node, describing what to do in that case, following the standard [sidecar heading conventions](sidecar-node-doc.md#in-prompt-corpus) — one level deeper than its parent. An affordance with zero registered variants never fires either of its sidecars.

**Naming caveat:** because both levels use the literal suffix `Usage`, an affordance and a variant sharing the exact same `canonical_name` string collide on one sidecar-map key — keep affordance and variant `canonical_name`s unique across both registries.












## Programmatic API

### `affordance_registry.py`

#### `Affordance`

A registered capability family.

**Attributes:**
- `canonical_name` (`str`): unique identifier for this affordance
- `usage_sidecar_name` (`str`, property): `"[{canonical_name}] Usage"`
- `fallback_sidecar_name` (`str`, property): `"[{canonical_name}] Fallback"`



#### `Variant`

A single registered concrete implementation of an `Affordance`.

**Attributes:**
- `canonical_name` (`str`): unique identifier for this variant
- `affordance_name` (`str`): canonical name of the `Affordance` this variant implements
- `usage_sidecar_name` (`str`, property): `"[{canonical_name}] Usage"`
- `lack_sidecar_name` (`str`, property): `"[{canonical_name}] Lack"`



#### `register_variant(canonical_name, affordance_name)`

The single entry point for populating both registries.

**Signature:**
```python
def register_variant(canonical_name: str, affordance_name: str) -> Variant
```

**Description:**
Constructs a `Variant` and inserts it into `variant_registry` under `canonical_name`, linked to the `Affordance` named `affordance_name` — registering that affordance first, under `affordance_registry`, when it isn't already registered. There is no separate call for registering an affordance on its own.

**Raises:** `ValueError` if `canonical_name` is already registered as a variant.

**Example:**
```python
from kaye_engine.prompt.affordance_registry import register_variant

# a two-variant affordance
register_variant("ask_user_input_v0", "ask-user-question")
register_variant("AskUserQuestion", "ask-user-question")

# a single-variant affordance
register_variant("ClaudeCode:TodoWrite", "ClaudeCode:TodoWrite")
```



#### `affordance_registry` / `variant_registry`

Module-level `dict[str, Affordance]` / `dict[str, Variant]`, keyed by `canonical_name`. Both start empty and are populated only as a side effect of `register_variant()` calls — there is no direct-insert API.

The `kaye-engine list-affordance`/`list-variant` CLI subcommands (q.v. [CLI Integration](#cli-integration) below) print these registries' sorted keys.












### Checkmark Evaluation

`_build_variant_sidecar_map(variants)` (private helper, `kaye_engine/prompt/blueprint/render.py`) turns a collection of available variant `canonical_name`s into a `dict[str, bool]` of every derived sidecar name:

- for each `variant_registry` entry: `usage_sidecar_name` is `True` iff its `canonical_name` is in `variants`; `lack_sidecar_name` is the negation
- for each `affordance_registry` entry: `usage_sidecar_name` is `True` iff *any* of its registered variants are present in `variants`; `fallback_sidecar_name` is `True` iff it has at least one registered variant and *all* of them are absent

`_splice_conditional_sidecars()` feeds this map alongside the plain `conditional_sidecars` name set — a sidecar node only checkmarks when its name matches one or the other, and only when its parent is already checkmarked.

This whole mechanism is opt-in per render call, via `RenderProfile.variants`:

- `variants=None` (the default) skips affordance checkmarking entirely, leaving any prior checkmarks as-is
- `variants=()` runs it against an empty available set — every `Lack` sidecar fires, and every `Fallback` sidecar whose affordance has ≥1 registered variant fires too












## CLI Integration

Every rendering command (any CLI subcommand reaching `render_prompt()`/`render_prompt_lines()`) inherits a `--variant VARIANT [VARIANT ...]` flag from `build_render_profile_parent_parser()` (`kaye_engine/cli/render_profile_parser.py`), alongside `--surface`, `--conditional-sidecar`, `--comment`/`--no-comment`, and `--sparseness`. `--variant` takes one or more variant canonical names and unions additively with whatever `--surface` derives — it has no short flag. Full flag table and merge semantics: `AGENTS.md` and `CONTEXT.md`.

Two read-only subcommands inspect the registries directly:

| command | alias | prints |
| --- | --- | --- |
| `kaye-engine list-affordance` | `lsa` | `affordance_registry` canonical names, sorted |
| `kaye-engine list-variant` | `lsv` | `variant_registry` canonical names, sorted |

How a consumer's own CLI determines what to pass as `variants` for a given invocation — typically by mapping a `--surface` name to a fixed variant list — is entirely up to that consumer; the engine has no concept of "surface" or "which variants apply where." Q.v. [`claude-doc.md`](claude-doc.md) for how kaye-engine's own `setup_claude_cli()` wires `--surface` to per-surface `RenderProfile.variants` for Claude platform tools specifically.












## Example

```python
from kaye_engine.prompt.affordance_registry import register_variant
from kaye_engine.prompt.blueprint.render_profile import RenderProfile

# register a single-variant affordance and a two-variant affordance
register_variant("ClaudeCode:TodoWrite", "ClaudeCode:TodoWrite")
register_variant("ask_user_input_v0", "ask-user-question")
register_variant("AskUserQuestion", "ask-user-question")

# Usage/Lack/Fallback checkmarking for every registered affordance/variant
prompt = bp.render_prompt(
    profile=RenderProfile(variants=("ClaudeCode:TodoWrite",))
)
```

With only `"ClaudeCode:TodoWrite"` available: its own `Usage` sidecar checkmarks (and its `Lack` does not); `ask_user_input_v0` and `AskUserQuestion` are both absent, so each fires its `Lack` sidecar, and `ask-user-question`'s `Fallback` sidecar fires (its `Usage` does not, having zero present variants) — while `ClaudeCode:TodoWrite` the affordance fires its own `Usage` (one present variant), never its `Fallback`.
