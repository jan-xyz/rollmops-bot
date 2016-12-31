#!/usr/bin/env python

from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientFactory
from twisted.internet.protocol import ReconnectingClientFactory

import json
import sys
import requests
import curses


class slackProtocol(WebSocketClientProtocol):
    def __init__(self, stdscr):
        WebSocketClientProtocol.__init__(self)
        self.messages = {}
        self.channels = {}
        self.ims = {}
        self.message_id = 1
        self.received_message_id = 1
        self.reconnect_url = ""
        self.factory = None

        self.stdscr = stdscr
        self.user_window = None
        self.header_window = None
        self.messages_window = None

    def onOpen(self):
        self.messages.clear()
        self.message_id = 1
        self.received_message_id = 1
        self.stdscr.refresh()
        self.user_window = self.display_users(self.factory.users,
                                              self.user_window)
        self.header_window = self.display_header(self.header_window)
        self.messages_window = self.display_messages(self.messages_window)

    def onMessage(self, payload, isBinary):
        res_string = payload.decode('utf8')
        res_json = json.loads(res_string)
        self.parseJsonPayload(res_json)
        self.display_messages(self.messages_window, res_json)
        self.received_message_id += 1

    def display_header(self, window):
        if window is None:
            window = curses.newwin(5, 40, 0, 0)
        window.addstr(2, 10, "rollmops bot v.0.1")
        window.border(0)
        window.refresh()

        return window

    def display_users(self, users, window):
        if window is None:
            begin_x = 0
            begin_y = 5
            height = len(users)
            width = 40
            window = curses.newwin(height, width, begin_y, begin_x)
        cursor = 0
        for user in users:
            user_name = user['name'].encode('utf-8')
            if user['presence'] == 'active':
                color = curses.A_STANDOUT
            else:
                color = curses.A_DIM
            window.addstr(cursor, 1, user_name, color)
            cursor += 1
        window.border(0)
        window.refresh()

        return window

    def display_messages(self, window, message=None):
        if window is None:
            window = curses.newwin(40, 120, 0, 40)
        if message is not None:
            window.addstr(self.received_message_id, 1,
                          json.dumps(message).encode('utf-8'))
        window.border(0)
        window.refresh()

        return window

    def sendMessageToChannel(self, text, channel):
        message_type = "message"
        message_channel = channel
        message_text = text
        message = {
            "id": self.message_id,
            "type": message_type,
            "channel": message_channel,
            "text": message_text
        }

        self.messages[self.message_id] = message
        self.sendMessage(json.dumps(message))
        self.message_id = self.message_id + 1

    def parseJsonPayload(self, jsonPayload):
        if 'type' in jsonPayload:
            if jsonPayload['type'] == 'reconnect_url':
                self.update_factory_url(jsonPayload['url'])
            elif jsonPayload['type'] == 'presence_change':
                self.update_user_presence(jsonPayload['user'],
                                          jsonPayload['presence'])
            elif jsonPayload['type'] == 'message':
                self.parse_message(jsonPayload)

    def update_factory_url(self, url):
        self.factory.url = url

    def update_user_presence(self, user_id, presence):
        for user in self.factory.users:
            if user["id"] == user_id:
                user["presence"] = presence
        self.display_users(self.factory.users, self.user_window)

    def parse_message(self, message):
        if "rollmops" in message["text"]:
            user_name = message['user']
            for user in self.factory.users:
                if user['id'] == message['user']:
                    user_name = user['profile']['first_name']
            text = "Hello %s, how can I help you?" % user_name
            channel = message["channel"]
            self.sendMessageToChannel(text, channel)


class slackFactory(ReconnectingClientFactory, WebSocketClientFactory):

    def __init__(self, requestURL, stdscr):
        self.stdscr = stdscr
        if requestURL == "":
            wssURL = ""
        else:
            res = requests.get(requestURL)
            try:
                json_reqsponse = json.loads(res.text)
            except:
                sys.exit(1)

            wssURL = json_reqsponse["url"]
            self.users = json_reqsponse["users"]

        WebSocketClientFactory.__init__(self, wssURL)

    def buildProtocol(self, addr):
        p = self.protocol(self.stdscr)
        p.factory = self
        return p
