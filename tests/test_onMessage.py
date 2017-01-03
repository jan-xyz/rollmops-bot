#!/usr/bin/env python

import pytest
import json
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

    return proto


def test_type_user_presence(protocol):
    """
    WHEN:
        a message comes in that reports a user status
    THEN:
        the user status shall be updated internally
    """
    user_id = "U024BE7LH"
    presence = "away"
    message = {
        "type": "presence_change",
        "user": user_id,
        "presence": presence
    }

    protocol.factory.users = [
        {
          "id": user_id,
          "name": "test1",
          "presence": "active"
        },
        {
          "id": "U29HVJZ3P",
          "name": "test2",
          "presence": "active"
        }
    ]

    protocol.onMessage(json.dumps(message), False)
    for user in protocol.factory.users:
        if user["id"] == user_id:
            assert user["presence"] == presence


def test_type_reconnect_url(protocol):
    """
    WHEN:
        a message comes in that reports a new reconnect_url
    THEN:
        the internal reconnect_url shall be updated
    """
    url = ("wss://mpmulti-zmfv.slack-msgs.com/websocket/YNaPb409Ro4_JWJiqlIdzP"
           "F-DjZMj10keIf9p579u3SDQx33RhqP0PL_nJm3xXBV9-kl94Y9dqJua0sKRoFTfirE"
           "L-I2e_wIDPN3hI9LhTXfayurWBPIdruJmbwXeZyOP8rSUNS0qv6pI_6DolpznSzEWP"
           "vYNDlFLTwLJdd_L9c="
           )
    message = {
        'type': 'reconnect_url',
        'url': url
    }

    protocol.factory.reconnect_url = ""

    protocol.onMessage(json.dumps(message), False)
    assert protocol.factory.url == url
