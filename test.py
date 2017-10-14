"""Test script for PyDriverStation"""

import unittest

def test():
    """Test entry point for driver station"""
    loader = unittest.TestLoader()
    driver_station_tests = loader.discover('.')
    test_runner = unittest.runner.TextTestRunner()
    test_runner.run(driver_station_tests)

if __name__ == '__main__':
    test()
