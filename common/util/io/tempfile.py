class TempFile:
    BIN_MODE = "b"
    STR_MODE = "s"

    def __init__(self, mode="b"):
        self.data = b"" if mode == self.BIN_MODE else ""
        self.mode = mode

    def write(self, d: bytes):
        if self.mode == self.STR_MODE:
            if isinstance(d, bytes):
                d = d.decode()
        else:
            if isinstance(d, str):
                d = d.encode()

        self.data += d
