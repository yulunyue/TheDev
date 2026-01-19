from common.util.export import List, os, File, SYS_ARGS, SYS_KW, logger, sys, time
from .file_handers.todo import TodoFile


def make_md_file(key=None, msg=""):
    if key is None:
        file_dir = (
            sys.argv[0]
            .replace(os.getcwd() + "\\", "")
            .replace(".py", ".md")
            .replace("\\", "/")
        )
        file_dir = f"doc/{file_dir}"
    else:
        file_dir = key + ".md"
    f = File(file_dir)
    f.write_if_not_exists(msg)
    return f.path, "\n".join(f.read_line()[-5:])


class ToolBase:
    name = None

    def get_name(self):
        return self.name or self.__class__.__name__

    def exit(self):
        pass

    def run(self):
        self.msgs = []
        self.argvs, kw = SYS_ARGS.copy(), SYS_KW.copy()
        if self.argvs:
            fun_name = self.argvs.pop()
        else:
            fun_name = ""
        md_file = make_md_file()[0]
        todo = TodoFile(md_file)
        logger.info(md_file)
        f = getattr(self, fun_name, None)
        funs = []
        if f is None:
            funs.extend(self.get_call_fun())
            kw, f = todo.get_cmd(fun_name)
            if f == 1:
                funs.extend(kw)
                f = None
            elif f == 2:
                funs = kw
                f = None
            elif isinstance(f, str):
                f = getattr(self, f)
        if f is not None:
            f(**kw)
            self.exit()
        else:
            for fun in funs:
                logger.info(fun)

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

    def cli(self):
        fi, fo = self.get_temp_file("inp.txt"), self.get_temp_file("out.txt")
        fi.write_if_not_exists("")
        last_cmd = []
        out_put_msgs = dict()
        while True:
            time.sleep(1)
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
                out_put_msgs[i] = [i, v, self.do_cmd(*v.split(" "))]
                flag = True
            if flag:
                msgs = []
                sr = sorted(out_put_msgs.values())[: len(cmd)]
                for i, v, r in sr:
                    msgs.append(f"i:{i} , cmd:{v}\n----------\n{r}\n-----------")
                fo.write_file("\n".join(msgs))
            last_cmd = cmd

    def get_temp_file(self, name):
        path = f"data/tool/{self.__class__.__name__}/{name}"
        logger.info(path)
        return File(path)
