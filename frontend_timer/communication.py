import serial
import rpi.gpio as gpio
import sqlite3


class IO:
    def __init__(self, serial_port: str, serial_indicator: int, button_pin: int):
        self.serial_port, self.serial_indicator, self.button_pin = serial_port, serial_indicator, button_pin
        # serial stuff
        self.serial = serial.Serial(serial_port, 9600, timeout=1)
        self.serial.open()
        # gpio stuff
        gpio.setmode(gpio.BCM)
        gpio.setup(serial_indicator, gpio.IN)
        gpio.setup(button_pin, gpio.IN)
        # sqlite stuff
        self.database = sqlite3.connect("speedclimbing_scores.db")
        self.cursor = self.database.cursor()
        self.cursor.execute("CREATE TABLE if not exists results(result real, name text)")
        self.database.commit()

    def read_serial_indicator(self) -> bool:
        return gpio.input(self.serial_indicator)

    def read_button(self) -> bool:
        return gpio.input(self.button_pin)

    # function returning whether a connection over serial was made
    def serial_available(self) -> bool:
        return self.serial.in_waiting == 1

    # TODO stripping the string from anything but the result
    # function reading the serial, returns a string containing only the result
    def read_serial(self) -> str:
        # why?
        if not self.serial.is_open():
            self.serial.open()

        line = self.serial.readline().decode("utf-8")
        print(line)
        return line

    def write(self, result: float, name: str = "unknown"):
        self.cursor.execute("INSERT INTO results VALUES (:result, :name)", {"result": result, "name": name})
        self.database.commit()
        # self.cursor.execute("SELECT * FROM results")
        # print(self.cursor.fetchall())
