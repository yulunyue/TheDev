from common.tool.export import ToolBase
from common.third_util.io.api import Api
from common.util.export import C, time_format


class TaskTool(ToolBase):
    def todo_every_day(self, uri, name, mp: dict, **kw):
        date_str = time_format("%Y-%m-%d")
        api = Api().set_endpoint(uri)
        for type, values in mp.items():
            for v in values:
                api.post(
                    "/app/todo/web_submit",
                    dict(
                        key=f"{date_str}_{v}",
                        type=C.METHOD_INSERT,
                        value=dict(category=type, content="AUTO_GEN"),
                    ),
                    headers={C.THE_DEV_USER: name},
                )


if __name__ == "__main__":
    TaskTool().run()
