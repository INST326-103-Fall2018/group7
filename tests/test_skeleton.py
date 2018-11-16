#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from tweets2csv.skeleton import fib

__author__ = "Faiz Shah"
__copyright__ = "Faiz Shah"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
