# -*- coding: utf-8 -*-

from six.moves import range


CYCLES_COUNT = 10 ** 5


def generate_cheifs_lines():
    for i in range(0, CYCLES_COUNT, 4):
        yield "{0}_Chief Armor.1-BT7 2".format(i)
        yield "{0}_Chief Vehicles.GAZ67 1".format(i + 1)
        yield "{0}_Chief Trains.USSR_FuelTrain/AA 1".format(i + 2)
        yield "{0}_Chief Ships.G5 1 60 3 2.0".format(i + 3)


def generate_cheif_road_lines():
    # Simulate all route points are created manually
    for i in range(CYCLES_COUNT - 1):
        yield "{0}.00 {0}.00 120.00 0 2 3.055555582046509".format(i)
    # Despite last point is always created manually, it has reduced format
    i += 1
    yield "{0}.00 {0}.00 120.00".format(i)


def generate_nstationary_lines():
    for i in range(0, CYCLES_COUNT, 7):
        yield "{0}_Static vehicles.aeronautics.Aeronautics$BarrageBalloon_2400m 1 {0}.00 {0}.00 360.00 0.0".format(i)
        yield "{0}_Static vehicles.artillery.Artillery$SdKfz251 2 {0}.00 {0}.00 360.00 0.0 0 1 1".format(i)
        yield "{0}_Static vehicles.lights.Searchlight$SL_ManualBlue 1 {0}.00 {0}.00 360.00 0.0".format(i)
        yield "{0}_Static vehicles.planes.Plane$I_16TYPE24 1 {0}.00 {0}.00 360.00 0.0 null 2 1.0 I-16type24_G1_RoW3.bmp 1".format(i)
        yield "{0}_Static vehicles.radios.Beacon$RadioBeacon 2 {0}.00 {0}.00 360.00 0.0".format(i)
        yield "{0}_Static vehicles.stationary.Stationary$Wagon1 1 {0}.00 {0}.00 360.00 0.0".format(i)
        yield "{0}_Static ships.Ship$G5 1 {0}.00 {0}.00 360.00 0.0 60 3 1.4".format(i)


def generate_buildings_lines():
    for i in range(CYCLES_COUNT):
        yield "{0}_bld House$Tent_Pyramid_US 1 {0}.00 {0}.00 360.00".format(i)


def generate_target_lines():
    for __ in range(0, CYCLES_COUNT, 9):
        yield "0 0 0 0 500 90939 91871 0 1 10_Chief 91100 91500"
        yield "1 1 1 60 750 133960 87552 1350"
        yield "2 2 1 30 500 135786 84596 0 0  Bridge84 135764 84636"
        yield "3 1 1 50 500 133978 87574 1150"
        yield "3 0 1 40 501 134459 85239 300 0 1_Chief 134360 85346"
        yield "4 0 1 10 750 134183 85468 0 1 r0100 133993 85287"
        yield "5 1 1 20 250 132865 87291 0 1 1_Chief 132866 86905"
        yield "6 1 1 30 500 134064 88188 1350"
        yield "7 2 1 30 500 135896 84536 0 0  Bridge84 135764 84636"


def generate_born_place_lines():
    for i in range(CYCLES_COUNT):
        yield "1 3000 {0} {0} 1 1000 200 0 0 0 5000 50 0 1 1 0 0 3.8 1 0 0 0 0".format(i)


def generate_static_camera_lines():
    for i in range(CYCLES_COUNT):
        yield "{0} {0} 35 1".format(i)


def generate_front_marker_lines():
    for i in range(CYCLES_COUNT):
        yield "FrontMarker{0} {0}.00 {0}.00 1".format(i)


def generate_rocket_lines():
    for i in range(CYCLES_COUNT):
        yield "{0}_Rocket Fi103_V1_ramp 2 {0}.00 {0}.00 360.00 60.0 10 80.0 {0}.00 {0}.00".format(i)


def generate_wing_route_lines():
    for i in range(0, CYCLES_COUNT, 7):
        yield "TAKEOFF {0}.00 {0}.00 0 0 &0".format(i)
        yield "TRIGGERS 0 10 20 0"
        yield "NORMFLY_401 {0}.00 {0}.00 500.00 300.00 &0 F2".format(i)
        yield "TRIGGERS 1 1 25 5 500"
        yield "NORMFLY {0}.00 {0}.00 500.00 300.00 r0100 1 &0".format(i)
        yield "GATTACK {0}.00 {0}.00 500.00 300.00 0_Chief 0 &0".format(i)
        yield "LANDING_104 {0}.00 {0}.00 0 0 &1".format(i)
