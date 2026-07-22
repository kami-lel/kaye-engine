# pylint: disable=missing-module-docstring

# output keys  #################################################################

OUTPUT_OPT_OBJ = "opt_obj"


# constants  ###################################################################

FALLBACK_SIGIL = "*"
BALANCE_TOLERANCE = 0.2

SIGIL_ADD_LONG = "+"
SIGIL_DEL_LONG = "-"
SIGIL_BALANCED_LONG = "*"
SIGIL_ADD_SHORT = "/"
SIGIL_DEL_SHORT = "\\"
SIGIL_BALANCED_SHORT = "|"


# auxiliaries  ##################################################################
def is_balanced(added: int, deleted: int) -> bool:
    largest = max(added, deleted, 1)
    return abs(added - deleted) <= BALANCE_TOLERANCE * largest


def resolve_ordinary_sigil(
    per_file_diff: str, LONG_SHORT_THRESHOLD: float
) -> str:
    added = 0
    deleted = 0

    for line in per_file_diff.split("\n"):
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            added += 1
        elif line.startswith("-"):
            deleted += 1

    is_long = per_file_diff.count("\n") > LONG_SHORT_THRESHOLD

    if is_balanced(added, deleted):
        return SIGIL_BALANCED_LONG if is_long else SIGIL_BALANCED_SHORT
    if added > deleted:
        return SIGIL_ADD_LONG if is_long else SIGIL_ADD_SHORT
    return SIGIL_DEL_LONG if is_long else SIGIL_DEL_SHORT


# Entry Point  #################################################################
def main(LONG_SHORT_THRESHOLD: float, per_file_diff: str, llm_message: str):
    sigil, _, summary = llm_message.strip("\n").partition("\n")
    sigil = sigil.strip()
    summary = summary.strip()

    if sigil == FALLBACK_SIGIL:
        sigil = resolve_ordinary_sigil(per_file_diff, LONG_SHORT_THRESHOLD)

    opt_obj = {"symbol": sigil, "summary": summary}

    return {OUTPUT_OPT_OBJ: opt_obj}
