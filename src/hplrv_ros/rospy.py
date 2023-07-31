# SPDX-License-Identifier: MIT
# Copyright © 2023 André Santos

###############################################################################
# Imports
###############################################################################

from typing import Any, Final, Iterable, List, Mapping, Type, Union

from hpl.ast import HplProperty, HplSpecification
from hpl.parser import property_parser, specification_parser
from hplrv.gen import MonitorGenerator, TemplateRenderer

from hplrv_ros.constants import ANY_PROP_SOURCE

###############################################################################
# Interface
###############################################################################


def generate_node(hpl_properties: ANY_PROP_SOURCE, topic_types: Mapping[str, str]) -> str:
    hpl_properties = _normalize_property_list(hpl_properties)
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
    return r.render_template('rospy.python.jinja', data)


###############################################################################
# Helper Functions
###############################################################################


def _normalize_property_list(source: ANY_PROP_SOURCE) -> List[HplProperty]:
    if isinstance(source, str):
        parser = specification_parser()
        spec: HplSpecification = parser.parse(source)
        return spec.properties
    if isinstance(source, HplSpecification):
        return source.properties
    properties = []
    parser = property_parser()
    for property in source:
        if not isinstance(property, HplProperty):
            property = parser.parse(property)
        properties.append(property)
    return properties
