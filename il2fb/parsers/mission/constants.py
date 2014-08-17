# -*- coding: utf-8 -*-
"""
Different constants.
"""
from il2fb.parsers.mission.helpers import _


###############################################################################
# Targets
###############################################################################

# Target types ----------------------------------------------------------------
TARGET_TYPE_DESTROY_CODE = '0'
TARGET_TYPE_DESTROY_AREA_CODE = '1'
TARGET_TYPE_DESTROY_BRIDGE_CODE = '2'
TARGET_TYPE_RECON_CODE = '3'
TARGET_TYPE_ESCORT_CODE = '4'
TARGET_TYPE_COVER_CODE = '5'
TARGET_TYPE_COVER_AREA_CODE = '6'
TARGET_TYPE_COVER_BRIDGE_CODE = '7'

TARGET_TYPE_DESTROY = 'destroy'
TARGET_TYPE_DESTROY_AREA = 'destroy_area'
TARGET_TYPE_DESTROY_BRIDGE = 'destroy_bridge'
TARGET_TYPE_RECON = 'recon'
TARGET_TYPE_ESCORT = 'escort'
TARGET_TYPE_COVER = 'cover'
TARGET_TYPE_COVER_AREA = 'cover_area'
TARGET_TYPE_COVER_BRIDGE = 'cover_bridge'

TARGET_TYPES_NAMES = {
    TARGET_TYPE_DESTROY: _("destroy"),
    TARGET_TYPE_DESTROY_BRIDGE: _("destroy bridge"),
    TARGET_TYPE_DESTROY_AREA: _("destroy area"),
    TARGET_TYPE_RECON: _("recon"),
    TARGET_TYPE_ESCORT: _("escort"),
    TARGET_TYPE_COVER: _("cover"),
    TARGET_TYPE_COVER_AREA: _("cover area"),
    TARGET_TYPE_COVER_BRIDGE: _("cover bridge"),
}

TARGET_TYPES_MAP = {
    TARGET_TYPE_DESTROY_CODE: TARGET_TYPE_DESTROY,
    TARGET_TYPE_DESTROY_BRIDGE_CODE: TARGET_TYPE_DESTROY_BRIDGE,
    TARGET_TYPE_DESTROY_AREA_CODE: TARGET_TYPE_DESTROY_AREA,
    TARGET_TYPE_RECON_CODE: TARGET_TYPE_RECON,
    TARGET_TYPE_ESCORT_CODE: TARGET_TYPE_ESCORT,
    TARGET_TYPE_COVER_CODE: TARGET_TYPE_COVER,
    TARGET_TYPE_COVER_AREA_CODE: TARGET_TYPE_COVER_AREA,
    TARGET_TYPE_COVER_BRIDGE_CODE: TARGET_TYPE_COVER_BRIDGE,
}

# Target priorities -----------------------------------------------------------
TARGET_PRIORITY_PRIMARY = 'primary'
TARGET_PRIORITY_SECONDARY = 'secondary'
TARGET_PRIORITY_HIDDEN = 'hidden'

TARGET_PRIORITIES = {
    TARGET_PRIORITY_PRIMARY: _("primary"),
    TARGET_PRIORITY_SECONDARY: _("secondary"),
    TARGET_PRIORITY_HIDDEN: _("hidden"),
}

TARGET_PRIORITIES_MAP = {
    '0': TARGET_PRIORITY_PRIMARY,
    '1': TARGET_PRIORITY_SECONDARY,
    '2': TARGET_PRIORITY_HIDDEN,
}

###############################################################################
# Flight_Way
###############################################################################

# Way points ----------------------------------------------------------------

WAY_POINT_TYPES = {
    'TAKEOFF': {
        'type': "takeoff_normal",
    },
    'TAKEOFF_002': {
        'type': "takeoff_pair",
    },
    'TAKEOFF_003': {
        'type': "takeoff_in_line",
    },
    'TAKEOFF_004': {
        'type': "taxiing",
    },
    'NORMFLY': {
        'type': 'normal',
    },
    'NORMFLY_401': {
        'type': 'patrol',
        'patrol_type': 'triangle',
    },
    'NORMFLY_402': {
        'type': 'patrol',
        'patrol_type': 'square',
    },
    'NORMFLY_403': {
        'type': 'patrol',
        'patrol_type': 'pentagon',
    },
    'NORMFLY_404': {
        'type': 'patrol',
        'patrol_type': 'hexagon',
    },
    'NORMFLY_405': {
        'type': 'patrol',
        'patrol_type': 'random',
    },
    'GATTACK': {
        'type': 'attack',
    },
    'LANDING': {
        'type': 'landing_on_left',
    },
    'LANDING_101': {
        'type': 'landing_on_right',
    },
    'LANDING_102': {
        'type': 'landing_short_on_left',
    },
    'LANDING_103': {
        'type': 'landing_short_on_right',
    },
    'LANDING_104': {
        'type': 'landing_straight',
    },
}

WAY_POINT_FORMATIONS = {
    'F1': 'echelon_right',
    'F2': 'echelon_left',
    'F3': 'rank',
    'F4': 'line_abreast',
    'F5': 'line_asteam',
    'F6': 'vic',
    'F7': 'finger_four',
    'F8': 'diamond',
}
