#!/usr/bin/env python


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
