class Display:
    def __init__(self):
        self.time = 0
        self.scores, self.latest = [], 0

    # TODO
    def communication_error(self, inaccurate_time):
        pass

    # TODO
    def show_scores(self):
        best_5 = self.scores[:5]

    def update_scores(self, new_score):
        self.latest = new_score
        self.scores.append(new_score)
        self.scores.sort()

    # TODO
    def show_time(self):
        pass

    # TODO
    def update_time(self, time):
        self.time = time

    def reset(self):
        self.time = 0
