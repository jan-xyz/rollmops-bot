#!/usr/bin/env python

from rollmops.rollmops_bot import Rollmops


def test_creating_a_rollmops():
    test_unit = Rollmops()
    assert isinstance(test_unit, Rollmops)
