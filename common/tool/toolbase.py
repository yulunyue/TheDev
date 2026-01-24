from common.util.export import List, os, File, SYS_ARGS, SYS_KW, logger, sys, time
from .file_handers.todo import TodoFile


def make_md_file(file_path=None):
    if file_path is None:
        file_path = (
            sys.argv[0]
            .replace("\\", "/")
            .replace("/tool/", "/doc/tool/")
            .replace(".py", ".md")
        )
    return file_path


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
        md_file = make_md_file()
        todo = TodoFile(md_file)
        logger.info(md_file)
        funs = todo.get_cmd(fun_name)
        if isinstance(funs, str):
            logger.info(f"NOT FIND {fun_name}\n{funs}")
            return
        for ff, fkw in funs:
            if isinstance(ff, str):
                ff = getattr(self, ff)
            ff(**fkw)

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
