
class MinMaxLim:
    def __init__(self, margin=0.1):
        self.margin = margin
        self.min = None
        self.max = None

    def update(self, new_value):
        if self.min is None:
            self.min = new_value
            self.max = new_value
        else:
            self.min = min(self.min, new_value)
            self.max = max(self.max, new_value)

    def get_lim(self):
        if self.max == self.min:
            distance = abs(self.max)
        else:
            distance = self.max - self.min

        extra = self.margin * distance
        return (self.min - extra, self.max + extra)

