#!/usr/bin/env python
"""Usage: growplot.py FILENAME
Plots values from the possibly still growing file.
Each value is expected to be on a new line.
"""

import sys

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot

from growplot.reading import TailReader


class Animator:
    def __init__(self, new_value_reader, figure):
        self.figure = figure
        self.ax = figure.add_subplot(111)
        self.xvalues = []
        self.yvalues = []
        self.reader = new_value_reader
        self.counter = 0
        self.timeout_millis = 200

        (self.line,) = self.ax.plot(self.xvalues, self.yvalues,
                linestyle='steps')

    def animate(self):
        values = self.reader.nextvalues()
        if values:
            for value in values:
                self.counter += 1
                self.xvalues.append(self.counter)
                self.yvalues.append(value)

            self.ax.set_xlim(0, self.xvalues[-1])
            self.ax.set_ylim(0, self.yvalues[-1])
            self.line.set_data(self.xvalues, self.yvalues)

            self.figure.canvas.draw()

        self.figure.canvas.manager.window.after(self.timeout_millis,
                self.animate)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print >>sys.stderr, __doc__
        sys.exit(1)

    filename = args[0]
    reader = TailReader(filename)

    figure = pyplot.figure()
    animator = Animator(reader, figure)
    animator.animate()
    pyplot.show()


if __name__ == "__main__":
    main()
