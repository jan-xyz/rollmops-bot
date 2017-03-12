#!/usr/bin/env python

from rollmops.rollmops_bot import Rollmops


def test_creating_a_bot():
    test_unit = Rollmops()
    assert isinstance(test_unit, Rollmops)


def test_setting_datahandler(bot, datahandler):
    test_unit = bot
    test_datahandler = datahandler
    test_unit.set_datahandler(test_datahandler)
    actual_datahandler = test_unit.get_datahandler()
    assert test_datahandler == actual_datahandler


def test_setting_ui(bot, ui):
    test_unit = bot
    test_ui = ui
    test_unit.set_ui(test_ui)
    actual_ui = test_unit.get_ui()
    assert test_ui == actual_ui


def test_setting_protocol(bot, protocol):
    test_unit = bot
    test_protocol = protocol
    test_unit.set_protocol(test_protocol)
    actual_protcol = test_unit.get_protocol()
    assert test_protocol == actual_protcol
