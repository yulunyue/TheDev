from common.tool.export import ToolBase, TaskConfig, TASK_MANAGE
from common.third_util.io.api import Api
from common.util.export import C, time_format, logger


class TaskTool(ToolBase):
    def todo_every_day(self, uri, name, mp: dict, **kw):
        date_str = time_format(fmt="%Y-%m-%d")
        api = Api().set_endpoint(uri)
        ret = []
        for type, values in mp.items():
            for v in values:
                value = dict(title=f"{date_str}_{v}", category=type, content="AUTO_GEN")
                res = api.post(
                    "/app/todo/web_insert",
                    value,
                    headers={C.THE_DEV_USER: name},
                )
                ret.append(res)
                logger.map(type=type, value=value, res=res)
        return ret


if __name__ == "__main__":
    TaskTool().run()
