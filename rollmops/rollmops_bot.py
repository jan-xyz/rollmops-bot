#!/usr/bin/env python

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import connectWS
import curses
import sys
import os

import slack_protocol


def main(stdscr):
    apikey = os.environ['ROLLMOPS_SLACK_API_KEY']
    requestURL = "http://slack.com/api/rtm.start?token=%s" % apikey

    log.startLogging(sys.stdout)

    factory = slack_protocol.slackFactory(requestURL, stdscr)
    factory.protocol = slack_protocol.slackProtocol

    connectWS(factory)
    reactor.run()

if __name__ == '__main__':
    curses.wrapper(main)
