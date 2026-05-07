from common.tool.export import FormBase, TaskConfig, Task, TASK_MANAGE
from common.util.export import C, Node, Type


class TaskManage(FormBase, Task):
    model: Type[TaskConfig] = TaskConfig

    def schema(self):
        return Node(
            data=dict(
                top_form=self.to_form_column_view(),
            )
        )

    def web_search(self, **kw):
        tasks = list(self.model.all())
        return Node(childs=tasks, title=f"任务总数: {len(tasks)}")

    def exec_task(self, name: str, **kw):
        task = self.model.get(name)
        task.exec()
        self.model.save_to_local()
        return task.to_json()


TASK_MANAGE.set_resource("config/setting/task.json").start()
