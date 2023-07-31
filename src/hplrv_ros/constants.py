# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos

###############################################################################
# Constants
###############################################################################

ANY_PROP: Final[Type] = Union[str, HplProperty]
ANY_PROP_LIST: Final[Type] = Iterable[ANY_PROP]
ANY_PROP_SOURCE: Final[Type] = Union[str, HplSpecification, ANY_PROP_LIST]
