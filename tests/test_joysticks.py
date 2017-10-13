"""Test module for `joysticks.py`"""

import unittest
import unittest.mock

import joysticks


class TestJoysticks(unittest.TestCase):
    """Test class for `Joysticks`"""

    def test_get_num_joysticks(self):
        """Test whether `Joysticks.get_num_joysticks` reports
         the correct number of joysticks
        """
        pygame_mock = unittest.mock.Mock()
        pygame_mock.joystick.get_count.return_value = 4
        stick = joysticks.Joysticks(pygame_mock)
        num_sticks = stick.get_num_joysticks()
        self.assertEqual(num_sticks, 4)

    def test_update(self):
        """Test whether Joysticks correctly flushes
         pygame event queue on `update`
        """
        pygame_mock = unittest.mock.Mock()
        # Mock object must report a number of
        # joysticks for Joysticks to be initialized correctly
        pygame_mock.joystick.get_count.return_value = 0
        stick = joysticks.Joysticks(pygame_mock)
        stick.update()
        self.assertTrue(pygame_mock.event.get.called)

    def test_quit(self):
        """Ensure quit cleans up and releases all resources"""
        pygame_mock = unittest.mock.Mock()
        # Mock object must report a number of
        # joysticks for Joysticks to be initialized correctly
        pygame_mock.joystick.get_count.return_value = 0
        stick = joysticks.Joysticks(pygame_mock)
        stick.quit()
        self.assertTrue(pygame_mock.quit.called)

    def test_get_joystick(self):
        """Test `Joysticks.get_joystick`"""
        pygame_mock = unittest.mock.Mock()
        joystick_mock = unittest.mock.Mock()
        joystick_mock.get_numaxes.return_value = 3
        joystick_mock.get_numbuttons.return_value = 3
        joystick_mock.get_axis.side_effect = self.joystick_get_axis
        joystick_mock.get_button.side_effect = self.joystick_get_button
        pygame_mock.joystick.Joystick.return_value = joystick_mock
        # Mock object must report a number of
        # joysticks for Joysticks to be initialized correctly
        pygame_mock.joystick.get_count.return_value = 3
        stick = joysticks.Joysticks(pygame_mock)

        expected_joy_data = {
            'axes': [0.0, 1.0, -1.0],
            'buttons': [0, 1, 1]
        }

        # Make sure joystick is initialized before being used
        self.assertTrue(joystick_mock.init.called)

        with self.assertRaises(ValueError):
            stick.get_joystick(3)

        with self.assertRaises(ValueError):
            stick.get_joystick(-1)

        joy_data = stick.get_joystick(0)
        self.assertEqual(expected_joy_data, joy_data)

    def joystick_get_axis(self, axis):
        """Mock function for `pygame.joystick.get_axis`"""
        return [0.0, 1.0, -1.0][axis]

    def joystick_get_button(self, button):
        """Mock function for `oygame.joystick.get_button`"""
        return [0, 1, 1][button]
