#! /usr/bin/env python


class rollmopsDataHandler(object):

    def __init__(self):
        self.wss_url = None
        self.users = []
        self.channels = []
        self.messages = []

        self.user_listeners = []
        self.message_listeners = []

    def get_wss_url(self):
        return self.wss_url

    def set_wss_url(self, wss_url):
        self.wss_url = wss_url

    def update_user_presence(self, user_id, presence):
        for user in self.users:
            if user['id'] == user_id:
                user["presence"] = presence
        self.notify_user_listeners()

    def append_users(self, users):
        for user in users:
            self.users.append(user)
        self.notify_user_listeners()

    def append_channels(self, channels):
        for channel in channels:
            self.channels.append(channel)

    def get_username(self, user_id):
        for user in self.users:
            if user['id'] == user_id:
                return user['name']
        return None

    def append_message(self, message):
        self.messages.append(message)
        self.notify_message_listeners()

    def add_user_listener(self, listener):
        self.user_listeners.append(listener)

    def notify_user_listeners(self):
        for listener in self.user_listeners:
            listener.on_user_change(self.users)

    def add_message_listener(self, listener):
        self.message_listeners.append(listener)

    def notify_message_listeners(self):
        for listener in self.message_listeners:
            listener.on_message_change(self.messages)
