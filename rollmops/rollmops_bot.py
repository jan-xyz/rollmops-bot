#!/usr/bin/env python

import os
import slack_protocol
import slack_curses_ui
import rollmops_data_handler


class Rollmops(object):

    def __init__(self):
        pass


def main(mainScreen=None):
    apikey = os.environ['ROLLMOPS_SLACK_API_KEY']
    requestURL = "http://slack.com/api/rtm.start?token=%s" % apikey

    datahandler = rollmops_data_handler.rollmopsDataHandler()
    if mainScreen is not None:
        slack_curses_ui.slackCursesUi(mainScreen, datahandler)
    protocol = slack_protocol.slackProtocol(requestURL, datahandler)
    protocol.connect()
    protocol.ioloop.start()


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
