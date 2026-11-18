"""
badge.py

define the native ``kamilog`` badge names the engine stamps on log lines;
a leaf module, so any command or logger user can import it without a cycle
"""

__all__ = (
    "CP_BADGE",
    "DEL_BADGE",
    "DRY_BADGE",
    "MV_BADGE",
    "NEW_BADGE",
    "OWR_BADGE",
    "TMP_BADGE",
)

# constants  ###################################################################
# run mode: only report, write nothing
DRY_BADGE = "dry"

# data: a line creates, overwrites, moves, copies, or deletes something
NEW_BADGE = "new"
OWR_BADGE = "owr"
MV_BADGE = "mv"
CP_BADGE = "cp"
DEL_BADGE = "del"

# data: a line writes scratch data, discarded once the run or block ends
TMP_BADGE = "tmp"
