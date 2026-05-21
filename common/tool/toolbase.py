from common.util.export import (
    File,
    SYS_ARGS,
    SYS_KW,
    logger,
    time,
    json_dumps,
)


class ToolBase:
    name = None

    def get_name(self):
        return self.name or self.__class__.__name__

    def exit(self):
        pass

    def run(self):
        self.msgs = []
        args, kw = SYS_ARGS.copy(), SYS_KW.copy()
        fun_name = args.pop(0)
        funs = getattr(self, fun_name)
        funs(*args, **kw)

    def do_cmd(self, *args):
        pass

    def cli(self, name):
        fi, fo = self.get_temp_file(f"{name}_inp.txt"), self.get_temp_file(
            f"{name}_out.txt"
        )
        logger.map(fi=fi, fo=fo)
        fi.write_if_not_exists("")

        while True:
            time.sleep(0.5)
            flag, data = fi.read_fast_file()
            if not flag:
                continue
            out_put_msgs = []
            for i, v in enumerate(data.split("\n")):
                out_put_msgs.append([v, self.do_cmd(*v.split(" "))])
            msgs = []
            for i, (v, r) in enumerate(out_put_msgs):
                if isinstance(r, dict):
                    r = json_dumps(r)
                msgs.append(f"i:{i} , cmd:{v}\n----------\n{r}\n-----------")
            fo.write_file("\n".join(msgs))

    def get_temp_file(self, name):
        path = f"data/tool/{self.__class__.__name__}/{name}"
        logger.info(path)
        return File(path)
