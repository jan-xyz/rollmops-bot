#!/usr/bin/env python

from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientFactory
from twisted.internet.protocol import ReconnectingClientFactory

import json
import sys
import requests


class slackProtocol(WebSocketClientProtocol):
    def __init__(self):
        WebSocketClientProtocol.__init__(self)
        self.messages = {}
        self.channels = {}
        self.ims = {}
        self.message_id = 1
        self.reconnect_url = ""
        self.factory = None

    def onOpen(self):
        self.messages.clear()
        self.message_id = 1
        self.received_message_id = 1

    def onMessage(self, payload, isBinary):
        res_string = payload.decode('utf8')
        res_json = json.loads(res_string)
        self.parseJsonPayload(res_json)

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

    def __init__(self, requestURL):
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
        p = self.protocol()
        p.factory = self
        return p
