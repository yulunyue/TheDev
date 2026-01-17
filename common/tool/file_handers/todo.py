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
                cmds.append(key)
        if len(cmds) == 0:
            return [f"{k}->{v}" for k, v in todo_calls.items()], 1
        if len(cmds) > 1:
            return [f"{k}->{todo_calls['k']}" for k in cmds], 2
        return self.cmd(todo_calls[cmds[0]])

    def cmd(self, cmd):
        args, kw = cmd_parse(cmd)
        f = None
        if len(args) == 1:
            f = args[0]
        elif len(args) == 2:
            f = getattr(Module().load_module_object(args[0])(), args[1])
        return kw, f
