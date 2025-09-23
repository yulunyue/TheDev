from .node import BpNode, logger
from common.util.export import get_function_info, Dict, uid
from .bp_param import BpParam


class BpFunc(BpNode):
    def __init__(self, func):
        self.func = func
        self.key = uid(self.func.__name__)
        super().__init__()
        self.load(**get_function_info(func).data)

    def load(self, args, kwargs: dict, **kw):
        self.args_key = args
        self.kwargs = kwargs

    def set_params(self, params):
        if len(params) != len(self.args_key):
            raise Exception(self.func, params)
        for i, v in enumerate(self.args_key):
            if isinstance(params[i], BpNode):
                self.childs[v] = params[i]
            else:
                self.childs[v] = BpParam(**self.kwargs[v]).set_value(params[i])

    def get_value(self):
        kv_value = {k: v.get_value() for k, v in self.childs.items()}
        ret = self.func(**kv_value)
        return ret
