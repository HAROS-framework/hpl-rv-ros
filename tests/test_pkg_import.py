# SPDX-License-Identifier: MIT
# Copyright © 2021 André Santos

###############################################################################
# Imports
###############################################################################

import bakeapy

###############################################################################
# Tests
###############################################################################


def test_import_was_ok():
    assert True


def test_pkg_has_version():
    assert hasattr(bakeapy, '__version__')
    assert isinstance(bakeapy.__version__, str)
    assert bakeapy.__version__ != ''
