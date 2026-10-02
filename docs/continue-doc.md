# Kaye Engine: support for Continue

<!-- fixme mpv continue support doc -->

`kaye-engine continue` (alias `c`) writes every entry of `exportable_registry` into a [Continue](https://docs.continue.dev) config folder, as a **rule** or as a **prompt**. Selection reuses `is_exportable` — an entry kept out of `exportable_registry` is never exported — so no Continue-specific flag exists.

## Usage

```bash
kaye-engine continue                  # write to ~/.continue
kaye-engine continue FOLDER           # write to FOLDER
kaye-engine c FOLDER -s 0 -C          # the shared render options apply
```

Use the default when Continue runs on this machine. Pass a custom `FOLDER` to inspect the output first, or to export into a project-local Continue folder.

The command accepts the shared render options (`--surface` where the consumer configured surfaces, `--comment`/`--no-comment`, `--conditional-sidecar`, `--variant`, `--sparseness`, `--reverse-order`; q.v. [`render-profile-doc.md`](render-profile-doc.md)). Comments are hidden by default and no surface is selected by default.

## Output Tree

```text
FOLDER/
├── rules/
│   └── <canonical_name>.md
└── prompts/
    └── <canonical_name>.md
```

Both subfolders are always created. A file is named after its entry's `canonical_name`; an existing file of the same name is overwritten.

## Classification

Each entry becomes a rule, a prompt, or nothing, decided by the export-policy flags (q.v. [`exportable-registry-doc.md`](exportable-registry-doc.md)). `always_apply` forces a rule, since "always apply" has no meaning for a prompt.

| `always_apply` | `llm_invokable` | `is_user_invokable` | result | `alwaysApply` |
| --- | --- | --- | --- | --- |
| ✔️ | 〃 | 〃 | rule in `rules/` | `true` |
| ❌ | ✔️ | 〃 | rule in `rules/` | `false` |
| ❌ | ❌ | ✔️ | prompt in `prompts/`, `invokable: true` | `false` |
| ❌ | ❌ | ❌ | skipped | ➖ |

Abbreviation groups are never user-invokable and always LLM-invokable, so they export as rules.

## File Format

Frontmatter fields follow Continue's own schema.

- `name`: the entry's display name
- `description`: a blueprint's description and when-to-use sidecars combined; an abbreviation group's display name; omitted when empty
- `alwaysApply`: `true` only for an `always_apply` rule
- `invokable`: `true`, prompts only
- `globs`: a blueprint's `{globs}` sidecar entries; omitted when empty

The body is the entry's `content()`, rendered with the resolved render profile.

## Surface Behaviour

`--surface` exists only when the consumer project configured surface profiles, and it is repeatable across names like the other rendering commands. With no `--surface`, only the entry's own `render_profile` and the explicit flags shape the output.

## Dry Run

`--dry-run` lists every folder and file the export would create or overwrite, each line carrying the `dry` badge, and writes nothing.

## Check the Result

Open one file from each subfolder. A rule's frontmatter carries `name`, and where present `description`, `alwaysApply` and `globs`; a prompt's carries `invokable: true`. The body is the entry's rendered content.
