#!/usr/bin/env python

import pytest
import mock
from twisted.test import proto_helpers


@pytest.fixture(scope="module")
def protocol():
    from rollmops.slack_protocol import slackProtocol, slackFactory
    from rollmops.slack_curses_ui import slackCursesUi

    wssURL = ''

    ui = mock.Mock()
    factory = slackFactory(wssURL, ui)
    factory.protocol = slackProtocol
    proto = factory.buildProtocol(('127.0.0.1', 0))
    tr = proto_helpers.StringTransport()
    proto.makeConnection(tr)

    return proto


@pytest.fixture(scope="module")
def ui():
    from rollmops.slack_curses_ui import slackCursesUi

    mainScreen = mock.Mock()
    header_window = mock.Mock()
    user_window = mock.Mock()
    messages_window = mock.Mock()
    user_window.getmaxyx.return_value = 10, 10
    messages_window.getmaxyx.return_value = 10, 10
    mainScreen.getmaxyx.return_value = 10, 10
    ui = slackCursesUi(mainScreen, header_window, user_window, messages_window)
    return ui


@pytest.fixture(scope="module")
def active_users():
    users = [
        {
          "id": "U024BE7LH",
          "name": "test1",
          "presence": "active"
        },
        {
          "id": "U026BE7LM",
          "name": "test2",
          "presence": "active"
        }
    ]
    return users


@pytest.fixture(scope="module")
def idle_users():
    users = [
        {
          "id": "U024BE7LH",
          "name": "test1",
          "presence": "away"
        },
        {
          "id": "U026BE7LM",
          "name": "test2",
          "presence": "away"
        }
    ]
    return users
