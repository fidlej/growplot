#!/usr/bin/env python
"""Usage: %prog FILENAME
Plots values from the possibly still growing file.
Each value is expected to be on a new line.
"""

import sys
import optparse

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot

from growplot.reading import TailReader

DEFAULTS = {
        "delimiter": "\n",
        }


def _parse_args():
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-d", "--delimiter",
            help="delimiter to use instead of %r" % DEFAULTS["delimiter"])
    parser.set_defaults(**DEFAULTS)

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("a single input file is required")

    return options, args[0]


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
    options, filename = _parse_args()
    reader = TailReader(filename, delimiter=options.delimiter)

    figure = pyplot.figure()
    animator = Animator(reader, figure)
    animator.animate()
    pyplot.show()


if __name__ == "__main__":
    main()
