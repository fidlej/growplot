#!/usr/bin/env python
"""Usage: %prog FILENAME
Plots values from the possibly still growing file.
Each value is expected to be on a new line.
"""

import optparse

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot

from growplot import reading

DEFAULTS = {
        "delimiter": "\n",
        "check_millis": "200",
        }


def _parse_args():
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-d", "--delimiter",
            help="delimiter to use instead of %r" % DEFAULTS["delimiter"])
    parser.add_option("--check_millis", type=int,
            help=("delay between checks for new values (default=%s)" %
                DEFAULTS["check_millis"]))
    parser.set_defaults(**DEFAULTS)

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("a single input file is required")

    return options, args[0]


class Animator:
    def __init__(self, figure, data_holder, check_millis):
        self.figure = figure
        self.data_holder = data_holder
        self.check_millis = check_millis

        self.ax = figure.add_subplot(111)
        (self.line,) = self.ax.plot([], [],
                linestyle="steps-mid")

    def start_animation(self):
        self._animate()

    def _animate(self):
        if self.data_holder.update_values():
            self.ax.set_xlim(self.data_holder.get_xlim())
            self.ax.set_ylim(self.data_holder.get_ylim())
            self.line.set_data(self.data_holder.get_xvalues(),
                    self.data_holder.get_yvalues())

            self.figure.canvas.draw()

        self.figure.canvas.manager.window.after(self.check_millis,
                self._animate)


def main():
    options, filename = _parse_args()
    reader = reading.TailReader(filename, delimiter=options.delimiter)
    data_holder = reading.DataHolder(reader)

    figure = pyplot.figure()
    animator = Animator(figure, data_holder, check_millis=options.check_millis)
    animator.start_animation()
    pyplot.show()


if __name__ == "__main__":
    main()
