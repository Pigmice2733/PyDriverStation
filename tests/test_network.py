"""Test module for `network.py`"""

import unittest
import unittest.mock

import network


class TestNetwork(unittest.TestCase):
    """Test class for `Network`"""

    def test_connected(self):
        """Test that `connected` correctly reports connection status"""
        networktables_mock = unittest.mock.Mock()
        networktables_mock.isConnected.side_effect = [True, False]

        network_instance = network.Network(networktables_mock, None, None)
        self.assertTrue(network_instance.connected())
        self.assertFalse(network_instance.connected())

    def test_change_server(self):
        """Test whether `change_server` correctly switches NetworkTables server"""
        networktables_mock = unittest.mock.Mock()

        network_instance = network.Network(networktables_mock, None, None)
        network_instance.change_server("localhost")

        self.assertTrue(networktables_mock.shutdown.called)
        networktables_mock.initialize.assert_called_with(server="localhost")

    def test_set_game_mode(self):
        """Test whether `set_game_mode` correctly sets game mode"""
        networktables_mock = unittest.mock.Mock()
        table_mock = unittest.mock.Mock()
        networktables_mock.getTable.return_value = table_mock

        network_instance = network.Network(networktables_mock, None, None)

        network_instance.set_game_mode("autonomous")
        table_mock.putString.assert_called_with("/mode", "autonomous")

        network_instance.set_game_mode("test")
        table_mock.putString.assert_called_with("/mode", "test")

    def test_set_enabled(self):
        """Test whether `set_enabled` correctly sets enalbed/disabled status"""
        networktables_mock = unittest.mock.Mock()
        table_mock = unittest.mock.Mock()
        networktables_mock.getTable.return_value = table_mock

        network_instance = network.Network(networktables_mock, None, None)

        network_instance.set_enabled(True)
        table_mock.putBoolean.assert_called_with("/enabled", True)

        network_instance.set_enabled(False)
        table_mock.putBoolean.assert_called_with("/enabled", False)

    def test_shutdown(self):
        """Test that `shutdown` correctly shutsdown NetworkTables"""
        networktables_mock = unittest.mock.Mock()
        table_mock = unittest.mock.Mock()
        networktables_mock.getTable.return_value = table_mock

        network_instance = network.Network(networktables_mock, None, None)

        network_instance.shutdown()
        self.assertTrue(networktables_mock.shutdown.called)

    def test_set_joystick_axis_value(self):
        """Test that `set_joystick_axis_value` works right"""
        networktables_mock = unittest.mock.Mock()
        table_mock = unittest.mock.Mock()
        networktables_mock.getTable.return_value = table_mock

        network_instance = network.Network(networktables_mock, None, None)

        network_instance.set_joystick_axis_value(2, 0, 0.45)
        table_mock.putNumber.assert_called_with("/joystick-2/axis-0", 0.45)

        network_instance.set_joystick_axis_value(0, 3, -1.0)
        table_mock.putNumber.assert_called_with("/joystick-0/axis-3", -1.0)

    def test_set_joystick_button_value(self):
        """Test that `set_joystick_axis_value` performs correctly"""
        networktables_mock = unittest.mock.Mock()
        table_mock = unittest.mock.Mock()
        networktables_mock.getTable.return_value = table_mock

        network_instance = network.Network(networktables_mock, None, None)

        network_instance.set_joystick_button_value(1, 0, 1)
        table_mock.putBoolean.assert_called_with("/joystick-1/button-0", 1)

        network_instance.set_joystick_button_value(0, 3, 0)
        table_mock.putBoolean.assert_called_with("/joystick-0/button-3", 0)
