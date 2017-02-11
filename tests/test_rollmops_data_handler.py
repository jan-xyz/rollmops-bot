#!/usr/bin/env python


def test_get_wss_url(datahandler):
    test_url = "test this"
    datahandler.wss_url = test_url

    assert datahandler.get_wss_url() == test_url


def test_set_wss_url(datahandler):
    test_url = "test this"
    datahandler.set_wss_url(test_url)

    assert datahandler.get_wss_url() == test_url


def test_append_users(datahandler, active_users):
    assert datahandler.users == []
    datahandler.append_users(active_users)
    assert datahandler.users == active_users


def test_update_user_presence(datahandler, active_users):
    presence = "away"
    user_id = active_users[0]['id']

    datahandler.users = active_users
    assert datahandler.users[0]['presence'] == 'active'
    datahandler.update_user_presence(user_id, presence)
    assert datahandler.users[0]['presence'] == 'away'


def test_append_channels(datahandler, channels):
    assert datahandler.channels == []
    datahandler.append_channels(channels)
    assert datahandler.channels == channels


def test_get_username(datahandler, active_users):
    username = active_users[0]['name']
    user_id = active_users[0]['id']
    datahandler.users = active_users
    assert datahandler.get_username(user_id) == username
    assert datahandler.get_username('this') is None
