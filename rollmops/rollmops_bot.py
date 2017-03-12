#!/usr/bin/env python

import os
import slack_protocol
import slack_curses_ui
import rollmops_data_handler


class Rollmops(object):

    def __init__(self):
        self.datahandler = None
        self.ui = None
        self.protocol = None

    def set_datahandler(self, datahandler):
        self.datahandler = datahandler

    def get_datahandler(self):
        return self.datahandler

    def set_ui(self, ui):
        self.ui = ui

    def get_ui(self):
        return self.ui

    def set_protocol(self, protocol):
        self.protocol = protocol

    def get_protocol(self):
        return self.protocol


def main(mainScreen=None):
    bot = Rollmops()
    apikey = os.environ['ROLLMOPS_SLACK_API_KEY']
    requestURL = "http://slack.com/api/rtm.start?token=%s" % apikey

    datahandler = rollmops_data_handler.rollmopsDataHandler()
    if mainScreen is not None:
        ui = slack_curses_ui.slackCursesUi(mainScreen, datahandler)
    protocol = slack_protocol.slackProtocol(requestURL, datahandler)
    protocol.connect()
    protocol.ioloop.start()
    bot.set_datahandler(datahandler)
    bot.set_ui(ui)
    bot.set_protocol(protocol)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--curses', action='store_true')

    args = parser.parse_args()

    if args.curses:
        import curses
        curses.wrapper(main)
    else:
        main()
