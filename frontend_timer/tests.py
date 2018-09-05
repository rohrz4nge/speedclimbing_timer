from communication import IO
from display import Display
from timer import Timer
from main import Main

from unittest.mock import patch, call
import unittest

""" Communication tests """
# mocking the library
RPi = unittest.mock.MagicMock()
serial = unittest.mock.MagicMock()
modules = {
    "RPi": RPi,
    "RPi.GPIO": RPi.GPIO,
    "serial": serial
}
patcher = unittest.mock.patch.dict("sys.modules", modules)
patcher.start()


class IOTestCase(unittest.TestCase):
    serial_port, button_pin, serial_indicator = "None", 0, 1
    gpio_alternator, serial_alternator = True, True

    def input_side_effect(self):
        self.gpio_alternator = not self.gpio_alternator
        return self.gpio_alternator

    def serial_side_effect(self):
        self.serial_alternator = not self.serial_alternator

    def setUp(self):
        self.gpio_set_mode = patch.object(RPi.GPIO, "setmode")
        self.gpio_setup = patch.object(RPi.GPIO, "setup")
        self.gpio_input = patch.object(RPi.GPIO, "input", side_effect=self.input_side_effect)
        self.gpio_bcm = patch.object(RPi.GPIO, "BCM")
        self.gpio_in = patch.object(RPi.GPIO, "IN")
        self.serial = patch("serial.Serial")
        self.serial_open = patch.object(serial.Serial, "open")
        self.serial_readline = patch.object(serial.Serial, "readline", return_value=b"abc123")
        self.serial_is_open = patch.object(serial.Serial, "is_open", side_effect=self.serial_side_effect)

    def test_init(self):
        with self.serial_open, self.serial_readline, self.serial_is_open:
            x = serial.Serial(1)
            print(self.serial.assert_called_with(1))
            print(x.open(), x.is_open(), x.readln())
        with self.gpio_set_mode, self.gpio_setup, self.gpio_input, self.gpio_bcm, self.serial_open, self.serial_is_open, self.serial_readln:
            IO(self.serial_port, self.serial_indicator, self.button_pin)
            self.gpio_set_mode.assert_called_with(self.gpio_bcm)
            self.gpio_setup.assert_called_with(self.serial_indicator, self.gpio_in)
            self.serial_open.assert_called_with(self.serial_port, 9600, timeout=1)

    def test_read_serial_indicator(self):
        with self.gpio_set_mode, self.gpio_setup, self.gpio_input, self.gpio_bcm, self.serial_open, self.serial_is_open, self.serial_readln:
            io = IO(self.serial_port, self.serial_indicator, self.button_pin)
            self.assertEqual(io.read_serial_indicator(), self.gpio_alternator)

    def test_read_button(self):
        with self.gpio_set_mode, self.gpio_setup, self.gpio_input, self.gpio_bcm, self.serial_open, self.serial_is_open, self.serial_readln:
            io = IO(self.serial_port, self.serial_indicator, self.button_pin)
            self.assertEqual(io.read_button(), self.gpio_alternator)


""" Display tests """

""" Timer tests """

""" Main tests """
