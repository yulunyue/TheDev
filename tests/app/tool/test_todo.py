from app.tool.todo import Todo
from app.tool.model.todo_model import TodoModel
from common.util.export import asset_exception


class TestTodo:
    def setup_method(self):
        self.t = Todo()._set_env(the_dev_user="test_user")
        TodoModel.instance_map.clear()

    def test_todo_insert(self):
        asset_exception(self.t.web_insert, title="", category="study", msg="null")
        asset_exception(self.t.web_insert, title="123", category="study")
        sorted(self.t.model.all(), key=lambda v: v.create_time.get_value(), reverse=True)

    def test_todo_delete(self):
        asset_exception(self.t.web_delete, title="123")

    def test_todo_update(self):
        asset_exception(self.t.web_edit, title="123", content="xx")

    def test_calc_score_empty(self):
        score, money = TodoModel.calc_score()
        assert score == 0
        assert money == TodoModel.INITIAL_MONEY

    def test_search_empty(self):
        score, money, todos = TodoModel.search("study", False)
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
