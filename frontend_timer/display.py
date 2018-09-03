import tkinter as tk
from os import _exit


class Display:
    def __init__(self):
        self.time = 0
        self.best_5, self.last_5 = [], []

        # tk stuff
        window_width, window_height = 1500, 1000
        score_font = ("Calibri", 84)
        fg_theme, bg_theme = "grey", "white"
        self.state = False
        self.tk = tk.Tk()
        self.tk.configure(background=bg_theme)
        self.text_canvas = tk.Canvas(self.tk, width=window_width, height=window_height, bd=0, background=bg_theme,
                                     highlightthickness=0)
        self.text_canvas.pack()

        # text fields
        # time display
        self.time_text = self.text_canvas.create_text(window_width / 15, window_height / 2, text="text", anchor="w",
                                                      font=("Calibri", 150), fill=fg_theme)
        self.text_canvas.itemconfig(self.time_text, text="0.00")

        # best scores
        self.best_text = self.text_canvas.create_text(window_width / 1.8, window_height / 4.5, text="text", anchor="nw",
                                                      justify="right", font=score_font, fill=fg_theme)
        self.text_canvas.itemconfig(self.best_text, text="1.00\n2.00\n10.00\n100.00\n999.00")

        # latest scores
        self.last_text = self.text_canvas.create_text(window_width / 1.26, window_height / 4.5, text="text",
                                                      anchor="nw",
                                                      justify="right", font=score_font, fill=fg_theme)
        self.text_canvas.itemconfig(self.last_text, text="1.00\n2.00\n10.00\n100.00\n999.99")
        # self.toggle_fullscreen()
        self.tk.update()

        self.tk.bind("<Escape>", self.destroy)
        self.tk.bind("f", self.toggle_fullscreen)

    """ binded functions """
    def destroy(self, tk_param: object):
        self.tk.destroy()
        _exit(1)

    def toggle_fullscreen(self, tk_param: object):
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
        self.last_5.append(new_score)
        # adding to the best scores
        self.best_5.append(new_score)
        self.best_5.sort()
        self.best_5 = self.best_5[:5]

        self.change_text(self.last_text, "\n".join(str(i) for i in self.last_5))
        self.change_text(self.best_text, "\n".join(str(i) for i in self.best_5))

    # given a time in ns, this function updates the time in the tk window
    def update_time(self, time: float):
        self.time = round(time, 2)
        self.change_text(self.time_text, str(self.time))

    # TODO
    def abort_timer(self):
        pass

    # TODO
    def false_start(self):
        pass

    # TODO
    def timeout(self):
        pass

    def reset(self):
        self.update_time(0)


if __name__ == '__main__':
    display = Display()
    display.tk.mainloop()
