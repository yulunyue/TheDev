from common.tool.export import ToolBase, TaskConfig, TASK_MANAGE
from common.third_util.io.api import Api
from common.util.export import C, time_format, logger


class TaskTool(ToolBase):
    def todo_every_day(self, uri, name, mp: dict, **kw):
        date_str = time_format(fmt="%Y-%m-%d")
        api = Api().set_endpoint(uri)
        for type, values in mp.items():
            for v in values:
                api.post(
                    "/app/todo/web_submit",
                    dict(
                        type=C.METHOD_INSERT,
                        value=dict(
                            title=f"{date_str}_{v}", category=type, content="AUTO_GEN"
                        ),
                    ),
                    headers={C.THE_DEV_USER: name},
                )

    def test_zx(self):
        logger.info(Api().set_endpoint("http://1.14.97.154:10000").post("/app"))

    def do_task(self, name):
        TaskConfig.set_resource("config/setting/task.json")
        TaskConfig.get(name).run()


if __name__ == "__main__":
    TaskTool().run()
