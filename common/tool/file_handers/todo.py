from common.util.export import File, logger, SYS_ARGS, cmd_parse, Module
from ..re_util import ReUtil


class TodoFile:
    RE_CMD = "```(.*?)\n(.*?)\n```"

    def __init__(self, f):
        self.f = File(f).write_if_not_exists("")
        self.todo_calls = dict()

    def get_todo_calls(self):
        if not self.todo_calls:
            lns = self.f.read_file()
            for key, cmd in ReUtil(TodoFile.RE_CMD).findall(lns):
                self.todo_calls[key] = cmd
        return self.todo_calls

    def get_cmd(self, key):
        cmds = []
        todo_calls = self.get_todo_calls()
        for k, v in todo_calls.items():
            if ReUtil(key).findall(k):
                cmds.append(v)
        if not cmds:
            return "\n".join([f"{k}->{v}" for k, v in todo_calls.items()])
        return [self.cmd(cmd) for cmd in cmds]

    def cmd(self, cmd):
        args, kw = cmd_parse(cmd)
        if "." in args[0]:
            f = Module(use_cache=True).load_module_object(
                args[0]
            )  # get_file_path_by_cls 需要使用cache
        else:
            f = args[0]
        return f, kw
