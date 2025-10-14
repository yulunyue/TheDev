from pynput import keyboard

from common.util.export import get_log, Thread


class KeyCode:
    CHAR_CTRL = "\x03"

    def __init__(self, k):
        if isinstance(k, keyboard.KeyCode):
            self.char, self.vk = k.char, k.vk
        else:
            self.char, self.vk = k.name, k.value.vk

    def is_ctrl_c(self):
        return self.char == KeyCode.CHAR_CTRL and self.vk == 67

    def __str__(self):
        return f"char:{self.char}; vk:{self.vk}"


class PynutUtil:

    def __init__(self):
        self.events = dict()
        self.key_board_istener: keyboard.Listener = None

    @property
    def logger(self):
        return get_log("pynut")

    def register(self, **kw):
        for key, call_back in kw.items():
            self.events[key] = call_back
        return self

    def on_press(self, k: keyboard.KeyCode):
        key = KeyCode(k)
        if key.char == "esc" or key.is_ctrl_c():  # wino
            self.key_board_istener.stop()
        elif self.events.get(key.char):
            self.events[key.char]()
        # else:
        #     print(key)

        return True

    def on_release(self, key):
        # self.logger.debug(f"{key} release")
        return True

    def run(self):
        if self.key_board_istener:
            return self
        self.key_board_istener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
        )
        self.key_board_istener.daemon = False
        self.key_board_istener.start()
        self.key_board_istener.join()
        return self

    def start(self):
        Thread(target=self.run).start()


PU_UTIL = PynutUtil()
