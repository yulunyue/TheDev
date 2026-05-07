from ..base_class.storege.file_config import (
    FileConfig,
)
from ..base_class.base_model import StrModel, NumberModel, DictModel
from ..os_util import OsUtil
from common.util.export import time, File, Module, traceback, C, logger, json
from common.third_util.http import WEB_SOCKET_CLIENTS


class TaskConfig(FileConfig):
    name = StrModel().not_null().set_title("任务名称")
    fun_path = StrModel().set_title("函数路径")
    args = StrModel().set_title("参数")
    run_model = DictModel().set_title("运行模式")
    run_num = NumberModel(default_value=0).set_title("运行次数")
    result = DictModel().set_title("执行结果")

    @classmethod
    def set_resource(cls, path):
        return super().set_resource(path)

    @classmethod
    def get_form_columns(cls):
        return [cls.name, cls.fun_path, cls.args]

    def __init__(self) -> None:
        super().__init__()
        self.fun = None
        self.last_begin_t = None
        self.last_finish_t = None

    def get_call(self):
        if self.fun:
            return self.fun
        fun_path = self.fun_path.get_value()
        parts = fun_path.split("::")
        if len(parts) >= 2:
            module_path = parts[0]
            func_name = parts[-1]
        else:
            parts = fun_path.split("/")
            module_path = "/".join(parts[:-1])
            func_name = parts[-1]
        self.fun = Module().load_module_object(
            func_name,
            module_path,
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

    def notify_update(self):
        msg = json.dumps({
            "type": C.TOPIC_TASK_UPDATE_MSG,
            "value": self.to_json()
        })
        for client in WEB_SOCKET_CLIENTS.values():
            try:
                client.write_message(msg)
            except Exception as e:
                logger.error(f"send task update error: {e}")

    def exec(self):
        if not self.can_run():
            return
        code = C.CODE_200
        try:
            last_begin_t = time.time()
            args = self.args.get_value().split(",")
            f = self.get_call()
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
        self.notify_update()
        return
