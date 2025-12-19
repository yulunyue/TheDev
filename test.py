from common.util.export import (
    File,
    Module,
    TestBase,
    logger,
    sys,
    random,
    md5,
    base64_encode,
    make_md_file,
    List,
)


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

    def random(self, name="todo"):
        cmds: List[str] = []
        for line in File(f"{name}.md").read_line():
            if line.startswith("#") or not line:
                continue
            cmds.append(line)
        cmd = random.sample(cmds, 1)[0]
        key = cmd.split("-m ").pop().split(" ")[0].replace(".", "/")
        logger.info(cmd)
        if not File(f"{key}.py").exists():
            raise Exception(key)
        logger.info(f"{key}.py")
        path, info = make_md_file(key)
        logger.info(f"{path} -> {info}")

    def main(self):
        getattr(self, sys.argv[1])(*sys.argv[2:])


if __name__ == "__main__":
    TestMain().main()
