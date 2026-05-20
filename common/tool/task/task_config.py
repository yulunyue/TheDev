from ..base_class.storage.file_config import (
    FileConfig,
)
from ..base_class.base_model import (
    StrModel,
    NumberModel,
    DictModel,
    JsonDictModel,
    SelectModel,
)
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
    time_change,
)


class TaskConfig(FileConfig):
    name = StrModel().not_null().set_title("任务名称")
    fun_path = StrModel().set_title("函数路径")
    kw = JsonDictModel().set_title("参数")
    run_model = (
        SelectModel(default_value=C.SECOND30)
        .set_title("运行模式")
        .set_options(
            **{
                C.NEVER: "永不执行",
                C.SECOND1: "间隔1秒执行",
                C.SECOND30: "间隔30秒执行",
                C.EVERY_DAY_BEGIN: "每天0点执行",
            }
        )
    )

    @classmethod
    def get_id_by_param(cls, name, **kw):
        return name

    @classmethod
    def set_resource(cls, path):
        return super().set_resource(path)

    @classmethod
    def get_form_columns(cls):
        return [cls.name, cls.fun_path, cls.kw, cls.run_model]

    def __init__(self) -> None:
        super().__init__()
        self.fun = None
        self.run_num = 0
        self.last_begin_t = 0
        self.last_finish_t = 0
        self.state = ""
        self.value = None
        self.code = C.CODE_200
        self.error_msg = ""

    def get_call(self):
        if self.fun:
            return self.fun
        fun_path = self.fun_path.get_value()
        logger.map(self.name.get_value(), fun_path=fun_path)
        self.fun = Module().load_fun_call(fun_path)
        return self.fun

    def can_run(self):
        run_model = self.run_model.get_value()
        if run_model == C.NEVER:
            return False
        t = time.time()
        if run_model == C.SECOND1:
            return t > self.last_finish_t + 1
        elif run_model == C.SECOND30:
            return t > self.last_finish_t + 30
        elif run_model == C.EVERY_DAY_BEGIN:
            return time_change("%Y-%m-%d")
        return False

    def get_log(self):
        ret = File(f"data/log/task/{self.name.get_value()}.log")
        return ret

    def notify_update(self):
        IO_MANAGE.send(
            f"{C.TOPIC_TASK_UPDATE_MSG}.{self.name.get_value()}", self.view()
        )

    def view(self):
        return dict(
            value=dict(
                code=self.code,
                run_num=self.run_num,
                t=f"[{time_format(self.last_begin_t)}] -> [{time_format(self.last_finish_t)}] USER_TIME:[{self.last_finish_t-self.last_begin_t}]",
                state=self.state,
                value=self.value,
                error_msg=self.error_msg,
            )
        )

    def exec(self):
        if not self.can_run():
            return
        self.run()

    def run(self):
        try:
            self.last_begin_t = time.time()
            self.last_finish_t = self.last_begin_t
            self.state = C.doing
            self.code = C.CODE_200
            self.notify_update()
            f = self.get_call()
            self.error_msg = ""
            self.value = f(**self.kw.get_value())
        except Exception as e:
            self.code = C.CODE_500
            self.error_msg = traceback.format_exc().split("\n")
            self.notify_update()
        finally:
            self.code = C.CODE_200
            self.state = C.wait
            self.last_finish_t = time.time()
            self.notify_update()
        self.run_num += 1

        return
