#!/usr/bin/env python

from twisted.internet import reactor
from autobahn.twisted.websocket import connectWS
from twisted.python import log

import curses
import os

import slack_protocol
import slack_curses_ui


def main(mainScreen):
    logfile = open('log', 'w')
    log.startLogging(logfile)

    apikey = os.environ['ROLLMOPS_SLACK_API_KEY']
    requestURL = "http://slack.com/api/rtm.start?token=%s" % apikey

    ui = slack_curses_ui.slackCursesUi(mainScreen)

    protocolFactory = slack_protocol.slackFactory(requestURL, ui)
    protocolFactory.protocol = slack_protocol.slackProtocol

    connectWS(protocolFactory)
    reactor.run()

if __name__ == '__main__':
    curses.wrapper(main)
