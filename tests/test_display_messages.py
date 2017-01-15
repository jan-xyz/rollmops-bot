#!/usr/bin/env python


def test_that_it_calls_border_and_refresh(ui):
    """
    WHEN:
        display_header is called
    THEN:
        the window border is set to 0
    """
    ui.display_messages(ui.messages_window)
    ui.messages_window.border.assert_called_with(0)
    ui.messages_window.refresh.assert_called_with(0, 0, 0, 40, 9, 10)
