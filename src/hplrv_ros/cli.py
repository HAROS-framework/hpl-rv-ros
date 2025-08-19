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

from typing import Any, Final

import argparse
from pathlib import Path
import sys
from traceback import print_exc

from hpl.ast import HplProperty
from ruamel.yaml import YAML

from hplrv_ros import __version__ as current_version
from hplrv_ros.common import normalized_properties, properties_from_specs
from hplrv_ros.rclpy import generate_node as generate_rclpy
from hplrv_ros.rospy import generate_node as generate_rospy

###############################################################################
# Constants
###############################################################################

PROG: Final[str] = 'hpl-rv-ros'

###############################################################################
# Argument Parsing
###############################################################################


def parse_arguments(argv: list[str] | None) -> dict[str, Any]:
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

    parser.add_argument(
        'topics',
        type=Path,
        help='path to a YAML/JSON file with types for each topic',
    )

    parser.add_argument('specs', nargs='+', help='input properties')

    args = parser.parse_args(args=argv)
    return vars(args)


###############################################################################
# Setup
###############################################################################


def load_configs(args: dict[str, Any]) -> dict[str, Any]:
    try:
        config: dict[str, Any] = {}
        # yaml = YAML(typ='safe')
        # config = yaml.load(args['config_path'])

        # arrange and check configs here

        return config
    except Exception as err:
        # log or raise errors
        print(err, file=sys.stderr)
        raise err

        # Optional: return some sane fallback defaults.
        # sane_defaults: Dict[str, Any] = {}
        # return sane_defaults


###############################################################################
# Commands
###############################################################################


def generate_ros_node(args: dict[str, Any], _configs: dict[str, Any]) -> int:
    yaml = YAML(typ='safe')
    topic_types: dict[str, str] = yaml.load(args['topics'])

    if args.get('files'):
        properties: list[HplProperty] = properties_from_specs(args['specs'])
    else:
        properties = normalized_properties(args['specs'])

    if args.get('rospy'):
        output: str = generate_rospy(properties, topic_types)
    else:
        output = generate_rclpy(properties, topic_types)

    output_path: str | None = args.get('output')
    if output_path:
        path: Path = Path(output_path).resolve(strict=False)
        path.write_text(output, encoding='utf-8')
    else:
        print(output)

    return 0


###############################################################################
# Entry Point
###############################################################################


def main(argv: list[str] | None = None) -> int:
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
