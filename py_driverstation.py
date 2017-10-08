"""
Python-based driver station. Currently only for
 the Pigmice-variant of RobotPy for Raspberry Pi
"""

import sys
import configparser

from PyQt5.QtWidgets import QAction, QApplication, QMainWindow
from PyQt5.QtCore import QTimer

from networktables import NetworkTables

from joysticks import Joysticks
from driverstation_ui.driverstation_ui import Ui_MainWindow


class PyDriverStation(Ui_MainWindow):
    """
    Python-based driver station to communicate with the Raspberry Pi
    """

    def __init__(self, qmain_window, server_ip=None):
        super(PyDriverStation, self).__init__()

        self.main_window = qmain_window

        self.setupUi(qmain_window)

        self.config_file_name = 'ds_config.cfg'
        self.init_config(self.config_file_name)

        self.table_name = 'driver_station'
        if server_ip:
            NetworkTables.initialize(server_ip)
        else:
            NetworkTables.initialize(
                self.config_parser['NetworkTables']['team_number'])
        self.table = NetworkTables.getTable(self.table_name)

        self.joysticks = Joysticks()

        # Set exit shortcut to 'Ctrl+Q'
        exit_act = QAction('Exit', self.main_window)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(self.close_application)
        self.main_window.addAction(exit_act)

        self.connect_buttons()
        self.setup_team_selector()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def init_config(self, config_name):
        """Read `config_name` into configparser.

        Will create `config_file` if it doesn't already exist
        """
        self.config_parser = configparser.ConfigParser()
        self.config_parser['DEFAULT'] = {'team_number': '2733'}

        try:
            self.config_parser.read_file(open(config_name))
        except FileNotFoundError:
            self.config_parser['NetworkTables'] = {'team_number': '2733'}
            self.save_config(config_name)

    def save_config(self, config_name):
        """Save config into `config_name`"""
        with open(config_name, 'w') as config_file:
            self.config_parser.write(config_file)

    def connect_buttons(self):
        """Connect buttons to handler functions"""
        self.mode_buttons = [self.AutonomousModeButton,
                             self.TeleopModeButton, self.TestModeButton]
        self.mode_names = {
            self.AutonomousModeButton: "autonomous",
            self.TeleopModeButton: "teleop",
            self.TestModeButton: "test"
        }

        self.enable_buttons = [self.EnableButton, self.DisableButton]
        self.enable_buttons_status = {
            self.EnableButton: True,
            self.DisableButton: False
        }

        self.AutonomousModeButton.clicked.connect(
            lambda _: self.mode_button_press(self.AutonomousModeButton))
        self.TeleopModeButton.clicked.connect(
            lambda _: self.mode_button_press(self.TeleopModeButton))
        self.TestModeButton.clicked.connect(
            lambda _: self.mode_button_press(self.TestModeButton))

        self.EnableButton.clicked.connect(
            lambda _: self.enabled_button_press(self.EnableButton))
        self.DisableButton.clicked.connect(
            lambda _: self.enabled_button_press(self.DisableButton))

    def setup_team_selector(self):
        """Setup the team selector spinbox"""
        self.TeamNumberSelector.setValue(
            int(self.config_parser['NetworkTables']['team_number']))

        self.UpdateTeamButton.clicked.connect(
            lambda _: self.team_selector_update(
                self.TeamNumberSelector.value())
        )

    def set_joystick_axis_value(self, joystick_number: int, axis_number: int, value: float):
        """Set a Networktable value. Set the joystick axis specified
        by `joystick` and `axis` to `value`.
        """
        key = "/joystick-" + str(joystick_number) + "/axis-" + str(axis_number)
        self.table.putNumber(key, value)

    def set_joystick_button_value(self, joystick_number: int, button_number: int, value: bool):
        """Set a Networktable value. Set the joystick button specified
        by `joystick` and `button` to `value`.
        """
        key = "/joystick-" + str(joystick_number) + \
            "/button-" + str(button_number)
        self.table.putBoolean(key, value)

    def update(self):
        """Update driver station"""

        # Set joystick data in NetworkTables
        self.joysticks.update()

        for joystick_num in range(self.joysticks.get_num_joysticks()):
            joy_data = self.joysticks.get_joystick(joystick_num)

            for index, value in enumerate(joy_data["axes"]):
                self.set_joystick_axis_value(joystick_num, index, value)

            for index, value in enumerate(joy_data["buttons"]):
                self.set_joystick_button_value(joystick_num, index, value)

    def mode_button_press(self, pressed_button):
        """Event handler for mode button press

        Sets mode buttons to checked/unchecked as if they were radio buttons.
        Updates game mode in NetworkTables.
        """
        for mode_button in self.mode_buttons:
            if mode_button == pressed_button:
                mode_button.setChecked(True)
                self.set_game_mode(self.mode_names[mode_button])
            else:
                mode_button.setChecked(False)

    def enabled_button_press(self, pressed_button):
        """Event handler for enable/disable button press

        Sets buttons checked state as if they were radio buttons.
        Updates enable/disable status in NetworkTables.
        """
        for button in self.enable_buttons:
            if button == pressed_button:
                button.setChecked(True)
                self.set_enabled(self.enable_buttons_status[button])
            else:
                button.setChecked(False)

    def team_selector_update(self, new_team_number):
        """Update team number button event handler

        Updates team number with current value of team number spinbox,
        connects NetworkTables to correct robot.
        """
        self.config_parser['NetworkTables']['team_number'] = str(
            new_team_number)

        NetworkTables.shutdown()
        NetworkTables.setTeam(new_team_number)
        NetworkTables.setClientMode()
        NetworkTables.initialize()

    def set_game_mode(self, mode: str):
        """Set the current game mode in NetworkTables"""
        key = "/mode"
        self.table.putString(key, mode)

    def set_enabled(self, enabled: bool):
        """Set enabled status in NetworkTables"""
        key = "/enabled"
        self.table.putBoolean(key, enabled)

    def close_application(self):
        """Cleanup and close application"""
        self.timer.stop()
        self.main_window.close()
        self.joysticks.quit()
        self.save_config(self.config_file_name)
        NetworkTables.shutdown()


if __name__ == '__main__':
    try:
        SERVER_IP = sys.argv[1]
    except IndexError:
        # No server ip provided, try localhost
        SERVER_IP = '127.0.0.1'

    print("Connecting to: " + SERVER_IP)

    APP = QApplication(sys.argv)
    WINDOW = QMainWindow()
    DS = PyDriverStation(WINDOW, SERVER_IP)
    WINDOW.show()

    try:
        sys.exit(APP.exec_())
    except KeyboardInterrupt:
        DS.close_application()
        print("\n\nExiting...\n\n")
        sys.exit(0)
