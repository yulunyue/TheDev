from ..base_class.storege.file_config import (
    FileConfig,
)
from ..base_class.base_model import StrModel, NumberModel, DictModel
from ..os_util import OsUtil
from common.util.export import (
    time,
    File,
    Module,
    traceback,
    C,
    logger,
    json,
    IO_MANAGE,
    time_format,
)


class TaskConfig(FileConfig):
    name = StrModel().not_null().set_title("任务名称")
    fun_path = StrModel().set_title("函数路径")
    args = StrModel().set_title("参数")
    run_model = DictModel().set_title("运行模式")

    @classmethod
    def get_id_by_param(cls, name, **kw):
        return name

    @classmethod
    def set_resource(cls, path):
        return super().set_resource(path)

    @classmethod
    def get_form_columns(cls):
        return [cls.name, cls.fun_path, cls.args]

    def __init__(self) -> None:
        super().__init__()
        self.fun = None
        self.run_num = 0
        self.last_begin_t = ""
        self.last_finish_t = ""
        self.state = ""
        self.error_msg = ""

    def get_call(self):
        if self.fun:
            return self.fun
        fun_path = self.fun_path.get_value()
        self.fun = Module().load_fun_call(fun_path)
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
        IO_MANAGE.send(
            f"{C.TOPIC_TASK_UPDATE_MSG}.{self.name.get_value()}",
            dict(
                code=self.code,
                run_num=self.run_num,
                last_begin_t=self.last_begin_t,
                last_finish_t=self.last_finish_t,
                state=self.state,
                error_msg=self.error_msg,
            ),
        )

    def exec(self):
        if not self.can_run():
            return

        try:
            self.last_begin_t = time_format()
            self.last_finish_t = ""
            args = self.args.get_value().split(",")
            self.state = C.doing
            self.code = C.CODE_200
            self.notify_update()
            f = self.get_call()
            self.error_msg = ""
            self.value = f(*args)
        except Exception as e:
            self.code = C.CODE_500
            self.error_msg = traceback.format_exc().split("\n")
            self.notify_update()
        finally:
            self.code = C.CODE_200
            self.state = C.wait
            self.last_finish_t = time_format()
            self.notify_update()
        self.run_num += 1

        return
