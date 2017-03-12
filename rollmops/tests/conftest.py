#!/usr/bin/env python

import pytest
import mock


@pytest.fixture(scope="module")
def protocol():
    from rollmops.slack_protocol import slackProtocol

    requestURL = ''
    datahandler = mock.Mock()

    return slackProtocol(requestURL, datahandler)


@pytest.fixture(scope="module")
def ui():
    from rollmops.slack_curses_ui import slackCursesUi

    mainScreen = mock.Mock()
    header_window = mock.Mock()
    user_window = mock.Mock()
    messages_window = mock.Mock()
    datahander = mock.Mock()
    user_window.getmaxyx.return_value = 10, 10
    messages_window.getmaxyx.return_value = 10, 10
    mainScreen.getmaxyx.return_value = 10, 10
    ui = slackCursesUi(mainScreen, datahander, header_window,
                       user_window, messages_window)
    return ui


@pytest.fixture(scope="module")
def datahandler():
    from rollmops.rollmops_data_handler import rollmopsDataHandler

    return rollmopsDataHandler()


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


@pytest.fixture(scope="module")
def channels():
    channels = [
        {
            "id": "C024BE91L",
            "name": "fun",
            "created": 1360782804,
            "creator": "U024BE7LH",
            "is_archived": False,
            "is_member": False,
            "num_members": 6,
            "topic": {
                "value": "Fun times",
                "creator": "U024BE7LH",
                "last_set": 1369677212
            },
            "purpose": {
                "value": "This channel is for fun",
                "creator": "U024BE7LH",
                "last_set": 1360782804
            }
        },
        {
            "id": "C024FG91L",
            "name": "work",
            "created": 1360782804,
            "creator": "U026BE7LM",
            "is_archived": False,
            "is_member": False,
            "num_members": 3,
            "topic": {
                "value": "all the work",
                "creator": "U026BE7LM",
                "last_set": 1369677212
            },
            "purpose": {
                "value": "This channel is for work",
                "creator": "U024BE7LH",
                "last_set": 1360782804
            }
        }
    ]
    return channels
