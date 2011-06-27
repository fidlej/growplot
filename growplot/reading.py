
import os
import array

from growplot import limiting

class DataHolder:
    def __init__(self, reader, aggregator):
        self.reader = reader
        self.aggregator = aggregator
        self.xvalues = array.array("f")
        self.yvalues = array.array("f")
        self.xlim = limiting.MinMaxLim(margin=0)
        self.ylim = limiting.MinMaxLim()

    def update_values(self):
        """Returns True if there is a change.
        """
        pairs = self.reader.nextvalues()
        if not pairs:
            return False

        for pair in pairs:
            if len(pair) == 1:
                x = 1 + len(self.xvalues)
                value = pair[0]
            else:
                x, value = pair

            value = self.aggregator.aggregate(value)
            self.xvalues.append(x)
            self.yvalues.append(value)
            self.xlim.update(x)
            self.ylim.update(value)

        return True

    def get_xvalues(self):
        return self.xvalues

    def get_yvalues(self):
        return self.yvalues

    def get_xlim(self):
        return self.xlim.get_lim()

    def get_ylim(self):
        return self.ylim.get_lim()



class TailReader:
    """A reader of values from the tail of a file.
    """
    def __init__(self, filename, delimiter="\n"):
        self.fd = os.open(filename, os.O_RDONLY|os.O_NONBLOCK)
        self.delimiter = delimiter
        self.remainder = ""

    def nextvalues(self):
        """Returns next found values from the file.
        """
        data = self._read_available(self.fd)
        if not data:
            return []

        lines = (self.remainder + data).split(self.delimiter)
        self.remainder = lines[-1]
        pairs = []
        for line in lines[:-1]:
            xy = line.split(None, 1)
            pairs.append(tuple(float(value) for value in xy))
        return pairs

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

