# -*- coding: utf-8 -*-
"""
il2ds_mis_parser constants.
"""
from il2ds_mis_parser.helpers import _


# -----------------------------------------------------------------------------
# All section code
# -----------------------------------------------------------------------------

MAIN = "MAIN"
SEASON = "SEASON"
WEATHER = "WEATHER"
MDS = "MDS"
RESPAWN_TIME = "RespawnTime"
CHIEFS = "Chiefs"
CHIEF_ROAD = "Chief_Road"
N_STATIONARY = "NStationary"
BUILDINGS = "Buildings"
TARGET = "Target"
BORN_PLACE = "BornPlace"
BORN_PLACE_COUNTRIES = "BornPlaceCountries"
STATIC_CAMERA = "StaticCamera"
BRIDGE = "Bridge"
HOUSE = "House"
FRONT_MARKER = "FrontMarker"


# -----------------------------------------------------------------------------
# Section name and descriptions
# -----------------------------------------------------------------------------

SECTION = {
    MAIN: (_("Main"), _("Basic settings mission"),),
    SEASON: (_("Season"), _("Date mission"),),
    WEATHER: (_("Weather"), _("Weather conditions"),),
    MDS: None,
    RESPAWN_TIME: (_("Time respawn objects"), None,),
    CHIEFS: None,
    CHIEF_ROAD: None,
    N_STATIONARY: None,
    BUILDINGS: (_("Building"), None,),
    TARGET: (_("Target"), None,),
    BORN_PLACE: (_("Airfield"), None),
    BORN_PLACE_COUNTRIES: (_("Airfield country"), None),
    STATIC_CAMERA: (_("Static camera"), None,),
    BRIDGE : (_("Bridge"), None,),
    HOUSE: None,
    FRONT_MARKER: (_("Front line"), None,),
}