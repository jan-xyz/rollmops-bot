#!/usr/bin/env python

import curses


class slackCursesUi(object):

    def __init__(self, mainScreen):
        self.mainScreen = mainScreen
        self.header_window = self.display_header()
        self.user_window = self.display_users()
        self.messages_window = self.display_messages()

    def display_header(self, window=None):
        if window is None:
            height = 5
            width = 40
            y = 0
            x = 0
            window = curses.newwin(height, width, y, x)
        window.border(0)
        window.refresh()
        return window

    def display_users(self, window=None):
        if window is None:
            height = self.get_maxy(self.mainScreen) - 5
            width = 40
            y = 5
            x = 0
            window = curses.newwin(height, width, y, x)
        window.border(0)
        window.refresh()
        return window

    def display_messages(self, window=None):
        if window is None:
            height = self.get_maxy(self.mainScreen)
            width = self.get_maxx(self.mainScreen) - 40
            y = 0
            x = 40
            window = curses.newwin(height, width, y, x)
        window.border(0)
        window.refresh()
        return window

    def get_maxx(self, window):
        return window.getmaxyx()[1]

    def get_maxy(self, window):
        return window.getmaxyx()[0]
