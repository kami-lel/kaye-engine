"""
shared expected-content constants for ``kaye claude user-system-prompt`` tests
"""

# Fixme update with better organizations

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
COMMENTARY_CASE = "### Commentary Case"
EMOTION_LINE = "- must use blockquote `>` for your emotions"
LANGUAGE_LINE = "- always respond in the **same language**"


# section groups  ##############################################################

# always present, regardless of flags
BASE_CONTENT = [
    INTRO,
    STYLE_GUIDE,
    STYLE_MARKDOWN,
    LIST_FORMAT,
    MATH_FORMATTING,
    DIAGRAMS,
]

# persona + chat-style markers, present unless --rapid drops them
PERSONA_CONTENT = [
    PERSONALITY,
    LANGUAGE,
    COMMENTARY_CASE,
    EMOTION_LINE,
    LANGUAGE_LINE,
]

# user-scope nodes (Role/Abbreviations) are injected by Dify API only;
# the CLI user-system-prompt command does not include them
USER_SCOPE = [ROLE, ABBREVIATIONS]


# per-flag expected content  ###################################################

# default (Chat blueprint)
CHAT_CONTENT = BASE_CONTENT + PERSONA_CONTENT
CHAT_ABSENT = [PEER_CODER] + USER_SCOPE

# -r (Rapid blueprint)
RAPID_CONTENT = BASE_CONTENT
RAPID_ABSENT = PERSONA_CONTENT + [PEER_CODER] + USER_SCOPE

# -c (Chat + Kaye Peer Coder)
CODER_CONTENT = BASE_CONTENT + PERSONA_CONTENT + [PEER_CODER]
CODER_ABSENT = USER_SCOPE

# -r -c (Rapid + Kaye Peer Coder)
RAPID_CODER_CONTENT = BASE_CONTENT + [PEER_CODER]
RAPID_CODER_ABSENT = PERSONA_CONTENT + USER_SCOPE
