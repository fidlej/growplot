
import os

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
