from ..base_class.table_base import (
    TableBase,
    StrModel,
    NumberModel,
    ConfigBase,
    TableConfig,
    DictModel,
)
from ..os_util import OsUtil


class TaskConfig(TableConfig):
    module_name = StrModel()
    fun_name = StrModel()
    root_path = StrModel()
    args = StrModel()
    log_type = StrModel()
    wait_time = NumberModel(default_value=1)
    last_begin_t = NumberModel(default_value=0)
    last_finish_t = NumberModel(default_value=0)
    result = DictModel()
    _fun = None

    def get_call(self):
        if self._fun:
            return self._fun

        module_name = self.module_name.get_value()
        if module_name:
            self._fun = Module().load_module(
                module_name,
                self.root_path.get_value(),
                self.fun_name.get_value(),
            )
        else:
            self._fun = (
                OsUtil()
                .set_logger(self.get_log())
                .set_env(self.root_path.get_value(), self.fun_name.get_value())
                .run
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
                code=THE_DEV_CONSTANT.CODE_500, value=traceback.format_exc().split("\n")
            )
        self.last_finish_t.set_value(time.time())

    def __repr__(self):
        return f"result:{self.result}"
