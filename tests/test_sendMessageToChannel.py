#!/usr/bin/env python

import pytest
import mock
from twisted.test import proto_helpers


@pytest.fixture(scope="module")
def protocol():
    from rollmops.slack_protocol import slackProtocol, slackFactory
    from rollmops.slack_curses_ui import slackCursesUi

    wssURL = ''

    mainScreen = mock.Mock()
    header_window = mock.Mock()
    user_window = mock.Mock()
    messages_window = mock.Mock()
    user_window.getmaxyx.return_value = 10, 10
    messages_window.getmaxyx.return_value = 10, 10
    mainScreen.getmaxyx.return_value = 10, 10

    ui = slackCursesUi(mainScreen, header_window, user_window, messages_window)
    factory = slackFactory(wssURL, ui)
    factory.protocol = slackProtocol
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
