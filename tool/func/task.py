from common.tool.export import ToolBase
from common.util.export import C, time_format, logger


class TaskTool(ToolBase):
    def todo_every_day(self, name, mp, **kw):
        from app.tool.todo import Todo

        date_str = time_format(fmt="%Y-%m-%d")
        items = [
            dict(
                title=f"{date_str}_{v}", category=type, content="AUTO_GEN", user_id=name
            )
            for type, values in mp.items()
            for v in values
        ]
        logger.info(f"todo_every_day items={items}")
        return Todo().web_batch_insert(items=items)


if __name__ == "__main__":
    TaskTool().run()
