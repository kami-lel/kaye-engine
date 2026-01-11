# Kaye Python API documentation

## `gen_prompt` module

The **core** module of *Kaye Python API*,
implement a systematic, dynamic, and structured framework
for **prompt management and manipulation**.













### Prompt Node `PromptCorpusNode`

<!-- TODO -->

The **prompt corpus** comprises the complete set of available prompts.

The class ``PromptCorpusNode`` serves as a tree-structured representation of
the prompt corpus, enabling hierarchical organization and efficient traversal.

Q.v. [anytree Documentation](https://anytree.readthedocs.io/en/stable/)













### Prompt Blueprint `PromptBlueprint`


A **prompt blueprint** defines a specific subset of the prompt corpus.

The ``PromptBlueprint`` class encapsulates prompt blueprint structure.













### loaders

The supporting function ``load_embedded_prompt_corpus()`` loads
the *embedded* prompt corpus (``kaye/gen_prompt/prompt_corpus.md``)
from the filesystem at runtime.

The supporting function ``load_embedded_prompt_blueprint(prompt_blueprint_name)``
retrieves and loads a selected *embedded* blueprint stored in
``kaye/gen_prompt/prompt_blueprints/`` at runtime.

<!-- TODO write Python API documentation -->