import serial
import rpi.gpio as gpio


class IO:
    def __init__(self, serial_port, serial_indicator, button_pin):
        self.serial_port, self.serial_indicator, self.button_pin = serial_port, serial_indicator, button_pin
        # serial stuff
        self.serial = serial.Serial(serial_port, 9600, timeout=1)
        self.serial.open()
        # gpio stuff
        gpio.setmode(gpio.BCM)
        gpio.setup(serial_indicator, gpio.IN)
        gpio.setup(button_pin, gpio.IN)

    def read_serial_indicator(self):
        return gpio.input(self.serial_indicator)

    def read_button(self):
        return gpio.input(self.button_pin)

    # function returning whether a connection over serial was made
    def serial_available(self):
        return self.serial.in_waiting == 1

    # TODO stripping the string from anything but the result
    # function reading the serial, returns a string containing only the result
    def read_serial(self):
        # why?
        if not self.serial.is_open():
            self.serial.open()

        line = self.serial.readline()
        print(line)
        return line
