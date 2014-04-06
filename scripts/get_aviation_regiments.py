# -*- coding: utf-8 -*-
"""
The return of the dictionary codes regiments.
"""

AIR_FORCES = {
    'r01': "rkka",
    'pl01': "poland",
    'fr01': "france",
    'gb01': "raf",
    'DU_NN': "holland",
    'RZ_NN': "rnzaf",
    'RA_NN': "raaf",
    'RN_NN': "royal_navy",
    'usa01': "usaaf",
    'UM_NN': "usmc",
    'UN_NN': "usn",
    'g01': "luftwaffe",
    'f01': "finland",
    'i01': "italy",
    'ro01': "romania",
    'sk01': "slovakia",
    'h01': "hungary",
    'ja01': "ija",
    'IN_NN': "ijn",
}


def get_army_aviation_regiments(file_path):
    """
    Aviation regiment grouped on the code of the army.
    The data comes from a file regiments.ini
    """
    regiments = {}
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('['):
                army_code = line.strip('[]')
                regiments.update({army_code: []})
            else:
                if line:
                    regiments[army_code].append(line)
    f.close()
    return regiments


def get_vvs_aviation_regiments(file_path):
    """
    Aviation regiment grouped on the code of the VVS.
    The data comes from a file regInfo.properties
    """
    regiments_vvs = {}
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line:
                if line.endswith('<none>'):
                    vvs_code = line.split()[0]
                    regiments_vvs.update({AIR_FORCES[vvs_code]: {}})
                else:
                    regiment = line.split()[0]
                    regiments_vvs[AIR_FORCES[vvs_code]][regiment] = line.lstrip(regiment).strip()
    f.close()
    return regiments_vvs
