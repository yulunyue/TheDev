from common.util.export import File, Module, TestBase


class TestMain:
    def run(self):
        for fp in File("tests").list_dir():
            _, *args = fp.name.split("_")
            if not args:
                continue
            m: TestBase = Module().load_module(
                f"tests.{fp.name}", fun_name=f"Test{args[0].title()}"
            )()
            m.run()


if __name__ == "__main__":
    TestMain().run()
