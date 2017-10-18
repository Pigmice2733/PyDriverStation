"""
Python-based driver station. Currently only for
 the Pigmice-variant of RobotPy for Raspberry Pi
"""

import sys
import configparser

# No name ... in module ... - pylint seems to have trouble with PyQt
# pylint: disable=E0611
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QStyle
from PyQt5.QtCore import QTimer, QRect, QPoint, QSize, Qt
from PyQt5.QtGui import QColor
# pylint: enable=E0611

import pygame
import networktables

from joysticks import Joysticks
from network import Network
from driverstation_ui.driverstation_ui import Ui_MainWindow


class DriverStationConfig:
    """Driver station config"""

    def __init__(self, config_file_name):
        """Initialize config using `config_file_name` as source file

        Will create `config_file_name` if it doesn't already exist
        """

        self.config_file_name = config_file_name
        self.config_parser = configparser.ConfigParser()
        self.config_parser['DEFAULT'] = {'team_number': '2733'}

        try:
            self.config_parser.read_file(open(config_file_name))
        except FileNotFoundError:
            self.config_parser['NetworkTables'] = {'team_number': '2733'}
            self.save_config()

    @property
    def team_number(self) -> int:
        """Get the team number from the config"""
        return int(self.config_parser['NetworkTables']['team_number'])

    @team_number.setter
    def team_number(self, new_team_number: int):
        """Set the team number in the config"""
        self.config_parser['NetworkTables']['team_number'] = new_team_number

    def save_config(self):
        """Save config into `config_file_name`"""
        with open(self.config_file_name, 'w') as config_file:
            self.config_parser.write(config_file)


class StatusIndicator:  # (Too few public methods) pylint: disable=R0903
    """Controller for status indicator"""

    def __init__(self, indicator_widget, status_colors):
        self.widget = indicator_widget
        self.status_colors = status_colors

        self.status = False
        self.widget.setStyleSheet(
            "background-color: %s" % self.status_colors[self.status].name())

    def update(self, new_status):
        """Update status indicator with new status

        Indicator widget color will be updated
         to correspond with new status
        """
        # Set status indicator color
        # Once status is updated, don't update again to avoid unecessary redraws
        if new_status and not self.status:
            self.status = True
            self.widget.setStyleSheet(
                "background-color: %s" % self.status_colors[self.status].name())
        elif not new_status and self.status:
            self.status = False
            self.widget.setStyleSheet(
                "background-color:  %s" % self.status_colors[self.status].name())


# (Too many instance attributes) pylint: disable=R0902
class PyDriverStation(Ui_MainWindow):
    """Python-based driver station to communicate with the Raspberry Pi
    """

    def __init__(self, qmain_window, network, config, joysticks):
        super(PyDriverStation, self).__init__()

        self.main_window = qmain_window
        self.setupUi(self.main_window)
        self.scale_window()

        self.config = config
        self.network = network
        self.joysticks = joysticks

        # Set exit shortcut to 'Ctrl+Q'
        exit_act = QAction('Exit', self.main_window)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(self.close_application)
        self.main_window.addAction(exit_act)

        self.connect_buttons()
        self.setup_team_selector()

        status_colors = {True: QColor(0, 180, 0), False: QColor(200, 0, 0)}
        self.connection_indicator = StatusIndicator(
            self.ConnectStatus, status_colors)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def scale_window(self):
        """Resize and move the window to handle different dpi screens"""
        available_geometry = QApplication.desktop().availableGeometry()

        scaled_height = available_geometry.height() * 0.35
        scaled_width = available_geometry.width() * 0.5

        scaled_geometry = QRect(
            (available_geometry.width() - scaled_width) / 2,
            (available_geometry.height() - scaled_height) / 2,
            scaled_width, scaled_height)

        self.main_window.setGeometry(scaled_geometry)

    def connect_buttons(self):
        """Connect buttons to handler functions"""

        # Mapping between mode buttons and mode string to put in NetworkTables
        self.mode_names = {
            self.AutonomousModeButton: "autonomous",
            self.TeleopModeButton: "teleop",
            self.TestModeButton: "test"
        }
        self.mode_buttons = [self.AutonomousModeButton,
                             self.TeleopModeButton, self.TestModeButton]

        # Mapping between button and enabled(True)/disabled(False)
        self.enable_buttons_status = {
            self.EnableButton: True,
            self.DisableButton: False
        }
        self.enable_buttons = [self.EnableButton, self.DisableButton]

        self.AutonomousModeButton.clicked.connect(
            lambda: self.mode_button_press(self.AutonomousModeButton))
        self.TeleopModeButton.clicked.connect(
            lambda: self.mode_button_press(self.TeleopModeButton))
        self.TestModeButton.clicked.connect(
            lambda: self.mode_button_press(self.TestModeButton))

        self.EnableButton.clicked.connect(
            lambda: self.enabled_button_press(self.EnableButton))
        self.DisableButton.clicked.connect(
            lambda: self.enabled_button_press(self.DisableButton))

    def setup_team_selector(self):
        """Setup the team selector spinbox"""
        self.TeamNumberSelector.setValue(
            self.config.team_number)

        self.UpdateTeamButton.clicked.connect(
            lambda: self.team_selector_update(
                self.TeamNumberSelector.value())
        )

    def update(self):
        """Update driver station"""

        # Update connection indicator
        self.connection_indicator.update(self.network.connected())

        # Set joystick data in NetworkTables
        self.joysticks.update()

        for joystick_num in range(self.joysticks.get_num_joysticks()):
            joy_data = self.joysticks.get_joystick(joystick_num)

            for index, value in enumerate(joy_data["axes"]):
                self.network.set_joystick_axis_value(
                    joystick_num, index, value)

            for index, value in enumerate(joy_data["buttons"]):
                self.network.set_joystick_button_value(
                    joystick_num, index, value)

    def mode_button_press(self, pressed_button):
        """Event handler for mode button press

        Sets mode buttons to checked/unchecked as if they were radio buttons.
        Updates game mode in NetworkTables.
        """
        for mode_button in self.mode_buttons:
            if mode_button == pressed_button:
                mode_button.setChecked(True)
                self.network.set_game_mode(self.mode_names[mode_button])
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
                self.network.set_enabled(self.enable_buttons_status[button])
            else:
                button.setChecked(False)

    def team_selector_update(self, new_team_number):
        """Update team number button event handler

        Updates team number with current value of team number spinbox,
        connects NetworkTables to correct robot.
        """
        self.config.team_number = str(
            new_team_number)

        self.network.change_server(new_team_number)

    def close_application(self):
        """Cleanup and close application"""
        self.timer.stop()
        self.main_window.close()
        self.joysticks.quit()
        self.config.save_config()
        self.network.shutdown()


def main(server_ip):
    """Main entry point for driver station"""
    joysticks = Joysticks(pygame)
    config = DriverStationConfig('ds_config.cfg')
    network = Network(networktables.NetworkTables, 'driver_station', server_ip)

    if not server_ip:
        server_ip = config.team_number
        print("Connecting to robot: " + server_ip)
    else:
        print("Connecting to: " + server_ip)

    app = QApplication(sys.argv)
    window = QMainWindow()
    driver_station = PyDriverStation(window, network, config, joysticks)
    window.show()

    try:
        return app.exec_()
    except KeyboardInterrupt:
        driver_station.close_application()
        print("\n\nExiting...\n\n")
        return 0


if __name__ == '__main__':
    try:
        SERVER_IP = sys.argv[1]
    except IndexError:
        SERVER_IP = None

    sys.exit(main(SERVER_IP))
