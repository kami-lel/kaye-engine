"""
This module implements a systematic, dynamic, and structured framework for
prompt management and manipulation.

The **prompt corpus** comprises the complete set of available prompts.

The class ``PromptCorpusNode`` serves as a tree-structured representation of
the prompt corpus, enabling hierarchical organization and efficient traversal.

The supporting function ``load_embedded_prompt_corpus()`` loads
the *embedded* prompt corpus (``kaye/gen_prompt/prompt_corpus.md``)
from the filesystem at runtime.

----

A **prompt blueprint** defines a specific subset the prompt corpus.

The ``PromptBlueprint`` class encapsulates prompt blueprint structure.

The supporting function ``load_prompt_blueprint(prompt_blueprint_name)``
retrieves and loads a selected *embedded* blueprint stored in
``kaye/gen_prompt/prompt_blueprints/`` at runtime.
"""

# todo include version in generated prompt

from .prompt_corpus_node import *
from .prompt_corpus_loader import *
from .prompt_blueprint import *
from .prompt_blueprint_loader import *

# FIXME refactor prompt template to blueprint
