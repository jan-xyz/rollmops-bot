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

    return proto


def test_that_it_calls_border_and_refresh(protocol):
    """
    WHEN:
        display_users is called
    THEN:
        the window border is set to 0
    """
    window = mock.Mock()
    users = [
        {
            "name": "bobby",
            "presence": "active"
        },
        {
            "name": "jim",
            "presence": "inactive"
        }
    ]
    protocol.ui.display_users(window, users)
    window.border.assert_called_with(0)
    window.refresh.assert_called_with()
