#!/usr/bin/env python

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot

class Animator:
    def __init__(self, figure):
        self.figure = figure
        self.ax = figure.add_subplot(111)
        self.line = None
        self.xvalues = []
        self.yvalues = []
        self.counter = 0

    def animate(self):
        print "i", self.counter
        self.counter += 1
        self.xvalues.append(self.counter)
        self.yvalues.append(self.counter**2)

        if self.line is None:
            (self.line,) = self.ax.plot(self.xvalues, self.yvalues,
                    linestyle='steps')
        else:
            self.ax.set_xlim(0, self.xvalues[-1])
            self.ax.set_ylim(0, self.yvalues[-1])
            self.line.set_data(self.xvalues, self.yvalues)

        self.figure.canvas.draw()
        self.figure.canvas.manager.window.after(1000,
                self.animate)


def main():
    figure = pyplot.figure()
    animator = Animator(figure)

    figure.canvas.manager.window.after(0, animator.animate)
    pyplot.show()



main()
