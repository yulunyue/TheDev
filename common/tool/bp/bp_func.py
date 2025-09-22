from .node import BpNode, logger
from common.util.export import get_function_info, Dict
from .bp_param import BpParam


class BpFunc(BpNode):
    def __init__(self, func):
        self.func = func
        self.load(**get_function_info(func).data)
        super().__init__()

    def load(self, args, kwargs: dict, **kw):
        self.kw_map: Dict[str, BpParam] = dict()
        self.args_key = args
        for k, v in kwargs.items():
            self.kw_map[k] = BpParam(**v)

    def set_params(self, params):
        if len(params) != len(self.args_key):
            raise Exception(self.func, params)
        for i, v in enumerate(self.args_key):
            self.kw_map[v].set_value(params[i])

    def execute(self):
        kv_value = {k: v.get_value() for k, v in self.kw_map.items()}
        logger.map(func=self.func.__name__, kw=kv_value)
        return self.func(**kv_value)

    def get_value(self):
        return self.execute()

    def __repr__(self):
        return f"name:{self.func.__name__}"
