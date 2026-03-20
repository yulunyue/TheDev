from ..base_class.storege.file_config import (
    FileConfig,
)
from ..base_class.base_model import StrModel, NumberModel, DictModel
from ..os_util import OsUtil
from common.util.export import time, File, Module, traceback, C


class TaskConfig(FileConfig):
    fun_path = StrModel()
    root_path = StrModel()
    args = StrModel()
    log_type = StrModel()
    wait_time = NumberModel(default_value=1)
    last_begin_t = NumberModel(default_value=0)
    last_finish_t = NumberModel(default_value=0)
    result = DictModel()
    resource_path = "config/setting/taskconfig.json"
    _fun = None

    def get_call(self):
        if self._fun:
            return self._fun
        fun_path = self.fun_path.get_value()
        self._fun = Module().load_module_object(
            fun_path,
            self.root_path.get_value(),
        )
        return self._fun

    def get_log(self):
        # log_type = self.log_type.get_value()
        ret = File(f"data/log/task/{self.key}.log")
        return ret

    def exec(self):
        now_t = time.time()
        if (
            self.wait_time.get_value() == -1
            or now_t - self.last_finish_t.get_value() < self.wait_time.get_value()
        ):
            return
        self.last_begin_t.set_value(now_t)
        try:
            self.result.update(
                value=self.get_call()(*self.args.get_value().split(",")),
            )
        except Exception as e:
            self.result.update(
                code=C.CODE_500, value=traceback.format_exc().split("\n")
            )
        self.last_finish_t.set_value(time.time())
