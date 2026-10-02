# Kaye Engine: support for Hermes

`kaye-engine hermes` (alias `m`) writes a Hermes home directory: a root `SOUL.md`, one `SOUL.md` per profile, and every entry of `exportable_registry` as an Agent Skill. The command is mechanism only; the consumer project names which blueprints become the soul and the profiles.

## Usage

```bash
kaye-engine hermes FOLDER             # write to FOLDER
kaye-engine m FOLDER -n               # report every write, change nothing
kaye-engine hermes FOLDER -s 0 -C     # the shared render options apply
```

`FOLDER` is required; there is no default location.

The command accepts the shared render options (`--surface` where the consumer configured surfaces, `--comment`/`--no-comment`, `--conditional-sidecar`, `--variant`, `--sparseness`, `--reverse-order`; q.v. [`render-profile-doc.md`](render-profile-doc.md)) and `-n`/`--dry-run`. Comments are hidden by default and no surface is selected by default.

## Output Tree

```text
FOLDER/
├── SOUL.md
├── skills/
│   └── <category>/<skill-name>/SKILL.md
└── profiles/
    └── <profile>/SOUL.md
```

- `SOUL.md`: the soul blueprint, rendered
- `profiles/<profile>/SOUL.md`: the blueprint mapped to that profile, rendered
- `skills/<category>/`: one folder per entry of `exportable_registry`, as `skill` does (q.v. [`exportable-registry-doc.md`](exportable-registry-doc.md))

The two `SOUL.md` kinds render from `blueprint_registry`, so a blueprint registered with `is_exportable=False` can still be a soul or a profile; it never becomes a skill. An existing file is overwritten.

## Consumer Configuration

```python
from kaye_engine import setup_hermes_cli

setup_hermes_cli(
    "kaye",                             # skills/<category>/
    "chat",                             # root SOUL.md
    {"kaye": "kaye-chat", "ria": "ria-chat"},  # profiles/<name>/SOUL.md
)
```

Call it after every named blueprint is registered; an unregistered name logs critical and exits 1. Running `hermes` before the call also exits 1. The skill version is the one given to `setup_claude_cli`.

## Dry Run

With `-n`, every folder and file is reported with the `dry` badge and nothing is written.
