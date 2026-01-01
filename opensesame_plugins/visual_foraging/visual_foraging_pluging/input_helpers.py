"""
Helper function for waiting for a mouse click in pygame.
"""

import pygame


def get_click(timeout=None, double_click_interval=400):
    """
    Wait for a mouse click and return click info.

    Parameters
    ----------
    timeout : float or None
        Maximum time to wait in seconds. None = wait indefinitely.
    double_click_interval : int
        Maximum time between clicks to count as double click (ms).

    Returns
    -------
    click_info : dict
        Contains:
            'x', 'y' : position of click
            'button' : mouse button pressed
            'rt' : reaction time in milliseconds
            'click_type' : 'single' or 'double'
        Returns None if timeout or quit.
    """
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    last_click_time = 0
    last_pos = None

    while True:
        now = pygame.time.get_ticks()
        if timeout is not None and (now - start_time) > timeout * 1000:
            return None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                button = event.button
                rt = now - start_time

                click_type = 'single'
                if last_click_time and (now - last_click_time) <= double_click_interval:
                    if last_pos == (x, y):
                        click_type = 'double'

                last_click_time = now
                last_pos = (x, y)

                return {
                    'x': x,
                    'y': y,
                    'button': button,
                    'rt': rt,
                    'click_type': click_type
                }

        clock.tick(60)

