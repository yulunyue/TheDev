from app.tool.todo import Todo
from app.tool.model.todo_model import TodoModel
from common.util.export import C, asset_exception


class TestTodo:
    def setup_method(self):
        self.t = Todo()._set_env(the_dev_user="test_user")
        TodoModel.instance_map.clear()

    def test_todo_insert(self):
        asset_exception(
            self.t.web_submit, C.METHOD_INSERT, dict(title="", category="study"), msg="null"
        )
        asset_exception(
            self.t.web_submit, C.METHOD_INSERT, dict(title="123", category="study")
        )
        sorted(self.t.model.all(), key=lambda v: v.create_time.get_value(), reverse=True)

    def test_todo_delete(self):
        asset_exception(self.t.web_submit, C.METHOD_DELETE, dict(title="123"))

    def test_todo_update(self):
        asset_exception(self.t.web_submit, C.METHOD_EDIT, dict(title="123", content="xx"))

    def test_calc_score_empty(self):
        assert TodoModel.calc_score("test_user") == 0

    def test_calc_money_balance_default(self):
        assert TodoModel.calc_money_balance() == TodoModel.INITIAL_MONEY

    def test_search_empty(self):
        score, money, todos = TodoModel.search("study", False, "test_user")
        assert todos == []
        assert isinstance(score, int)
        assert isinstance(money, int)

    def test_schema_returns_structure(self):
        result = self.t.schema()
        assert result.data is not None
        assert "top_form" in result.data
        assert "category" in result.data

    def test_web_search_empty(self):
        result = self.t.web_search("study", False)
        assert result.childs == []
        assert result.title is not None
