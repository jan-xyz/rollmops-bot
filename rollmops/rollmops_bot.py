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
        self.message_id = 0

    def onOpen(self):
        self.messages = {}
        self.sendMessageToChannel("hello Jan", "G2S151RCP")

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
                print jsonPayload['url']
            elif jsonPayload['type'] == 'presence_change':
                print '%s is now %s' % (jsonPayload['user'],
                                        jsonPayload['presence'])
        elif 'ok' in jsonPayload:
            print "srv ack: '%s'" % self.messages[jsonPayload['reply_to']]
        else:
            print jsonPayload


class ourWS_reconnecting(ReconnectingClientFactory, WebSocketClientFactory):

    def __init__(self, *args, **kwargs):
        WebSocketClientFactory.__init__(self, *args, **kwargs)


def main():
    apikey = os.environ['ROLLMOPS_SLACK_API_KEY']
    requestURL = "http://slack.com/api/rtm.start?token=%s" % apikey

    res = requests.get(requestURL)
    try:
        json_reqsponse = json.loads(res.text)
    except:
        print
        print "received broken json from %s" % requestURL
        sys.exit(1)

    wssURL = json_reqsponse["url"]

    log.startLogging(sys.stdout)

    factory = ourWS_reconnecting(wssURL)
    factory.protocol = MyClientProtocol

    connectWS(factory)
    reactor.run()

if __name__ == '__main__':
    main()
