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

WEATHER_CLOUDLESS = '0'
WEATHER_CLEAR = '1'
WEATHER_HAZE = '2'
WEATHER_SLIGHT_FOG = '3'
WEATHER_FOG = '4'
WEATHER_RAIN_OR_SNOW = '5'
WEATHER_THUNDERSTORM = '6'

WEATHER_TYPES = {
    WEATHER_CLOUDLESS: 'cloudless',
    WEATHER_CLEAR: 'clear',
    WEATHER_HAZE: 'haze',
    WEATHER_SLIGHT_FOG: 'slight_fog',
    WEATHER_FOG: 'fog',
    WEATHER_RAIN_OR_SNOW: 'rain_or_snow',
    WEATHER_THUNDERSTORM: 'thunderstorm',
}

# -----------------------------------------------------------------------------
# Stationary types
# -----------------------------------------------------------------------------

STATIONARY_TYPE = 'stationary'
STATIONARY_TYPE_ARTILLERY = 'artillery'
STATIONARY_TYPE_PLANES = 'planes'
STATIONARY_TYPE_RADIOS = 'radios'

SKILLS = {
    0: 'cadet',
    1: 'rookie',
    2: 'veteran',
    3: 'ace',
}