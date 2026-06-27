"""
Kaye Programmatic API: Prompt Generation

The **core** module of *Kaye Python API*,
implement a systematic, dynamic, and structured framework
for **prompt management and manipulation**.
"""

# constants  ###################################################################

REPLACEMENT_NEWLINE_SYMBOL = "↵"

# imports  #####################################################################

from .base_prompt_node import *
from .prompt_corpus_node import *
from .prompt_corpus_loader import *
from .prompt_blueprint import *
from .prompt_blueprint_loader import *
from .abbr_nodes import *
from .today_node import *
from .embedded_blueprints import *
