# Pigmice Python DriverStation
This is a project to create a Python-based driver station for our Raspberry Pi minibots.

## Dependencies
The driver station uses Qt as the GUI framework, this was chosen because it is a well maintained and documented cross-platform toolkit with bindings for Python. NetworkTables is used for communicating with the robot over wifi, NetworkTables is used for compatibility reasons with RobotPy and WPILib. Pygame is used for interfacing with usb joystick controllers. `pynetworktables`, `pyqt5` and `pygame` are all needed to run the driver station, these can all be installed via `pip`. `pyqt5_tools` is also needed to build the UI files, and is also installable from pip.

## Installing, building and running

Make sure you have Python 3 installed as well as `pip3` before you begin. You can check whether you have Python installed (and the version) by running `python --version` in the terminal.

1. Clone this repository
2. Install `pipenv` using `pip3 install pipenv`
3. Install dependencies with `pipenv install`

To activate the `pipenv` shell environment so all the dependencies are available, run `pipenv shell`. If you are using Windows and this command fails with something like 'Please ensure that the SHELL environment variable is set before activating shell.', use `pipenv shell --fancy` instead.

You must build the UI before you can run the driver station, use
```
pyuic5 .\driverstation_ui\driverstation_ui.ui -o .\driverstation_ui\driverstation_ui.py
```
to do this. The UI must be rebuilt every time it changes. You may have to activate the `pipenv` shell before this will work.

To run, first activate the shell. Then use `python .\py_driverstation.py` to launch the driver station.

**Note:** For now, the driver station must be started with `python .\py_driverstation.py <remote-ip>`, where `remote-ip` is the ip of the robot you wish to connect to. For testing on the same computer, use `localhost`.