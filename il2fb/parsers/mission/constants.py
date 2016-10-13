# coding: utf-8

#: Flag which indicates whether stationary aircraft is restorable in case it
#: can be used for spawning.
IS_STATIONARY_AIRCRAFT_RESTORABLE = '2'

#: Flag for empty values.
NULL = 'null'

#: Flag which indicates new line with continuation of weapon limitations.
WEAPONS_CONTINUATION_MARK = '+'

#: Flag which indicates new line with extra parameters for flight route points.
ROUTE_POINT_EXTRA_PARAMETERS_MARK = 'TRIGGERS'

#: Flag which indicates whether radio silence is disabled for a given route
#: point of flight.
ROUTE_POINT_RADIO_SILENCE_OFF = '&0'

#: Flag which indicates whether radio silence is enabled for a given route
#: point of flight.
ROUTE_POINT_RADIO_SILENCE_ON = '&1'

#: Enumeration of flags which indicate beginning of a comment.
COMMENT_MARKERS = (';', '#', '//', '--', )

#: Multiplication coefficient which is used to convert speed of moving ground
#: units into km/h.
CHIEF_SPEED_COEFFICIENT = 3.6
