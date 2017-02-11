#! /usr/bin/env python

from tornado.ioloop import IOLoop
from tornado import gen, httpclient
from tornado.websocket import websocket_connect

import json


class slackProtocol(object):

    def __init__(self, requestURL, datahandler):
        self.datahandler = datahandler
        loginResponse = self.requestSlackLogin(requestURL)
        if loginResponse is not None:
            self.initialize_datahandler(datahandler, loginResponse)
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.message_id = 0

    def requestSlackLogin(self, url):
        http_client = httpclient.HTTPClient()
        json_response = None
        try:
            response = http_client.fetch(url)
            json_response = json.loads(response.body)
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            print("Error: " + str(e))
        except Exception as e:
            # Other errors are possible, such as IOError.
            print("Error: " + str(e))
        http_client.close()
        return json_response

    def initialize_datahandler(self, datahandler, response):
        datahandler.set_wss_url(response['url'])
        datahandler.append_users(response['users'])
        datahandler.append_channels(response['channels'])

    @gen.coroutine
    def connect(self):
        try:
            self.ws = yield websocket_connect(self.datahandler.get_wss_url())
        except Exception, e:
            print "connection error %s" % e
        else:
            self.run()

    @gen.coroutine
    def run(self):
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                print "connection closed"
                self.ws = None
                break
            self.parse_json_payload(json.loads(msg))

    def parse_json_payload(self, jsonPayload):
        if 'type' in jsonPayload:
            if jsonPayload['type'] == 'reconnect_url':
                self.update_reconnect_url(jsonPayload['url'])
            elif jsonPayload['type'] == 'presence_change':
                self.update_user_presence(jsonPayload['user'],
                                          jsonPayload['presence'])
            elif jsonPayload['type'] == 'message':
                self.parse_message(jsonPayload)

    def update_reconnect_url(self, url):
        self.datahandler.set_wss_url(url)

    def update_user_presence(self, user_id, presence):
        self.datahandler.update_user_presence(user_id, presence)

    def parse_message(self, message):
        self.datahandler.append_message(message)
        if "rollmops" in message["text"]:
            text = "Hello %s, how can I help you?" % (
                self.datahandler.get_username(message['user'])
            )
            channel = message["channel"]
            self.send_message_to_channel(text, channel)

    def send_message_to_channel(self, text, channel):
        message_type = "message"
        message_channel = channel
        message_text = text
        message = {
            "id": self.message_id,
            "type": message_type,
            "channel": message_channel,
            "text": message_text
        }

        self.ws.write_message(json.dumps(message))
        self.message_id = self.message_id + 1
