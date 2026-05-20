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
        funs = getattr(self,fun_name)
        funs(*args,**kw)

    def get_call_fun(self):
        ret = []
        for v in list(dir(self)):
            if v[0] == "_":
                continue
            if v in {"run", "exit", "get_temp_file", "get_call_fun", "get_name"}:
                continue
            if v == "cli" and not hasattr(self, "do_cmd"):
                continue
            if callable(getattr(self, v)):
                ret.append(v)
        return ret

    def cli(self, do_cmd):
        fi, fo = self.get_temp_file("inp.txt"), self.get_temp_file("out.txt")
        logger.map(fi=fi, fo=fo)
        fi.write_if_not_exists("")
        last_cmd = []
        out_put_msgs = dict()
        while True:
            time.sleep(0.5)
            cmd = [
                v
                for v in fi.read_fast_file().split("\n")
                if v and not v.startswith("#")
            ]
            if cmd == last_cmd:
                continue
            flag = False
            for i, v in enumerate(cmd):
                if i < len(last_cmd) and v == last_cmd[i]:
                    continue
                out_put_msgs[i] = [i, v, do_cmd(*v.split(" "))]
                flag = True
            if flag:
                msgs = []
                sr = sorted(out_put_msgs.values())[: len(cmd)]
                for i, v, r in sr:
                    if isinstance(r, dict):
                        r = json_dumps(r)
                    msgs.append(f"i:{i} , cmd:{v}\n----------\n{r}\n-----------")
                fo.write_file("\n".join(msgs))
            last_cmd = cmd

    def get_temp_file(self, name):
        path = f"data/tool/{self.__class__.__name__}/{name}"
        logger.info(path)
        return File(path)
