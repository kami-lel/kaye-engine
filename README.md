# kaye README

> Consistent AI agent persona **Kaye**, powered by rigorous prompt engineering













## Core Concepts

### Prompt Corpus

The [Prompt Corpus](kaye/prompt_corpus.md) is the center concept, a **Single, Structured Markdown**
 holding instructions, rules, styles, roles, and references
it defines who **Kaye** is, and this project focuses on tools to **generate
scenario-ready prompts** from it via blueprints, the *gen_prompt* module, and a
lightweight *CLI* so outputs stay consistent across contexts

single **Source Of Truth** in *prompt_corpus.md* defining persona, roles, rules

----

- role: task-specific **Behavior Profile** inside the corpus shaping response
  style, scope
- prompt: final **Rendered Text** tailored to context, ready for direct use
- blueprint: tree **Selection Spec** controlling which corpus parts render













## Python API

- Python module API: programmatic **API** to list, preview,
  generate













## HTTP API













## Python CLI

- CLI: command-line **CLI** via *python -m kaye* to list, show, generate fast

<!-- TODO: introduce: corpus, python api, http api, cli, dify apps -->