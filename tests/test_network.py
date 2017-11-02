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
        """Test that `change_server` correctly switches NetworkTables
         server"""
        networktables_mock = unittest.mock.Mock()

        network_instance = network.Network(networktables_mock, None, None)
        network_instance.change_server("localhost")

        # Make sure Networktables was shutdown before network change
        self.assertTrue(networktables_mock.shutdown.called)
        # Make sure new network server ip is correct
        networktables_mock.initialize.assert_called_with(server="localhost")

    def test_table_reference(self):
        """Test that the NetworkTable reference is a reference
         to a table on the new network after a `change_server`"""
        networktables_mock = unittest.mock.Mock()
        table_mock = unittest.mock.Mock()
        # When table is gotten from first network, table will be None,
        #  from second network will return table_mock
        networktables_mock.getTable.side_effect = [None, table_mock]

        network_instance = network.Network(networktables_mock, None, None)

        # Test initial Network.table value
        self.assertTrue(network_instance.table is None)

        network_instance.change_server("localhost")

        # Test final value of Network.table
        self.assertTrue(network_instance.table == table_mock)

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
