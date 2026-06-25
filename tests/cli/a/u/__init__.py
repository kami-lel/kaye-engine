"""
shared expected-content constants for ``kaye claude user-system-prompt`` tests
"""

# section markers  #############################################################

INTRO = "# Introduction"
PERSONALITY = "# Personality"
LANGUAGE = "# Language"
STYLE_GUIDE = "# Style Guide"
STYLE_MARKDOWN = "## Style Guide Markdown Format"
LIST_FORMAT = "#### List Format"
MATH_FORMATTING = "#### Math Formatting"
DIAGRAMS = "#### Diagrams"
ROLE = "# Role"
ABBREVIATIONS = "# (Abbreviations)"
PEER_CODER = "# Kaye Peer Coder"
EMOTION_LINE = "- must use blockquote `>` for your emotions"
LANGUAGE_LINE = "- always respond in the **same language**"


# section groups  ##############################################################

# always present, regardless of flags (base + user scope)
BASE_CONTENT = [
    INTRO,
    STYLE_GUIDE,
    STYLE_MARKDOWN,
    LIST_FORMAT,
    MATH_FORMATTING,
    DIAGRAMS,
    ROLE,
    ABBREVIATIONS,
]

# persona markers, present unless --rapid drops them
PERSONA_CONTENT = [
    PERSONALITY,
    LANGUAGE,
    EMOTION_LINE,
    LANGUAGE_LINE,
]


# per-flag expected content  ###################################################

# default (Chat blueprint)
CHAT_CONTENT = BASE_CONTENT + PERSONA_CONTENT
CHAT_ABSENT = [PEER_CODER]

# -r (Rapid blueprint)
RAPID_CONTENT = BASE_CONTENT
RAPID_ABSENT = PERSONA_CONTENT + [PEER_CODER]

# -c (Chat + Kaye Peer Coder)
CODER_CONTENT = BASE_CONTENT + PERSONA_CONTENT + [PEER_CODER]

# -r -c (Rapid + Kaye Peer Coder)
RAPID_CODER_CONTENT = BASE_CONTENT + [PEER_CODER]
RAPID_CODER_ABSENT = PERSONA_CONTENT
