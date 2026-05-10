from common.tool.export import FormBase, TaskConfig, Task, TASK_MANAGE, FontSearch
from common.util.export import C, Node, Type


def test(*args):
    return dict(value=1)


class TaskManage(FormBase, Task):
    model: Type[TaskConfig] = TaskConfig

    def view(self, key, **kw):
        return TaskConfig.get(key).view()

    def schema(self):
        return Node(
            data=dict(
                top_form=self.to_form_column_view(),
            )
        )

    def web_search(self, key: str = "", **kw):
        return FontSearch().add_node(
            [
                {C.TITLE: d.name.get_value(), C.VALUE: d.name.get_value()}
                for d in self.model.all()
            ]
        )

    def exec_task(self, key: str, **kw):
        task = self.model.get(key)
        task.run()
        return Node(value="ok")
