from time import monotonic_ns

"""
A (not incredibly accurate) timer utility using monotonic_ns introduced in Python 3.7
"""


class Timer:
    def __init__(self):
        self.start_time, self.result = 0, 0

    def start(self):
        self.start_time = monotonic_ns()

    def get_current_time(self):
        return monotonic_ns() - self.start_time

    def countdown_is_over(self, countdown_time):
        return self.get_current_time() >= countdown_time

    def stop(self):
        self.result = monotonic_ns() - self.start_time

    def get_inaccurate_result(self):
        return self.result

    def reset(self):
        self.result = 0
