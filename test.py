from common.util.export import (
    File,
    Module,
    TestBase,
    logger,
    sys,
    random,
    md5,
    base64_encode,
)


def make_file(md5_value, name, msg=""):
    f = File(f"doc/life/{md5_value}/{name}")
    f.write_if_not_exists(msg)
    return f.path, "\n".join(f.read_line()[-5:])


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
        cmds = []
        for line in File(f"{name}.md").read_line():
            if line.startswith("#") or not line:
                continue
            cmds.append(line)
        cmd: str = cmds[random.randint(0, len(cmds) - 1)]
        file_path = cmd.split(" ")[2].replace(".", "/") + ".py"
        md5_value = md5(cmd)
        infos = ["", cmd, file_path]
        path, info = make_file(md5_value, "日志.md")
        infos.append(f"{path} -> {info}")
        logger.info("\n".join(infos))

    def main(self):
        getattr(self, sys.argv[1])(*sys.argv[2:])


if __name__ == "__main__":
    TestMain().main()
