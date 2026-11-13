# Kaye Engine: Consumer Documentation

A **consumer** owns corpus, values and skills in `kaye-engine`. It is one Python setup function that registers everything, then hands control to the engine's CLI; there is no configuration file. This page is a starting point: read the code for the details, and the [minimal-consumer](https://github.com/kami-lel/kaye-library/tree/dev/examples/minimal-consumer/example_consumer/__init__.py) for a working example.

## Setup Order

Register in this order; later steps validate against earlier ones:

1. Consumer: `register_consumer(display_name, canonical_name, version)`
2. Glossaries: `register_abbr_glossary(...)`, see [abbreviations](abbrs-doc.md)
3. Abbreviation data: `populate_abbr_data_with_json_file(path)`
4. Substitutions: `register_dynamic_substitution(name, value)`, see [dynamic content](dynamic-content-doc.md)
5. Corpus: `register_corpus_under_node(...)`, then `load_corpus_tree()`, see [corpus format](corpus-doc.md)
6. Blueprints: `register_blueprint(...)`, then `set_entry_consumer(canonical_name)`, see [prompt](prompt-doc.md#prompt-blueprint) and the [exportable registry](exportable-registry-doc.md)

## Engine Only

<!-- BUG example crashes: str source ending .md raises ValueError, needs Path; step 4 takes a DynamicSubstitution, not a plain value -->

```python
from kaye_engine import (
    load_corpus_tree,
    register_blueprint,
    register_consumer,
    register_corpus_under_node,
    set_entry_consumer,
)
from kaye_engine.prompt.blueprint import (
    create_blueprint_from_node,
    get_corpus_node,
)


def setup_my_consumer():
    register_consumer("My Consumer", "my-consumer", "0.1.0")
    register_corpus_under_node((), "my-corpus.md")
    load_corpus_tree()
    register_blueprint(
        "my-rules",
        create_blueprint_from_node(
            get_corpus_node("My Rules"), is_recursive=True
        ),
        consumer="my-consumer",
    )
    set_entry_consumer("my-consumer")
```

A skill-backing section needs `{description}` and `{when_to_use}` sidecars, see [sidecars](sidecar-doc.md).

## Building on kaye-library

[kaye-library](https://github.com/kami-lel/kaye-library) ships generic skills and glossaries, no persona. Each step has a library call; use all, some, or none, interleaved with your own:

| step | library call |
|---|---|
| 1 | `register_kaye_library_consumer()` |
| 2 | `register_kaye_library_abbr_glossaries()` |
| 3 | `get_kaye_library_abbrs_json_path()`, passed to `populate_abbr_data_with_json_file` |
| 4 | `register_kaye_library_dynamic_substitutions()` |
| 5 | `register_kaye_library_corpus()` |
| 6 | `register_kaye_library_blueprints()` |

Never call `setup_kaye_library_for_kaye_engine()` from a consumer: it is the library's own whole setup.

Rules:

- Names: a repeated substitution name or root node name raises
- Abbreviations: your file may repeat a library entry only to add a glossary or habit flag; `priority`, `wrap` and `remark` must not conflict, see [abbreviations](abbrs-doc.md)
- Contract: library skill names and node paths are stable; selecting them is safe

## Taking a Library Skill Over

Build the new blueprint over the library's blueprint *object*, never its name (that is a cycle), then register it with `override_exportable`. The skill keeps its name and flags and moves to your plugin. `commit-sense` and `coder` are made for this.

```python
from kaye_engine import override_exportable
from kaye_engine.prompt.blueprint import (
    create_blueprint,
    get_blueprint,
    replace_meta,
)

library_bp = get_blueprint("commit-sense").blueprint
meta = library_bp.meta
bp = replace_meta(
    create_blueprint(dependencies=[library_bp, "my-trailer-rules"]),
    display_name=meta.display_name,
    description_node=meta.description_node,
    when_to_use_node=meta.when_to_use_node,
)
override_exportable("commit-sense", bp, consumer="my-consumer")
```

## Running the CLI

```python
from kaye_engine.cli.cli_main import register_cli_main_parser

setup_my_consumer()
cli_parser, _ = register_cli_main_parser("my-consumer", "my-consumer")
parsed_args = cli_parser.parse_args()
parsed_args.func(parsed_args)
```

The `claude` and `hermes` subcommands also need `setup_claude_cli(...)` and `setup_hermes_cli(...)` as the last step; a missing one exits 1 and names what is absent. The library's standalone chat blueprints are not included when composing steps, so supply your own.
