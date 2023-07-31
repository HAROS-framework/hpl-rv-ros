# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos

"""
Module that contains the command line program.

Why does this file exist, and why not put this in __main__?

  In some cases, it is possible to import `__main__.py` twice.
  This approach avoids that. Also see:
  https://click.palletsprojects.com/en/5.x/setuptools/#setuptools-integration

Some of the structure of this file came from this StackExchange question:
  https://softwareengineering.stackexchange.com/q/418600
"""

###############################################################################
# Imports
###############################################################################

from typing import Any, Dict, Final, Iterable, List, Optional

import argparse
from pathlib import Path
import sys
from traceback import print_exc

from hpl.ast import HplProperty, HplSpecification
from hpl.parser import specification_parser
from hplrv.gen import lib_from_files, lib_from_properties, TemplateRenderer

from hplrv_ros import __version__ as current_version
from hplrv_ros.constants import ANY_PROP_LIST
from hplrv_ros.rospy import generate_node as generate_rospy

###############################################################################
# Constants
###############################################################################

PROG: Final[str] = 'hpl-rv-ros'

###############################################################################
# Argument Parsing
###############################################################################


def parse_arguments(argv: Optional[List[str]]) -> Dict[str, Any]:
    description = 'Tools to enable HPL Runtime Verification for ROS applications.'
    parser = argparse.ArgumentParser(prog=PROG, description=description)

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'{PROG} {current_version}',
        help='prints the program version',
    )

    parser.add_argument(
        '--rospy',
        action='store_true',
        help='use a ROS1 node template (default: ROS2)',
    )

    parser.add_argument(
        '-f',
        '--files',
        action='store_true',
        help='process args as HPL files (default: HPL properties)',
    )

    parser.add_argument('-o', '--output', help='output file to place generated code')

    parser.add_argument('args', nargs='+', help='input properties')

    args = parser.parse_args(args=argv)
    return vars(args)


###############################################################################
# Setup
###############################################################################


def load_configs(args: Dict[str, Any]) -> Dict[str, Any]:
    try:
        config: Dict[str, Any] = {}
        # with open(args['config_path'], 'r') as file_pointer:
        # yaml.safe_load(file_pointer)

        # arrange and check configs here

        return config
    except Exception as err:
        # log or raise errors
        print(err, file=sys.stderr)
        if str(err) == 'Really Bad':
            raise err

        # Optional: return some sane fallback defaults.
        sane_defaults: Dict[str, Any] = {}
        return sane_defaults


###############################################################################
# Helper Functions
###############################################################################


def _property_list_from_files(sources: Iterable[str]) -> List[HplProperty]:
    properties = []
    parser = specification_parser()
    for source in sources:
        path: Path = Path(source).resolve(strict=True)
        text: str = path.read_text(encoding='utf-8').strip()
        spec: HplSpecification = parser.parse(text)
        properties.extend(spec.properties)
    return properties


###############################################################################
# Commands
###############################################################################


def generate_ros_node(args: Dict[str, Any], _configs: Dict[str, Any]) -> int:
    properties: ANY_PROP_LIST = args['args']
    if args.get('files'):
        properties = _property_list_from_files(properties)
    output: str = generate_rospy(properties, topic_types)
    output: str = lib_from_properties(properties)

    renderer = TemplateRenderer.from_pkg_data(pkg='hplrv_ros')
    data = { 'lib': output }
    if args.get('rospy'):
        output = renderer.render_template('rospy.python.jinja', data)
    else:
        output = renderer.render_template('rclpy.python.jinja', data)

    input_path: str = args.get('output')
    if input_path:
        path: Path = Path(input_path).resolve(strict=False)
        path.write_text(output, encoding='utf-8')
    else:
        print(output)
    return 0


###############################################################################
# Entry Point
###############################################################################


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_arguments(argv)

    try:
        # Load additional config files here, e.g., from a path given via args.
        # Alternatively, set sane defaults if configuration is missing.
        config = load_configs(args)
        return generate_ros_node(args, config)

    except KeyboardInterrupt:
        print('Aborted manually.', file=sys.stderr)
        return 1

    except Exception as err:
        print('An unhandled exception crashed the application!')
        print(err)
        print_exc()
        return 1
