from app.tool.todo import Todo
from common.util.export import C, asset_exception


class TestTodo:
    def test_todo_insert(self):
        t = Todo()._set_env(the_dev_user="test_user")
        t.model.instance_map.pop("", None)
        asset_exception(
            t.web_submit, C.METHOD_INSERT, dict(title="", category="study"), msg="null"
        )
        asset_exception(
            t.web_submit, C.METHOD_INSERT, dict(title="123", category="study")
        )
        sorted(t.model.all(), key=lambda v: v.create_time.get_value(), reverse=True)

    def test_todo_delete(self):
        t = Todo()._set_env(the_dev_user="test_user")
        asset_exception(t.web_submit, C.METHOD_DELETE, dict(title="123"))

    def test_todo_update(self):
        t = Todo()._set_env(the_dev_user="test_user")
        asset_exception(t.web_submit, C.METHOD_EDIT, dict(title="123", content="xx"))
