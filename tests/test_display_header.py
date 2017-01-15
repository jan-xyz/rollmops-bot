#!/usr/bin/env python


def test_that_it_calls_border_and_refresh(ui):
    """
    WHEN:
        display_header is called
    THEN:
        the window border is set to 0
    """
    ui.display_header(ui.header_window)
    ui.header_window.border.assert_called_with(0)
    ui.header_window.refresh.assert_called_with()
