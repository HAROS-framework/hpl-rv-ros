# SPDX-License-Identifier: MIT
# Copyright © 2023 André Santos

###############################################################################
# Imports
###############################################################################

from pathlib import Path
from setuptools import find_packages, setup

###############################################################################
# Constants
###############################################################################

PROJECT = 'hpl-rv-ros'
PYTHON_PKG = 'hplrv_ros'
HERE = Path(__file__).parent

###############################################################################
# Utility
###############################################################################


def read(filename):
    # Utility function to read the README, etc..
    # Used for the long_description and other fields.
    return (HERE / filename).read_text(encoding='utf-8')


###############################################################################
# Setup
###############################################################################


setup(
    name=PROJECT,
    use_scm_version={
        'version_scheme': 'no-guess-dev',
        'local_scheme': 'dirty-tag',
        'fallback_version': '0.1.0',
    },
    description='Runtime Verification tools for ROS systems',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url=f'https://github.com/HAROS-framework/{PROJECT}',
    author='André Santos',
    author_email='haros.framework@gmail.com',
    license='MIT',
    keywords='ros, runtime verification, runtime monitoring, code generation',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={},  # {PYTHON_PKG: ['dir/*.file']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Quality Assurance',
    ],
    entry_points={
        'console_scripts': [f'{PROJECT}={PYTHON_PKG}.cli:main'],
    },
    python_requires='>=3.8, <4',
    install_requires=[
        'hpl-rv>=1.0.0',
        'hpl-specs<2.0.0',
        'Jinja2>=3.1.0',
        'ruamel.yaml>=0.17.0',
    ],
    extras_require={
        'dev': ['pytest', 'tox'],
    },
    zip_safe=False,
    project_urls={
        'Source': f'https://github.com/HAROS-framework/{PROJECT}/',
        'Tracker': f'https://github.com/HAROS-framework/{PROJECT}/issues',
        # 'Say Thanks!': 'http://saythanks.io/to/haros-framework',
    },
)
