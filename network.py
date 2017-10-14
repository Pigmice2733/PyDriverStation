"""Networking for driver station"""


class Network:
    """NetworkTables wrapper for driver station"""

    def __init__(self, networktables, table_name, server_ip):
        """Initialize network

        `networktables`: Reference to NetworkTables or mock of NetworkTables
        `table_name` - `str`: Name of NetworkTables table to communicate over
        `server_ip` - `str`: Ip of NetworkTables server to connect to
        """
        self.networktables = networktables

        self.table_name = table_name

        self.networktables.initialize(server_ip)
        self.table = self.networktables.getTable(self.table_name)

    def change_server(self, new_ip):
        """Connect to different NetworkTables server

        `new_ip`: IP of new NetworkTables server to connect to
        """
        self.networktables.shutdown()
        self.networktables.initialize(server=new_ip)

    def connected(self):
        """Is the network connected
        - with NetworkTables returns `True` if it is
         connected to at least one other
          NetworkTables instance
        """
        return self.networktables.isConnected()

    def set_joystick_axis_value(self, joystick_number: int, axis_number: int, value: float):
        """Set a NetworkTable value. Set the joystick axis specified
        by `joystick` and `axis` to `value`.
        """
        key = "/joystick-" + str(joystick_number) + "/axis-" + str(axis_number)
        self.table.putNumber(key, value)

    def set_joystick_button_value(self, joystick_number: int, button_number: int, value: bool):
        """Set a NetworkTable value. Set the joystick button specified
        by `joystick` and `button` to `value`.
        """
        key = "/joystick-" + str(joystick_number) + \
            "/button-" + str(button_number)
        self.table.putBoolean(key, value)

    def set_game_mode(self, mode: str):
        """Set the current game mode in NetworkTables"""
        key = "/mode"
        self.table.putString(key, mode)

    def set_enabled(self, enabled: bool):
        """Set enabled status in NetworkTables"""
        key = "/enabled"
        self.table.putBoolean(key, enabled)

    def shutdown(self):
        """Shutdown and release resources"""
        self.networktables.shutdown()
