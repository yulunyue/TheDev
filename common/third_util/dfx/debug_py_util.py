import debugpy


class DebugPyUtil:
    def run(self, port=5678):
        debugpy.listen(("0.0.0.0", port))
        while True:
            print("等待调试器附加...")
            debugpy.wait_for_client()
            debugpy.breakpoint()
