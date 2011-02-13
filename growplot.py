#!/usr/bin/env python

#BACKEND = "TkAgg"
BACKEND = "GTKAgg"

import matplotlib
matplotlib.use(BACKEND)

from matplotlib import pyplot

import time

class Animator:
    def __init__(self, figure):
        self.figure = figure
        self.ax = figure.add_subplot(111)
        self.line = None
        self.xvalues = []
        self.yvalues = []
        self.counter = 0

    def animate(self):
        for i in xrange(100):
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
            time.sleep(1)


def main():
    #TODO: try it with gtk
    figure = pyplot.figure()
    animator = Animator(figure)

    if BACKEND == "TkAgg":
        figure.canvas.manager.window.after(100, animator.animate)
    else:
        import gobject
        gobject.idle_add(animator.animate)

    pyplot.show()



main()
