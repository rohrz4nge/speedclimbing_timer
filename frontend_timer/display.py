import tkinter as tk


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
        self.text_canvas = tk.Canvas(self.tk, width=window_width, height=window_height, bd=0, background=bg_theme, highlightthickness=0)
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

        self.toggle_fullscreen()
        self.tk.update()

    def toggle_fullscreen(self):
        self.state = not self.state
        self.tk.attributes('-fullscreen', self.state)

    def change_text(self, text_canvas, new_text):
        self.text_canvas.itemconfig(text_canvas, text=new_text)
        self.tk.update()

    # TODO
    def communication_error(self, inaccurate_time):
        pass

    def update_scores(self, new_score):
        # adding to the last scores
        self.last_5 = self.last_5[:4]
        self.last_5.append(new_score)
        # adding to the best scores
        self.best_5.append(new_score)
        self.best_5.sort()
        self.best_5 = self.best_5[:5]

        self.change_text(self.last_text, "\n".join(str(i) for i in self.last_5))
        self.change_text(self.best_text, "\n".join(str(i) for i in self.best_5))

        # actual gui updates

    # function converting ns to seconds
    def safediv(self):
        return self.time / 1000000000 if self.time > 0 else 0

    # given a time in ns, this function updates the time in the tk window
    def update_time(self, time):
        self.time = time
        self.change_text(self.time_text, round(self.safediv(), 2))

    def reset(self):
        self.update_time(0)


if __name__ == '__main__':
    display = Display()
