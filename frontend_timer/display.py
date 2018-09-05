import tkinter as tk
from timer import Timer
from os import _exit
from typing import Tuple
# for testing only
from random import randint

test = False


class Display:
    def __init__(self, dark_theme=False):
        self.false_start_first, self.false_start_alternator, self.false_start_timer = True, True, 0
        self.timer = Timer()
        self.time = "0.00"
        self.best_5, self.last_5 = [], []

        # tk stuff
        window_width, window_height = 1800, 1000
        headline_font = ("Roboto Mono Regular", 84)
        score_font = ("Roboto Regular", 84)
        if dark_theme:
            self.headline_theme, self.fg_theme, self.bg_theme = '#%02x%02x%02x' % (109, 194, 146), '#%02x%02x%02x' % (
                250, 250, 250), '#%02x%02x%02x' % (41, 44, 50)
        else:
            self.headline_theme, self.fg_theme, self.bg_theme = '#00e676', '#263238', '#%02x%02x%02x' % (250, 250, 250)
        self.false_start_theme = '#e14c1d'

        self.state = False
        self.tk = tk.Tk()
        self.tk.configure(background=self.bg_theme)
        self.text_canvas = tk.Canvas(self.tk, width=window_width, height=window_height, bd=0, background=self.bg_theme,
                                     highlightthickness=0)
        self.text_canvas.pack()

        # text fields
        # time display
        self.time_text = self.text_canvas.create_text(window_width / 15, window_height / 2, text="text", anchor="w",
                                                      font=("Calibri", 150), fill=self.fg_theme)
        self.text_canvas.itemconfig(self.time_text, text="0.00")

        # best scores
        self.best_head = self.text_canvas.create_text(window_width / 1.4773, window_height / 12, text="Best",
                                                      anchor="ne",
                                                      justify="right", font=headline_font, fill=self.headline_theme)
        self.best_text = self.text_canvas.create_text(window_width / 1.45, window_height / 3.8, text="text",
                                                      anchor="ne",
                                                      justify="right", font=score_font, fill=self.fg_theme)
        self.text_canvas.itemconfig(self.best_text, text="1.00\n2.00\n10.00\n100.00\n999.00")

        # latest scores
        self.last_head = self.text_canvas.create_text(window_width / 1.1423, window_height / 12, text="Last",
                                                      anchor="ne",
                                                      justify="right", font=headline_font, fill=self.headline_theme)
        self.last_text = self.text_canvas.create_text(window_width / 1.115, window_height / 3.8, text="text",
                                                      anchor="ne",
                                                      justify="right", font=score_font, fill=self.fg_theme)
        self.text_canvas.itemconfig(self.last_text, text="1.00\n2.00\n10.00\n100.00\n999.99")
        # self.toggle_fullscreen()
        self.tk.update()

        self.tk.bind("<Escape>", lambda x: self.destroy())
        self.tk.bind("f", lambda x: self.toggle_fullscreen())

    """ binded functions """

    def destroy(self):
        self.tk.destroy()
        _exit(1)

    def toggle_fullscreen(self):
        self.state = not self.state
        self.tk.attributes('-fullscreen', self.state)

    """ display functions """

    # given a canvas and a (formatted) string, this function updates the displayed text of the text_canvas to new_text
    def change_text(self, text_canvas: int, new_text: str):
        self.text_canvas.itemconfig(text_canvas, text=new_text)
        self.tk.update()

    # TODO
    def communication_error(self, inaccurate_time: float):
        pass

    def update_scores(self, new_score: float):
        # adding to the last scores
        self.last_5 = self.last_5[:4]
        self.last_5 = [round(new_score, 2)] + self.last_5
        # adding to the best scores
        self.best_5.append(round(new_score, 2))
        self.best_5.sort(reverse=False)
        self.best_5 = self.best_5[:5]
        self.change_text(self.last_text, "\n".join("{:.2f}".format(i) for i in self.last_5))
        self.change_text(self.best_text, "\n".join("{:.2f}".format(i) for i in self.best_5))

    # given a time in ns, this function updates the time in the tk window
    def update_time(self, time: float):
        self.time = "{:.2f}".format(time)
        self.change_text(self.time_text, self.time)

    # TODO
    def abort_timer(self):
        pass

    # function letting the display background blink 3 seconds, returns True if 3 seconds have passed, otherwise False
    def false_start(self):
        if self.false_start_first:
            self.false_start_first = False
            self.timer.start()
            self.false_start_timer = 0
        if self.timer.countdown_is_over(self.false_start_timer * 500000000):
            self.false_start_timer += 1
            self.change_false_start_bg()
        return True if self.timer.countdown_is_over(3000000000) else False

    # TODO
    def timeout(self):
        pass

    # function changing the background color based on the corrent color (used for blinking)
    def change_false_start_bg(self):
        if self.false_start_alternator:
            self.change_bg(self.false_start_theme)
        else:
            self.change_bg(self.bg_theme)
        self.false_start_alternator = not self.false_start_alternator

    # function taking hex or rgb colors, sets the background color to the given color, default color: self.bg_theme
    def change_bg(self, hex_color: str = None, rgb_colors: Tuple[int, int, int] = None):
        if hex_color:
            self.text_canvas.configure(background=hex_color)
        elif rgb_colors:
            self.text_canvas.configure(background='#%02x%02x%02x' % rgb_colors)
        # default bg
        else:
            self.text_canvas.configure(background=self.bg_theme)

    def reset(self):
        self.change_bg()
        self.false_start_first, self.false_start_alternator, self.false_start_timer = True, True, 0
        self.update_time(0.00)

    def mainloop(self):
        i = 1
        x = True
        while True:
            self.update_scores(randint(580, 9999) / 100)
            if x:
                if self.false_start():
                    x = False
                    self.reset()
            self.tk.update()
            i += 1


if __name__ == '__main__':
    display = Display()
    display.mainloop()
