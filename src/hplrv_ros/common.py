# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos

###############################################################################
# Imports
###############################################################################

from typing import Iterable, List, Union

from pathlib import Path

from hpl.ast import HplProperty, HplSpecification
from hpl.parser import property_parser, specification_parser

###############################################################################
# Constants
###############################################################################

ANY_PROP_LIST = Iterable[Union[str, HplProperty]]

ANY_SPEC = Union[str, Path, HplSpecification]
ANY_SPEC_LIST = Iterable[Union[str, Path, HplSpecification]]

###############################################################################
# Helper Functions
###############################################################################


def normalized_properties(properties: ANY_PROP_LIST) -> List[HplProperty]:
    parser = property_parser()
    return [p if isinstance(p, HplProperty) else parser.parse(p) for p in properties]


def properties_from_specs(specs: ANY_SPEC_LIST) -> List[HplProperty]:
    parser = specification_parser()
    properties: List[HplProperty] = []
    for spec in specs:
        if isinstance(spec, HplSpecification):
            properties.extend(spec.properties)
        else:
            path: Path = Path(spec).resolve(strict=True)
            text: str = path.read_text(encoding='utf8').strip()
            hpl_spec: HplSpecification = parser.parse(text)
            properties.extend(hpl_spec.properties)
    return properties
