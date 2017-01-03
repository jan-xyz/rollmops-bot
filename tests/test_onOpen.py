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
    ui = slackCursesUi(mainScreen, header_window, user_window, messages_window)
    factory = slackFactory(wssURL, ui)
    factory.protocol = slackProtocol
    proto = factory.buildProtocol(('127.0.0.1', 0))
    tr = proto_helpers.StringTransport()
    proto.makeConnection(tr)

    proto.factory.users = [
        {
            "name": "bobby",
            "presence": "active"
        },
        {
            "name": "jim",
            "presence": "inactive"
        }
    ]
    proto.user_window = mock.Mock()
    proto.header_window = mock.Mock()
    proto.messages_window = mock.Mock()

    return proto


def test_message_index_reset(protocol):
    """
    WHEN:
        a new connection is opened
    THEN:
        the messages array and message_id are reset
    """
    protocol.message_id = 3
    protocol.messages = {
        "1": "test",
        "2": "test"
    }
    assert len(protocol.messages) == 2
    assert protocol.message_id == 3
    protocol.onOpen()
    assert len(protocol.messages) == 0
    assert protocol.message_id == 1
