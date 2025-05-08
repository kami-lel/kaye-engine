"""
This module provides a systematic, dynamic, and structured approach to
generating system prompt text.
It enables users to create either a complete prompt or a selected **subset**
of a prompt from a full prompt definition.

A **Full Prompt Tree**—implemented as the `FullPromptParserNode` class in
`full_prompt_parser.py`—is a tree-structured representation of the full prompt.

The helper function `load_current_full_prompt_tree` (from
`full_prompt_tree_loader.py`) loads the full prompt tree from the file
`kaye/gen_prompt/prompt_full.md` at runtime.

A **Prompt Template**—implemented as the `PromptTemplate` class in
`prompt_template.py`—can represent either the entire prompt tree
or a specific subset.

The function `load_prompt_template(prompt_name)` loads the full prompt tree from
`kaye/gen_prompt/prompt_full.md` and constructs a predefined prompt template
specified in `kaye/gen_prompt/prompt_templates/` at runtime.
"""

# todo include version in generated prompt

from .full_prompt_parser import *
from .full_prompt_tree_loader import *
from .prompt_template import *
from .prompt_template_loader import *

# FIXME refactor full prompt tree to prompt corpus
# FIXME refactor prompt template to blueprint
# TODO better docstrings, etc.
