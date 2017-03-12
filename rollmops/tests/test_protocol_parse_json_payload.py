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

    protocol.parse_json_payload(message)
    protocol.datahandler.update_user_presence.assert_called_with(
        user_id, presence)


def test_type_reconnect_url(protocol):
    """
    WHEN:
        a message comes in that reports a new reconnect_url
    THEN:
        the internal reconnect_url shall be updated
    """
    url = "wss://mpmulti-zmfv.slack-msgs.com/websocket/YNa"
    message = {
        'type': 'reconnect_url',
        'url': url
    }

    protocol.parse_json_payload(message)
    protocol.datahandler.set_wss_url.assert_called_with(url)


def test_type_message_causes_ui_call(protocol):
    """
    WHEN:
        a message comes in that reports a new message
    THEN:
        the ui shall be notified
    """
    message = {
        'type': 'message',
        'text': 'hello world!'
    }

    protocol.parse_json_payload(message)
    protocol.datahandler.append_message.assert_called_with(message)
