#!/usr/bin/env python

import pytest
import mock
from twisted.test import proto_helpers


@pytest.fixture(scope="module")
def protocol():
    from rollmops.rollmops_bot import MyClientProtocol, ourWS_reconnecting

    wssURL = ''

    main_window = mock.Mock()
    factory = ourWS_reconnecting(wssURL, main_window)
    factory.protocol = MyClientProtocol
    proto = factory.buildProtocol(('127.0.0.1', 0))
    tr = proto_helpers.StringTransport()
    proto.makeConnection(tr)

    return proto


def test_that_it_calls_border_and_refresh(protocol):
    """
    WHEN:
        display_header is called
    THEN:
        the window border is set to 0
    """
    window = mock.Mock()
    protocol.display_header(window)
    window.border.assert_called_with(0)
    window.refresh.assert_called_with()
