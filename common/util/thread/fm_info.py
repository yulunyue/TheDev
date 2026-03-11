from types import FrameType


class FmInfo:
    def __init__(self, frame) -> None:
        self.frame: FrameType = frame

    def get_local_self(self):
        return self.frame.f_locals["self"]
