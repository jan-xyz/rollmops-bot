#!/usr/bin/env python

import curses


class slackCursesUi(object):

    def __init__(self, mainScreen):
        self.header_window = self.display_header()
        self.user_window = self.display_users()
        self.messages_window = self.display_messages()

    def display_header(self, window=None):
        if window is None:
            window = curses.newwin(5, 40, 0, 0)
        window.border(0)
        window.refresh()
        return window

    def display_users(self, window=None):
        if window is None:
            window = curses.newwin(40, 20, 5, 0)
        window.border(0)
        window.refresh()
        return window

    def display_messages(self, window=None):
        if window is None:
            window = curses.newwin(40, 120, 0, 40)
        window.border(0)
        window.refresh()
        return window
