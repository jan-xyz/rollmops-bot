#!/usr/bin/env python

import pytest
from twisted.test import proto_helpers


@pytest.fixture(scope="module")
def protocol():
    from rollmops.rollmops_bot import MyClientProtocol, ourWS_reconnecting

    wssURL = ''

    factory = ourWS_reconnecting(wssURL)
    factory.protocol = MyClientProtocol
    proto = factory.buildProtocol(('127.0.0.1', 0))
    tr = proto_helpers.StringTransport()
    proto.makeConnection(tr)

    return proto


def test_message_index_increment(protocol):
    """
    WHEN:
        a message is sent
    THEN:
        the message is stored in the message array and message_id is
        incremented.
    """
    protocol.messages = {}
    protocol.message_id = 1

    test_message = "test message"
    test_channel = "G2S151RCP"

    protocol.sendMessageToChannel(test_message, test_channel)

    assert len(protocol.messages) == 1
    assert protocol.message_id == 2
    assert protocol.messages[1]["text"] == test_message
    assert protocol.messages[1]["channel"] == test_channel
