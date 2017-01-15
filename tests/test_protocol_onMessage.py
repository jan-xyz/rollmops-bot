#!/usr/bin/env python

import json


def test_type_user_presence(protocol, active_users):
    """
    WHEN:
        a message comes in that reports a user status
    THEN:
        the user status shall be updated internally
    """
    user_id = active_users[0]['id']
    presence = "away"
    message = {
        "type": "presence_change",
        "user": user_id,
        "presence": presence
    }

    protocol.factory.users = active_users
    assert protocol.factory.users[0]["presence"] == "active"

    protocol.onMessage(json.dumps(message), False)
    user_found = False
    for user in protocol.factory.users:
        if user["id"] == user_id:
            user_found = True
            assert user["presence"] == presence
    if not user_found:
        assert False


def test_type_reconnect_url(protocol):
    """
    WHEN:
        a message comes in that reports a new reconnect_url
    THEN:
        the internal reconnect_url shall be updated
    """
    message = {
        'type': 'reconnect_url',
        'url': "wss://mpmulti-zmfv.slack-msgs.com/websocket/YNa"
    }

    protocol.factory.reconnect_url = ""
    assert protocol.factory.url == ""

    protocol.onMessage(json.dumps(message), False)
    assert protocol.factory.url == message['url']


def test_type_message_causes_ui_call(protocol):
    """
    WHEN:
        a message comes in that reports a new message
    THEN:
        the ui shall be notified
    """
    window = protocol.ui.messages_window
    message = {
        'type': 'message',
        'text': 'hello world!'
    }
    messages = []

    protocol.incoming_messages = messages
    assert protocol.incoming_messages == messages
    protocol.onMessage(json.dumps(message), False)
    messages.append(message)
    protocol.ui.display_messages.assert_called_with(window, messages)
