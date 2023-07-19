# SPDX-License-Identifier: MIT
# Copyright © 2023 André Santos

###############################################################################
# Imports
###############################################################################

import hplrv_ros

###############################################################################
# Tests
###############################################################################


def test_import_was_ok():
    assert True


def test_pkg_has_version():
    assert hasattr(hplrv_ros, '__version__')
    assert isinstance(hplrv_ros.__version__, str)
    assert hplrv_ros.__version__ != ''
