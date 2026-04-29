from ..base_class.storege.file_config import (
    FileConfig,
)
from ..base_class.base_model import StrModel, NumberModel, DictModel
from ..os_util import OsUtil
from common.util.export import time, File, Module, traceback, C, logger


class TaskConfig(FileConfig):
    name = StrModel()
    fun_path = StrModel()
    args = StrModel()
    run_model = DictModel()
    run_num = NumberModel(default_value=0)
    result = DictModel()

    @classmethod
    def set_resource(cls, path):
        return super().set_resource(path)

    def __init__(self) -> None:
        super().__init__()
        self.fun = None
        self.last_begin_t = None
        self.last_finish_t = None

    def get_call(self):
        if self.fun:
            return self.fun
        fun_paths = self.fun_path.get_value().split("/")
        fun_path = fun_paths.pop()
        self.fun = Module().load_module_object(
            fun_path,
            "/".join(fun_path),
        )
        return self.fun

    def can_run(self):
        run_model = self.run_model.get_value()
        if not run_model:
            return True
        raise Exception(run_model)

    def get_log(self):
        ret = File(f"data/log/task/{self.name.get_value()}.log")
        return ret

    def exec(self):
        if not self.can_run():
            return
        code = C.CODE_200
        try:
            last_begin_t = time.time()
            args = self.args.get_value().split(",")
            f = self.get_call()
            logger.map(args=args, f=f)
            value = f(*args)
        except Exception as e:
            code = C.CODE_500
            value = traceback.format_exc().split("\n")
        finally:
            last_finish_t = time.time()
        self.run_num.set_value(self.run_num.get_value() + 1)
        self.result.update(
            code=code,
            value=value,
            last_begin_t=last_begin_t,
            last_finish_t=last_finish_t,
        )
        return
