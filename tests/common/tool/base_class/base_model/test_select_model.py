from common.tool.base_class.base_model.select_model import SelectModel
from common.tool.base_class.baseconfig import ConfigBase
from common.util.export import File
import os
import tempfile


class MockConfig(ConfigBase):
    def __init__(self):
        self._id = "test"
        self._config = {}

    def update_param_value(self, param, value):
        self._config[param.key] = value

    def get_param_value(self, param):
        return self._config.get(param.key, param.default_value)


class TestSelectModel:

    def setup_class(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.conf_file = os.path.join(cls.temp_dir, "test_select_conf.json")

    def teardown_class(cls):
        if os.path.exists(cls.conf_file):
            os.remove(cls.conf_file)
        if os.path.exists(cls.temp_dir):
            os.rmdir(cls.temp_dir)

    def setup_method(self):
        if os.path.exists(self.conf_file):
            os.remove(self.conf_file)
        abs_path = File(self.conf_file).get_abs_path()
        if abs_path in File.FILES:
            del File.FILES[abs_path]

    def test_set_options_args(self):
        model = SelectModel().set_options("a", "b", "c")
        assert model.get_options() == {"a": "a", "b": "b", "c": "c"}

    def test_set_options_kwargs(self):
        model = SelectModel().set_options(study="学习", work="工作")
        assert model.get_options() == {"study": "学习", "work": "工作"}

    def test_set_options_mixed(self):
        model = SelectModel().set_options("a", "b", study="学习")
        assert model.get_options() == {"a": "a", "b": "b", "study": "学习"}

    def test_set_conf_file(self):
        File(self.conf_file).write_file({
            "study": {"title": "学习", "score": 1, "money": 0},
            "sport": {"title": "运动", "score": 3, "money": 0},
        })
        model = SelectModel().set_conf_file(self.conf_file)
        assert model.get_options() == {"study": "学习", "sport": "运动"}
        assert model.get_options_data() == {
            "study": {"title": "学习", "score": 1, "money": 0},
            "sport": {"title": "运动", "score": 3, "money": 0},
        }

    def test_get_data(self):
        File(self.conf_file).write_file({
            "study": {"title": "学习", "score": 1, "money": 0},
            "work": {"title": "工作", "score": 0, "money": 0},
        })
        model = SelectModel().set_conf_file(self.conf_file)
        cfg = MockConfig()
        model.set_datasource(cfg)
        model.set_key("category")
        model.set_value("study")
        assert model.get_data() == {"title": "学习", "score": 1, "money": 0}

    def test_get_data_empty(self):
        model = SelectModel()
        cfg = MockConfig()
        model.set_datasource(cfg)
        model.set_key("test")
        cfg._config["test"] = "value"
        assert model.get_data() == {}

    def test_set_value_valid_static(self):
        model = SelectModel().set_options("a", "b", "c")
        cfg = MockConfig()
        model.set_datasource(cfg)
        model.set_key("test")
        model.set_value("a")
        assert model.get_value() == "a"

    def test_set_value_valid_conf_file(self):
        File(self.conf_file).write_file({
            "a": {"title": "选项A"},
            "b": {"title": "选项B"},
        })
        model = SelectModel().set_conf_file(self.conf_file)
        cfg = MockConfig()
        model.set_datasource(cfg)
        model.set_key("test")
        model.set_value("a")
        assert model.get_value() == "a"

    def test_set_value_invalid(self):
        File(self.conf_file).write_file({
            "a": {"title": "选项A"},
            "b": {"title": "选项B"},
        })
        model = SelectModel().set_conf_file(self.conf_file)
        cfg = MockConfig()
        model.set_datasource(cfg)
        model.set_key("test")
        try:
            model.set_value("invalid")
            assert False, "should raise exception"
        except Exception as e:
            assert "not in options" in str(e)

    def test_to_json_static(self):
        model = SelectModel().set_options("study", "work")
        json_data = model.to_json()
        assert json_data["type"] == "select"
        children = json_data["children"]
        assert len(children) == 2
        assert {"title": "study", "value": "study"} in children
        assert {"title": "work", "value": "work"} in children

    def test_to_json_conf_file(self):
        File(self.conf_file).write_file({
            "study": {"title": "学习", "score": 1},
            "work": {"title": "工作"},
        })
        model = SelectModel().set_conf_file(self.conf_file)
        json_data = model.to_json()
        assert json_data["type"] == "select"
        children = json_data["children"]
        assert len(children) == 2
        assert {"title": "学习", "value": "study"} in children
        assert {"title": "工作", "value": "work"} in children

    def test_clone_static_options(self):
        proto = SelectModel().set_options("a", "b", "c")
        cloned = proto.clone()
        assert cloned.get_options() == {"a": "a", "b": "b", "c": "c"}
        cloned.set_datasource(MockConfig())
        cloned.set_key("test")
        cloned.set_value("a")
        assert cloned.get_value() == "a"

    def test_clone_conf_file(self):
        File(self.conf_file).write_file({
            "study": {"title": "学习", "score": 1},
            "work": {"title": "工作", "score": 0},
        })
        proto = SelectModel().set_conf_file(self.conf_file)
        cloned = proto.clone()
        cloned.set_datasource(MockConfig())
        cloned.set_key("category")
        cloned.set_value("study")
        assert cloned.get_data() == {"title": "学习", "score": 1}
        assert cloned.get_options() == {"study": "学习", "work": "工作"}