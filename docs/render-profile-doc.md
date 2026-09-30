# Kaye Engine: Render Profile Documentation

<!--
Fixme CLI provide none and all
Bug -u & --variant fail get displayed in all docstring
-->


A **`RenderProfile`** holds the settings for one render of a prompt. It answers questions such as:

- which optional sidecars and affordance variants to include
- in which order to walk the tree
- how many blank lines to keep
- whether to end with a generated-by comment

Profiles are small and mergeable. A registry entry, a Claude surface, and the command line can each contribute one, and the engine merges them into the single profile that a render uses. The class lives in `kaye_engine/prompt/blueprint/render_profile.py`.

## Quick Start

Pass a profile to `render_prompt()` through `profile=`:

```python
from kaye_engine.prompt.blueprint.render_mode import RenderMode
from kaye_engine.prompt.blueprint.render_profile import RenderProfile

prompt = bp.render_prompt(
    profile=RenderProfile(
        conditional_sidecars=("[Bash]",),
        mode=RenderMode.POST_ORDER,
        sparseness=0,
    )
)
```

Any field left out keeps its default, so `RenderProfile()` is the plain render: nothing extra included, tree walked top to bottom, blank-line runs capped at one.













## Fields

| Field | Default | What it does |
| --- | --- | --- |
| `conditional_sidecars` | `()` | names of sidecar nodes to include, see [Conditional Sidecars](#conditional-sidecars) |
| `variants` | `None` | affordance variants available on the target, see [Variants](#variants) |
| `mode` | `RenderMode.NORMAL` | how the tree is walked and printed, see [Render Modes](#render-modes) |
| `sparseness` | `1` | how many blank lines to keep, see [Sparseness](#sparseness) |
| `show_comment` | `False` | add a trailing generated-by comment, see [Comment](#comment) |
| `display_name` | `""` | the `NAME` in that comment, left out when empty |
| `disable_first_heading` | `False` | drop the first heading line but keep its content |
| `glossary_priority_threshold` | `None` | glossary filter, see [Glossary Fields](#glossary-fields) |
| `is_sorted` | `None` | 〃 |
| `is_numbered_list` | `None` | 〃 |

`profile.as_kwargs()` returns every field as a `dict`.

`disable_first_heading` only applies to a positive render. A negative render ignores it, as it ignores any field that its docstring does not list.

### Glossary Fields

The three glossary fields take effect only inside inline `(((name)))` substitutions, because those receive the profile's fields as keyword arguments. Glossary nodes rendered in the tree walk do not read them. They get only the keyword arguments passed straight to `render_prompt()`, which is how `kaye-engine dynamic-node -t THRESHOLD` sets `glossary_priority_threshold=`. See [Dynamic Node Documentation](dynamic-content-doc.md#feeding-render-time-input).













## Merging

`a.merge(b)` combines two profiles into a **new** one. Neither `a` nor `b` changes. The fields combine differently by kind:

| Kind | Fields | Rule |
| --- | --- | --- |
| Collections | `conditional_sidecars`, `variants` | union, duplicates dropped, first-seen order |
| Everything else | all other fields | `b` wins |

Two details matter in practice.

**`b` wins even with its default.** A field `b` never set still overrides `a`:

```python
a = RenderProfile(conditional_sidecars=("a", "b"), variants=("x",), sparseness=0)
b = RenderProfile(conditional_sidecars=("b", "c"))

a.merge(b)
# conditional_sidecars=('a', 'b', 'c'), variants=('x',), sparseness=1
b.merge(a)
# conditional_sidecars=('b', 'c', 'a'), variants=('x',), sparseness=0
```

`a.merge(b)` gives `sparseness=1`, because `b`'s default replaced `a`'s `0`. To keep a value through a merge, put its profile on the right-hand side.

**`None` means "off" for `variants`.** It adds nothing to a union, and the result is `None` only when every profile being merged has `None`.

`mode` also counts as a "`b` wins" field, so merging never combines two modes. To get `NEGATIVE` and `IMAGE` together, build the combined value yourself:

```python
RenderProfile(sparseness=0, mode=RenderMode.IMAGE).merge(
    RenderProfile(mode=RenderMode.NEGATIVE | RenderMode.IMAGE)
)
```













## Render Modes

`RenderMode` (`kaye_engine/prompt/blueprint/render_mode.py`) is a flag enum set on `RenderProfile.mode`. Combine members with `|`.

| Member | Effect |
| --- | --- |
| `NORMAL` | the plain positive render |
| `NEGATIVE` | print the negative prompt (`{avoid}` content) instead of the positive one |
| `POST_ORDER` | print children before their parent |
| `REVERSE_ORDER` | reverse the order of siblings at every level |
| `IMAGE` | shorthand for `POST_ORDER \| REVERSE_ORDER` plus flat `title:` headings and `sparseness=1` |

`POST_ORDER` and `REVERSE_ORDER` are independent of each other and work on both the positive and the negative render. Nothing is dropped, only reordered.

Each mode changes the walk like this:

- `POST_ORDER`: each node prints after its children, so a parent's heading and content come last
- `REVERSE_ORDER`: siblings print in reverse, so a later section comes before an earlier one
- `IMAGE`: every heading becomes a bare `title:` line, whatever its depth, and the order is post-order with reversed siblings

### Negative Prompt

`NEGATIVE` collects the `{avoid}` sidecars of the tree instead of the normal content. The rules for what appears:

- a node's `{avoid}` content prints under that node's heading, and only when the node is checkmarked
- the tree is always walked all the way down, so a checkmarked node below an unchecked one still contributes
- a node with no `{avoid}` content anywhere beneath it is left out

Adding `IMAGE` removes every title, leaving only the `{avoid}` text, with its blocks still separated by a blank line. Any other combination, such as `NEGATIVE | POST_ORDER`, keeps its headings. See [Negative-Instruction Sidecar](sidecar-node-doc.md#negative-instruction-sidecar) and [generate negative prompt](prompt-doc.md#generate-negative-prompt). Whether an `Exportable` can render a negative prompt at all is its `supports_negative_content` flag, see [Exportable Registry Documentation](exportable-registry-doc.md).













## Conditional Sidecars

Sidecar nodes such as `{[Bash]}` are left out of every render unless a profile asks for them. List their names in `conditional_sidecars`:

```python
bp.render_prompt(profile=RenderProfile(conditional_sidecars=("[Bash]",)))
```

Things to know:

- a sidecar is included only when its parent node is checkmarked as well
- any `{name}` sidecar can be requested, including the reserved descriptor names
- `{avoid}` is normally reached through `RenderMode.NEGATIVE` instead

See [Sidecar Node Documentation](sidecar-node-doc.md#conditional-sidecar-nodes) for the node types.

## Variants

`variants` switches on the affordance sidecars: `Usage`, `Lack`, and `Fallback`. List the variants available on the target, and the engine picks the matching sidecars:

- a listed variant includes its `Usage` sidecar
- an unlisted variant includes its `Lack` sidecar
- an affordance includes its `Usage` sidecar when any of its variants is listed, otherwise its `Fallback` sidecar

```python
bp.render_prompt(profile=RenderProfile(variants=("ClaudeCode:TodoWrite",)))
```

The field has three states:

- `None`: off, affordance sidecars are ignored (default)
- `()`: on, with every variant absent, so every `Lack` and `Fallback` sidecar applies
- `("A", "B")`: on, with `A` and `B` present

See [Affordance Documentation](affordance-doc.md#checkmark-evaluation) for how the sidecars are derived. Conditional sidecars and variants share one step before the tree walk, and both require the sidecar's parent to be checkmarked.

## Sparseness

`sparseness` limits how many blank lines survive in the finished text:

| Value | Result |
| --- | --- |
| `-1` | everything on one line, with `↵` in place of each newline |
| `0` | no blank lines |
| `1` | each run of blank lines becomes one blank line |
| `N` | runs are capped at `N` blank lines |
| `99` | no trimming at all |

Good to know:

- blank lines at the start and end are always removed, except at `99`
- blank lines inside a fenced code block are never touched, at any level
- the dataclass default is `1`, while the CLI default is `DEFAULT_SPARSENESS` (`0`), see [CLI Options](#cli-options)
- `IMAGE` mode overrides any `sparseness` with `1`
- the trailing comment follows `sparseness`: a block by default, one line at `-1`, see [Comment](#comment)
- `{description}` and `{when_to_use}` always render at `-1`, so a multi-line value becomes one string
- inline `(((name)))` substitutions are applied first, and `sparseness` is applied afterward to the whole result, so a substitution's blank lines follow the same rule













## Comment

With `show_comment`, the text ends with a generated-by comment, one line per fact:

```
<!--
blueprint: NAME
Kaye Engine v1.2.3
-->
```

- the `blueprint:` line is left out when `display_name` is empty; `BlueprintRegistry.content()` fills an empty one from the registry entry's own name
- at `sparseness=-1` the whole comment joins into the single line, `<!-- blueprint: NAME↵Kaye Engine v1.2.3 -->`
- the comment is added after `IMAGE` mode's heading rewrite, so a line starting with `#` is never rewritten

A client project appends its own lines with `register_comment_line(line)`:

```python
from kaye_engine import register_comment_line

register_comment_line("My Project v0.1.0")
```

- registered lines follow the default lines, in registration order
- registering the same line again is ignored
- a non-`str` line raises `TypeError`; a line with a newline or `-->` raises `ValueError`

## Where Profiles Come From

A render can draw on three sources, from the most general to the most specific:

1. **Entry default**: the `render_profile` given to `register_blueprint()`, the baseline for that one blueprint
2. **Surface**: a named profile from the consumer's `surface_profiles`, chosen with `--surface`
3. **Command-line flags**: `--variant`, `--conditional-sidecar`, `--sparseness`, `--comment`, `--reverse-order`

The command line merges sources 2 and 3 into one profile with `resolve_render_profile()`. Then `BlueprintRegistry.content(profile=...)` merges it onto the entry's default, like this:

```python
entry.render_profile.merge(profile)
```

The caller's profile is on the right, so its collections add to the entry's and its other fields overwrite the entry's, defaults included, see [Merging](#merging). When no `profile=` is passed, the entry's default is used as is.

Set an entry default when registering:

```python
from kaye_engine import register_blueprint
from kaye_engine.prompt.blueprint.render_profile import RenderProfile

register_blueprint(
    "coder",
    "Kaye Peer Coder",
    coder_blueprint,
    render_profile=RenderProfile(conditional_sidecars=("[Claude]",)),
)
```

Calling `PromptBlueprint.render_prompt(profile=...)` or `generate_prompt_without_dependencies(profile=...)` directly skips entry defaults. Both fall back to `RenderProfile()` when given no profile. Extra keyword arguments such as `query=` are not profile fields; they pass through to each node's `content_lines()`.

## Surfaces

A **surface** is a named render target, such as `chat`, `code`, or the VS Code extension. Surfaces support different tools, so one corpus should render differently for each. A surface with Bash access gets the Bash usage sidecar, and one without does not.

Kaye Engine defines no surfaces itself. A consumer passes a `dict[str, RenderProfile]` to `setup_claude_cli(surface_profiles=...)`, where each profile lists that surface's `variants` and `conditional_sidecars`:

```python
from kaye_engine.prompt.blueprint.render_profile import RenderProfile

SURFACE_PROFILES = {
    "chat": RenderProfile(
        variants=("ClaudeChat:ask_user_input_v0", ...),
        conditional_sidecars=("[ClaudeChat]", "[Claude]"),
    ),
    "code": RenderProfile(
        variants=("ClaudeCode:AskUserQuestion", ...),
        conditional_sidecars=("[ClaudeCode]", "[Claude]"),
    ),
}

setup_claude_cli(..., surface_profiles=SURFACE_PROFILES)
```

Then `--surface NAME [NAME ...]` (`-u`) selects one or more surfaces:

- several surfaces merge in the order given, so `--surface chat code` unions both profiles' collections
- the allowed names are the dict's keys
- `--surface` is absent from the CLI when no `surface_profiles` were configured
- each `claude` subcommand preselects a surface when the flag is omitted, see [Per-Command Defaults](#per-command-defaults)

See also [Claude Documentation](claude-doc.md).













## CLI Options

Every **rendering command** takes the same six options. A rendering command is any subcommand that reaches `PromptBlueprint.render_prompt()`, directly or through `Exportable.content()`:

- `blueprint generate`
- `dynamic-node`
- `exportable`
- `skill`, `claude plugin`, `claude marketplace`, `claude code`
- `claude user-system-prompt`, `claude vs-code-extension`

| Flag | Short | Effect |
| --- | --- | --- |
| `--surface` | `-u` | surface(s) to render for, see [Surfaces](#surfaces) |
| `--comment` / `--no-comment` | `-c` / `-C` | turn `show_comment` on or off |
| `--conditional-sidecar` | `-i` | extra sidecar names, added to the surface's |
| `--variant` | ➖ | extra variant names, added to the surface's |
| `--sparseness` | `-s` | set `sparseness`, see [Sparseness](#sparseness) |
| `--reverse-order` | ➖ | add `RenderMode.REVERSE_ORDER` to the mode |

A shared parent parser, `build_render_profile_parent_parser()`, registers these flags, and `resolve_render_profile()` turns the parsed arguments into one `RenderProfile`. Both are in `kaye_engine/cli/render_profile_parser.py`.

Two notes on the flags:

- `claude user-system-prompt` already uses `-c` for `--coder`, so its comment flags have no short form
- `blueprint show` has the same comment flags but is not a rendering command

### How Flags Resolve

`resolve_render_profile()` works in this order:

1. start from `RenderProfile()` and merge in each selected surface's profile
2. if `--variant` was given or any surface is selected, merge in the `--variant` names; this switches `variants` **on**, so a surface with no listed variants yields `()` instead of `None`
3. if `--conditional-sidecar` was given, merge those names in
4. work out `mode`, adding `REVERSE_ORDER` when `--reverse-order` was passed
5. merge in `sparseness`, `show_comment`, and `mode` last

Two consequences follow. `--variant` and `--conditional-sidecar` only add to what a surface provides. And `sparseness` and `show_comment` always come from the flag or the command's own default, never from a surface profile.

### Per-Command Defaults

A command supplies its own fallback when a flag is omitted:

| Command | Comment | Surface |
| --- | --- | --- |
| `blueprint generate` | on | none |
| `dynamic-node` | off | none |
| `exportable` | off | none |
| `skill` | off | `chat` |
| `claude plugin` | off | `chat`, `cowork` |
| `claude marketplace` | off | `vsc` |
| `claude code` | off | `code` |
| `claude vs-code-extension` | on | `vsc` |
| `claude user-system-prompt` | on | `chat`, `cowork` |

A default surface only works when the consumer's `surface_profiles` defines that name.

`--sparseness` defaults to `DEFAULT_SPARSENESS` (`kaye_engine/cli/__init__.py`, currently `0`), unless a subcommand passes its own `default_sparseness` to `build_render_profile_parent_parser()`.

`blueprint generate` also sets `display_name` to the blueprint's registered name, so the trailing comment names it.

### Handing the Profile Down

The resolved profile travels as a single `render_profile=` argument through every `claude` export, from skill to user prompt, and reaches `Skill.from_exportable()`, which calls `exportable.content(profile=...)`. The entry's own default is merged in at that point, not replaced.
