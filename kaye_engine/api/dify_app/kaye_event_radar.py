"""
kaye_event_radar.py

define API to specific work with Dify App: Kaye Event Radar
"""

# pylint: disable=missing-function-docstring

from flask import Blueprint, abort

from kaye_engine import PROGRAM_NAME

# Blueprints  ##################################################################

# Flask Routing  ###############################################################

# /kaye/dify-app/kaye-event-radar
event_radar_bp = Blueprint(
    "kaye-event-radar", PROGRAM_NAME, url_prefix="/kaye-event-radar"
)


# /kaye/dify-app/kaye-event-radar/filter-events
@event_radar_bp.route("/filter-events", methods=["GET"])
def kaye_event_radar_filter():
    abort(501)


# /kaye/dify-app/kaye-event-radar/parse-events
@event_radar_bp.route("/parse-events", methods=["GET"])
def kaye_event_radar_parse():
    abort(501)
