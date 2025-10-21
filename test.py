from common.util.export import File, Module, TestBase, logger


class TestMain:
    def run(self):
        for fp in File("tests").list_dir():
            _, *args = fp.name.split("_")
            if not args:
                continue
            cls = None
            try:
                cls: TestBase = Module().load_module(
                    f"tests.{fp.name}", fun_name=f"Test{args[0].title()}"
                )
                cls().run()
            except Exception as e:
                logger.exception(e)


if __name__ == "__main__":
    TestMain().run()
