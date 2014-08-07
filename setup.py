# -*- coding: utf-8 -*-
import os

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.rst')).read()
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='il2fb-mission-parser',
    version='1.0.0',
    description="Parse IL-2 FB mission file and produce detailed information "
                "about mission",
    long_description=README,
    keywords=[
        'il2', 'il-2', 'fb', 'forgotten battles', 'parser', 'mission',
    ],
    license='LGPLv3',
    url='https://github.com/IL2HorusTeam/il2fb-mission-parser',
    author='Alexander Oblovatniy, Alexander Kamyhin',
    author_email='oblovatniy@gmail.com, kamyhin@gmail.com',
    packages=[
        'il2fb.parsers.mission',
    ],
    namespace_packages=[
        'il2fb',
        'il2fb.parsers',
    ],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'License :: Free for non-commercial use',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries',
    ],
    platforms=[
        'any',
    ],
)
