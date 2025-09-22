from .node import BpNode, logger
from .bp_param import BpParam
from .bp_func import BpFunc
from common.util.export import File, get_log, List, get_function_info


class BpCompile:
    def __init__(self):
        self.func = dict()

    def load_from_file(self, s: str):
        codes = File(s).read_file()
        self.tmp_params: List[BpFunc] = []
        self.tmp_s = ""
        for c in codes:
            if c == "\n" or c == " " or c == "    " or c == "":
                continue
            elif c == "(":
                self.hander_left()
            elif c == ")":
                self.hander_right()
            elif c == ",":
                self.hander_s()
            else:
                self.tmp_s += c
        return self.tmp_params[0]

    def hander_left(self):
        self.tmp_params.append(self.get_func(self.tmp_s))
        self.tmp_params.append("(")
        self.tmp_s = ""

    def hander_right(self):

        params = []
        if self.tmp_s:
            params.append(self.tmp_s)
        while self.tmp_params[-1] != "(":
            params.insert(0, self.tmp_params.pop())
        self.tmp_params.pop()
        self.tmp_params[-1].set_params(params)
        # logger.map(tmp_params=self.tmp_params, params=params)
        self.tmp_s = ""

    def hander_s(self):
        if self.tmp_s:
            self.tmp_params.append(self.tmp_s)
            self.tmp_s = ""

    def register_func(self, **kw):
        for k, value in kw.items():
            self.func[k] = value

    def get_func(self, key):
        return BpFunc(self.func[key])


BP = BpCompile()
