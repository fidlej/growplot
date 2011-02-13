#!/usr/bin/env python

import os

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot


class TailReader:
    def __init__(self, filename):
        self.fd = os.open(filename, os.O_RDONLY|os.O_NONBLOCK)
        self.remainder = ""

    def nextvalues(self):
        """Returns next found values from the file.
        """
        data = self._read_available(self.fd)
        if not data:
            return []

        lines = (self.remainder + data).split("\n")
        self.remainder = lines[-1]
        return [float(line) for line in lines[:-1]]

    def _read_available(self, fd):
        """Reads all available bytes
        from the non-blocking fd.
        """
        buf = ""
        while True:
            try:
                bytes = os.read(fd, 8192)
                if len(bytes) == 0:
                    return buf

                buf += bytes
            except OSError, e:
                if e.errno == errno.EINTR:
                    continue
                elif e.errno == errno.EAGAIN:
                    return buf
                else:
                    raise


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
    reader = TailReader("data.log")
    import time
    while True:
        values = reader.nextvalues()
        print "values:", values
        time.sleep(1)

    return
    figure = pyplot.figure()
    animator = Animator(figure)

    figure.canvas.manager.window.after(0, animator.animate)
    pyplot.show()


if __name__ == "__main__":
    main()
