from pynput import keyboard
from common.util.export import get_log, Thread


class PynutUtil:
    def __init__(self):
        self.events = dict()

    @property
    def logger(self):
        return get_log("pynut")

    def register(self, key, call_back):
        self.events[key] = call_back
        return self

    def on_press(self, key):
        self.logger.debug(f"{key} press")
        return True

    def on_release(self, key):
        self.logger.debug(f"{key} release")
        return True

    def run(self):
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        ) as listener:
            listener.join()

    def start(self):
        Thread(target=self.run).start()
