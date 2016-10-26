#!/usr/bin/env python

from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientFactory
from autobahn.twisted.websocket import connectWS

from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
import sys
import os
import requests
import json


class MyClientProtocol(WebSocketClientProtocol):

    def __init__(self):
        WebSocketClientProtocol.__init__(self)
        self.messages = {}
        self.users = {}
        self.channels = {}
        self.ims = {}
        self.message_id = 1
        self.reconnect_url = ""
        self.factory = None

    def onOpen(self):
        self.messages.clear()
        self.message_id = 1

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
            else:
                print jsonPayload
        elif 'ok' in jsonPayload:
            print "srv ack: '%s'" % self.messages[jsonPayload['reply_to']]
        else:
            print jsonPayload

    def update_factory_url(self, url):
        self.factory.url = url

    def update_user_presence(self, user_id, presence):
        for user in self.factory.users:
            if user["id"] == user_id:
                user["presence"] = presence
                print "%s is now %s" % (user["name"], user["presence"])

    def parse_message(self, message):
        print message
        if "rollmops" in message["text"]:
            user_name = message['user']
            for user in self.factory.users:
                if user['id'] == message['user']:
                    user_name = user['name']
            text = "Hello %s, how can I help you?" % user_name
            channel = message["channel"]
            self.sendMessageToChannel(text, channel)


class ourWS_reconnecting(ReconnectingClientFactory, WebSocketClientFactory):

    def __init__(self, requestURL):
        if requestURL == "":
            wssURL = ""
        else:
            res = requests.get(requestURL)
            try:
                json_reqsponse = json.loads(res.text)
            except:
                print
                print "received broken json from %s" % requestURL
                sys.exit(1)

            wssURL = json_reqsponse["url"]
            self.users = json_reqsponse["users"]

        WebSocketClientFactory.__init__(self, wssURL)

    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self
        return p


def main():
    apikey = os.environ['ROLLMOPS_SLACK_API_KEY']
    requestURL = "http://slack.com/api/rtm.start?token=%s" % apikey

    log.startLogging(sys.stdout)

    factory = ourWS_reconnecting(requestURL)
    factory.protocol = MyClientProtocol

    connectWS(factory)
    reactor.run()

if __name__ == '__main__':
    main()
