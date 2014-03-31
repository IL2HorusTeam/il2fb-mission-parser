# -*- coding: utf-8 -*-
"""
Application constants.
"""

# -----------------------------------------------------------------------------
# Target types
# -----------------------------------------------------------------------------

TARGET_TYPE_DESTROY = '0'
TARGET_TYPE_DESTROY_BRIDGE = '1'
TARGET_TYPE_DESTROY_AREA = '2'
TARGET_TYPE_RECON = '3'
TARGET_TYPE_ESCORT = '4'
TARGET_TYPE_COVER = '5'
TARGET_TYPE_COVER_AREA = '6'
TARGET_TYPE_COVER_BRIDGE = '7'

TARGET_TYPES = {
    TARGET_TYPE_DESTROY: 'destroy',
    TARGET_TYPE_DESTROY_BRIDGE: 'destroy_bridge',
    TARGET_TYPE_DESTROY_AREA: 'destroy_area',
    TARGET_TYPE_RECON: 'recon',
    TARGET_TYPE_ESCORT: 'escort',
    TARGET_TYPE_COVER: 'cover',
    TARGET_TYPE_COVER_AREA: 'cover_area',
    TARGET_TYPE_COVER_BRIDGE: 'cover_bridge',
}

# -----------------------------------------------------------------------------
# Target priorities
# -----------------------------------------------------------------------------

TARGET_PRIORITIES = {
    '0': 'main',
    '1': 'extra',
    '2': 'hidden',
}

# -----------------------------------------------------------------------------
# Weather types
# -----------------------------------------------------------------------------

CLOUDLESS = '0'
CLEAR_WEATHER = '1'
HAZE = '2'
LIGHT_FOG = '3'
FOG = '4'
RAIN_OR_SNOW = '5'
THUNDERSTORM = '6'

WEATHER_TYPES = {
    CLOUDLESS: 'cloudless',
    CLEAR_WEATHER: 'clear_weather',
    HAZE: 'haze',
    LIGHT_FOG: 'light_fog',
    FOG: 'fog',
    RAIN_OR_SNOW: 'rain or snow',
    THUNDERSTORM: 'thunderstorm',
}