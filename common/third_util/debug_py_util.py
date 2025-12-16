import debugpy


class DebugPyUtil:
    def run(self):
        while True:
            debugpy.listen(("0.0.0.0", 5678))
            print("等待调试器附加...")
            debugpy.wait_for_client()
