# -*- coding: utf-8 -*-
"""
Different constants.
"""

################################################################################
# Flight Way
################################################################################

# Way points -------------------------------------------------------------------

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
