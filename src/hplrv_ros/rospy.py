# SPDX-License-Identifier: MIT
# Copyright © 2023 André Santos

###############################################################################
# Imports
###############################################################################

from collections.abc import Iterable, Mapping

from hpl.ast import HplProperty
from hplrv.gen import MonitorGenerator, TemplateRenderer

from hplrv_ros.common import ANY_SPEC_LIST, properties_from_specs

###############################################################################
# Interface
###############################################################################


def generate_node_from_specs(specs: ANY_SPEC_LIST, topic_types: Mapping[str, str]) -> str:
    properties: list[HplProperty] = properties_from_specs(specs)
    return generate_node(properties, topic_types)


def generate_node(hpl_properties: Iterable[HplProperty], topic_types: Mapping[str, str]) -> str:
    r = TemplateRenderer.from_pkg_data(pkg='hplrv_ros', template_dir='templates')
    gen = MonitorGenerator()
    data = gen.data_for_monitor_library(hpl_properties)
    topics = {}
    ros_imports = {'std_msgs'}
    for name in data['callbacks']:
        msg_type = topic_types[name]
        topics[name] = msg_type
        pkg = msg_type.split('/')[0]
        ros_imports.add(pkg)
    data = {
        'lib': gen.monitor_library(hpl_properties),
        'topics': topics,
        'ros_imports': ros_imports,
    }
    code: str = r.render_template('rospy.py.jinja', data)
    return code
