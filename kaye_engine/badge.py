"""
badge.py

define the native ``kamilog`` badge names the engine stamps on log lines;
a leaf module, so any command or logger user can import it without a cycle
"""

__all__ = (
    "DEL_BADGE",
    "DRY_BADGE",
    "MV_BADGE",
    "NEW_BADGE",
    "OWR_BADGE",
)

# constants  ###################################################################
# run mode: only report, write nothing
DRY_BADGE = "dry"

# data: a line creates, overwrites, moves, or deletes something
NEW_BADGE = "new"
OWR_BADGE = "owr"
MV_BADGE = "mv"
DEL_BADGE = "del"
