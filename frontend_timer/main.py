from timer import Timer
from display import Display
from communication import IO

idling, countdown, countdown_timer, waiting, result, reset = 0, 1, 2, 3, 4, 5


class Main:
    def __init__(self):
        # stuff for the Arduino communication
        self.serial_port, self.serial_indicator, self.button_pin = "/dev/0", 4, 1
        self.io = IO(self.serial_port, self.serial_indicator, self.button_pin)
        self.result = 0
        # stuff for the display
        self.display = Display()
        # stuff for the timer
        self.timer = Timer()
        self.countdown_time, self.countdown_timer_time = 2000000000, 100000000
        # stuff for the main
        self.database_path = "database.csv"
        self.result_dict = {"abort": self.display.abort_timer, "false_start": self.display.false_start,
                            "timeout": self.display.timeout}
        # stuff for the fsm
        self.prev, self.current = 0, 0
        self.states = [self.idling, self.countdown, self.countdown_timer, self.waiting, self.read_result, self.reset]
        self.mainloop()

    # function converting ns to seconds
    @staticmethod
    def safediv(time):
        return time / 1000000000 if time > 0 else 0

    # given a state, this function changes the states accordingly
    def change_state(self, next_state):
        self.prev = self.current
        self.current = next_state

    # given the index of the current state, changes self.prev, to the same as self.current, if the state stayed the same
    def same_state(self):
        self.prev = self.current

    def check_button_serial(self):
        if self.io.read_button():
            self.change_state(reset)
        if self.io.read_serial_indicator():
            self.timer.stop()
            self.change_state(result)
        else:
            self.same_state()

    """ States """

    def idling(self):
        if self.io.read_button():
            self.change_state(countdown)
        else:
            self.same_state()

    def countdown_states(self, countdown_time, next_state):
        # initializing timer
        if self.prev != self.current:
            self.timer.start()
        # transitions
        if self.timer.countdown_is_over(countdown_time):
            self.change_state(next_state)
        else:
            self.check_button_serial()

    def countdown(self):
        self.countdown_states(self.countdown_time, countdown_timer)

    def countdown_timer(self):
        self.countdown_states(self.countdown_timer_time, waiting)

    def waiting(self):
        self.display.update_time(self.timer.get_current_time())
        # transitions
        self.check_button_serial()

    def read_result(self):
        if self.io.serial_available():
            self.result = self.io.read_serial()
            # checking if the result is abort, falsestart or timeout
            if self.result in self.result_dict:
                self.result_dict[self.result]()
            else:
                self.result = self.safediv(int(self.result))
                self.display.update_scores(self.result)
                self.io.write(self.result)
        else:
            self.display.communication_error(self.timer)
        self.change_state(reset)

    def reset(self):
        self.display.reset()
        self.result = 0
        self.change_state(idling)

    """ loop functions """

    # based on the current state index, this function executes the current state
    def transitions(self):
        print(self.current)
        self.states[self.current]()

    # an infinite loop calling the states
    def mainloop(self):
        while True:
            self.transitions()


if __name__ == "__main__":
    main = Main()
