#!/usr/bin/env python


def test_that_it_calls_border_and_refresh(ui):
    """
    WHEN:
        display_users is called
    THEN:
        the window border is set to 0
    """
    ui.display_users(ui.user_window)
    ui.user_window.getmaxyx.assert_called_with()
    ui.user_window.refresh.assert_called_with(0, 0, 5, 0, 9, 40)
