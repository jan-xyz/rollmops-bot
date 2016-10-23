#!/usr/bin/env python

from rollmops.rollmops_bot import MyClientProtocol, ourWS_reconnecting


def test_createFactory():
    wssURL = ''
    factory = ourWS_reconnecting(wssURL)
    factory.protocol = MyClientProtocol
    assert isinstance(factory, ourWS_reconnecting)
