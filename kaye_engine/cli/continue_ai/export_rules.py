"""
export_rules.py

define ``classify_exportable``
"""

_KIND_RULE = "rule"
_KIND_PROMPT = "prompt"

# classification  ##############################################################

def classify_exportable(exportable):
    """
    decide how an entry lands in a Continue folder

    ``always_apply`` forces a rule; otherwise an LLM-invokable entry is a
    rule, a merely user-invokable one is a prompt, and the rest is skipped

    :param exportable: entry to classify
    :type exportable: Exportable
    :return: ``"rule"``, ``"prompt"``, or ``None`` when skipped
    :rtype: str or None
    """
    if exportable.always_apply or exportable.llm_invokable:
        return _KIND_RULE
    if exportable.is_user_invokable:
        return _KIND_PROMPT
    return None

