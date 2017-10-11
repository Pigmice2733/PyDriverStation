"""Joystick-related utilities"""


class Joysticks:
    """Provides data about usb joysticks (and other
     controllers pygame recognizes as joysticks) via pygame
    """

    def __init__(self, pygame):
        """Initialize joysticks"""

        self._pygame = pygame

        self._pygame.init()

        self._scan_joysticks()

    def _scan_joysticks(self):
        # List of all joysticks plugged in (at time of initialization)
        self._joysticks = [self._pygame.joystick.Joystick(
            x) for x in range(self._pygame.joystick.get_count())]
        list(map(lambda joy: joy.init(), self._joysticks))

    def update(self):
        """Call periodically, preferably before a group of calls
         to `get_joystick`, this will flush the pygame event queue.
        """
        self._pygame.event.get()

    def get_num_joysticks(self) -> int:
        """Returns the number of USB joysticks plugged into computer.

        Note - Hat sticks (on most joysticks) will count as separate joysticks.
        """
        return self._pygame.joystick.get_count()

    def get_joystick(self, stick: int) -> dict:
        """Returns dict holding state of specified joystick.

        `joy_data = {
            axes: [0.0, 0.0, 0.0],
            buttons: [0, 1, 0]
        }`

        `axes` holds the position of joystick `n` at index
         `n`, `buttons` does the same for the buttons.
        """

        joy_data = {"axes": [], "buttons": []}

        joystick = self._joysticks[stick]

        for axis in range(joystick.get_numaxes()):
            # We might need to skip axis #6 to remain
            #  consistent with RobotPy and WPIlib
            joy_data["axes"].append(joystick.get_axis(axis))

        for button in range(joystick.get_numbuttons()):
            # We might need to skip button #10 to remain
            #  consistent with RobotPy and WPIlib
            joy_data["buttons"].append(joystick.get_button(button))

        return joy_data

    def quit(self):
        """Clean up and release resources"""
        self._pygame.quit()
