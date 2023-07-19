# SPDX-License-Identifier: MIT
# Copyright © 2023 André Santos

###############################################################################
# Imports
###############################################################################

from typing import Any, Final, Iterable, List, Mapping, Type, Union

from hpl.ast import HplProperty, HplSpecification
from hpl.parser import property_parser, specification_parser
from hplrv.gen import MonitorGenerator, TemplateRenderer

###############################################################################
# Constants
###############################################################################

ANY_PROP: Final[Type] = Union[str, HplProperty]
ANY_PROP_LIST: Final[Type] = Iterable[ANY_PROP]
ANY_PROP_SOURCE: Final[Type] = Union[str, HplSpecification, ANY_PROP_LIST]

###############################################################################
# Interface
###############################################################################


def render_node(hpl_properties: ANY_PROP_SOURCE, topic_types: Mapping[str, str]) -> str:
    hpl_properties = _normalize_property_list(hpl_properties)
    r = TemplateRenderer.from_pkg_data(pkg='hplrv_ros', template_dir='templates')
    gen = MonitorGenerator()
    data = gen.data_for_monitor_library(hpl_properties)
    topics = {}
    ros_imports = {'std_msgs'}
    for name in data['callbacks']:
        msg_type = topic_types[name]
        topics[name] = msg_type
        pkg, _msg = msg_type.split('/')
        ros_imports.add(pkg)
    data['topics'] = topics
    data['ros_imports'] = ros_imports
    return r.render('rospy.python.jinja', data)



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
