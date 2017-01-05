#!/usr/bin/env python

import curses


class slackCursesUi(object):

    def __init__(self, mainScreen, header_window=None, user_window=None,
                 messages_window=None):
        self.mainScreen = mainScreen
        self.header_window = self.display_header(header_window)
        self.user_window = self.display_users(user_window)
        self.messages_window = self.display_messages(messages_window)

    def display_header(self, window=None):
        if window is None:
            height = 5
            width = 40
            y = 0
            x = 0
            window = curses.newwin(height, width, y, x)
        window.addstr(2, 1, "rollmops v.0.1")
        window.border(0)
        window.refresh()
        return window

    def display_users(self, window=None, users=[]):
        if window is None:
            height = self.get_maxy(self.mainScreen) - 5
            width = 40
            window = curses.newpad(height, width)
        max_y, max_x = window.getmaxyx()
        # resize window to fit all lines
        if len(users)+2 >= max_y:
            window.resize(len(users)+2, max_x)
        # print all users onto the window
        cursor = 1
        for user in users:
            user_name = user['name'].encode('utf8')
            if user['presence'] == 'active':
                color = curses.A_STANDOUT
            else:
                color = curses.A_DIM
            window.addstr(cursor, 1, user_name, color)
            cursor += 1
        window.refresh(0, 0, 5, 0, self.get_maxy(self.mainScreen)-1, 40)
        return window

    def display_messages(self, window=None, messages=[]):
        if window is None:
            height = self.get_maxy(self.mainScreen)
            width = self.get_maxx(self.mainScreen) - 40
            window = curses.newpad(height, width)
        max_y, max_x = window.getmaxyx()
        # resize window to fit all lines
        if len(messages)+2 >= max_y:
            window.resize(len(messages)+2, max_x)
        cursor = 1
        # print all messages onto the window
        for message in messages:
            text = message['user']+":"+message['text']
            window.addstr(cursor, 1, text.encode('utf8'))
            cursor += 1
        window.border(0)
        window.refresh(0, 0, 0, 40, self.get_maxy(self.mainScreen)-1,
                       self.get_maxx(self.mainScreen))
        return window

    def get_maxx(self, window):
        return window.getmaxyx()[1]

    def get_maxy(self, window):
        return window.getmaxyx()[0]
