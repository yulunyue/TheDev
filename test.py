






from common.util.export import File, Module, TestBase, logger, sys, random


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

    def random(self):
        cmds = []
        for line in File("todo.md").read_line():
            if line.startswith("#") or not line:
                continue
            cmds.append(line)
        logger.info(cmds[random.randint(0, len(cmds) - 1)])

    def main(self):
        getattr(self, sys.argv[1])(*sys.argv[2:])


if __name__ == "__main__":
    TestMain().main()
