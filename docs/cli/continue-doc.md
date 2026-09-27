# Guide: The continue Command

This guide shows how to export your exportables into [Continue](https://docs.continue.dev) with `kaye-engine continue` (alias `c`). For the flat reference, q.v. [`continue-doc.md`](../continue-doc.md).

## Run It

```bash
kaye-engine continue                # write to ~/.continue/
kaye-engine continue FOLDER         # write to FOLDER instead
kaye-engine c FOLDER -s 0 -C        # the shared render flags apply
```

Use the default when Continue runs on this machine. Pass a custom `FOLDER` to inspect the output first, or to export into a project-local Continue folder.

## What Gets Written

```text
FOLDER/                      (default: ~/.continue/)
├── rules/
│   └── <canonical_name>.md
└── prompts/
    └── <canonical_name>.md
```

Both subfolders are always created. Files are named after each entry's `canonical_name`, and an existing file of the same name is overwritten.

## Rule, Prompt, or Skipped

Each exportable lands in one place, decided by its export-policy flags:

| `always_apply` | `llm_invokable` | `is_user_invokable` | Result |
| --- | --- | --- | --- |
| ✔️ | 〃 | 〃 | rule, written with `alwaysApply: true` |
| ❌ | ✔️ | 〃 | rule, `alwaysApply: false` |
| ❌ | ❌ | ✔️ | prompt, `invokable: true` |
| ❌ | ❌ | ❌ | skipped |

- Always-Apply Entries: `always_apply` forces a rule, since "always apply" means nothing for a prompt
- Abbreviation Groups: never user-invokable, always LLM-invokable, so they export as rules

## Render Flags

The command takes the shared render flags: `--comment`/`--no-comment`, `--sparseness`, `--variant`, `--conditional-sidecar`, `--reverse-order`, and `--surface` where the consumer configured surfaces. Q.v. [`render-profile-doc.md`](../render-profile-doc.md). Comments are hidden by default.

## Check the Result

Open one file from each subfolder. A rule's frontmatter carries `name`, and where present `description`, `alwaysApply` and `globs`; a prompt's carries `invokable: true`. The body is the entry's rendered content.
