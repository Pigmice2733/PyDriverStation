# Pigmice Python DriverStation
This is a project to create a Python-based driver station for our minibot Raspberry Pi framework.
This may eventually become a cross-platform replacement for the DriverStation.

## Dependencies
The driver station uses Qt as the GUI framework, this was chosen because it is a well maintained and documented cross-platform toolkit with bindings for Python. NetworkTables is used for commnuicaing with the robot over wifi, NetworkTables is used for compatibility reasons with RobotPy and WPILib. Pygame is used for interfacing with ubs joystick controllers. `pynetworktables`, `pyqt5` and `pygame` are all needed to run the driver station, these can all be installed via `pip`. `pyqt5_tools` is also needed to build the UI files, and is also installable from pip.

## Installing, building and running
1. Clone this repository
2. Install `pynetworktables`, `pyqt5` and `pygame` using `pip install <package>`
3. Install `pyqt5_tools` with `pip install pyqt5_tools`
4. Build the UI - `pyuic5 .\driverstation_ui\driverstation_ui.ui -o .\driverstation_ui\driverstation_ui.py`
5. To run, use `python .\py_driverstation.py`