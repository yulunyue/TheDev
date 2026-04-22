from common.util.export import TestBase, File, logger
from common.tool.export import StrModel, NumberModel, DictModel
from common.tool.base_class.baseconfig import ConfigBase
from common.tool.base_class.storege.file_config import FileConfig
import pytest
import os
import tempfile


class TestFileConfigModel(FileConfig):
    name = StrModel()
    age = NumberModel(18)
    email = StrModel("default@example.com")
    metadata = DictModel({})


class TestFileConfig:

    def setup_class(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_file = os.path.join(cls.temp_dir, "test_file_config.json")
        TestFileConfigModel.set_resource(cls.test_file)

    def setup_method(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        TestFileConfigModel.set_resource(self.test_file)

    def teardown_class(cls):
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)
        if os.path.exists(cls.temp_dir):
            os.rmdir(cls.temp_dir)

    def test_init_resource_new_file(self):
        assert not os.path.exists(self.test_file)
        TestFileConfigModel.set_resource(self.test_file)
        assert hasattr(TestFileConfigModel, 'fp')
        assert hasattr(TestFileConfigModel, '_config')
        assert TestFileConfigModel._config == {}

    def test_init_resource_existing_file(self):
        File(self.test_file).write_file({
            "test1": {"name": "Alice", "age": 25, "email": "alice@example.com"}
        })
        TestFileConfigModel.set_resource(self.test_file)
        assert "test1" in TestFileConfigModel.instance_map
        assert TestFileConfigModel.instance_map["test1"].name.get_value() == "Alice"

    def test_save(self):
        model = TestFileConfigModel.insert("save_test", name="Bob", age=30)
        TestFileConfigModel.save()
        assert os.path.exists(self.test_file)
        content = File(self.test_file).read_file()
        assert "save_test" in content
        assert content["save_test"]["name"] == "Bob"

    def test_insert_and_save(self):
        model = TestFileConfigModel.insert("insert_test", name="Charlie", age=35)
        model.save()
        content = File(self.test_file).read_file()
        assert "insert_test" in content
        assert content["insert_test"]["name"] == "Charlie"
        assert content["insert_test"]["age"] == 35

    def test_update_param_value(self):
        model = TestFileConfigModel.insert("update_test", name="David")
        model.update_param_value(model.name, "Eve")
        assert model.name.get_value() == "Eve"

    def test_update_param_value_if_none(self):
        model = TestFileConfigModel.insert("if_none_test", name="Frank")
        model.update_param_value(model.name, "George", if_none=True)
        assert model.name.get_value() == "Frank"

    def test_get_param_value(self):
        model = TestFileConfigModel.insert("get_test", name="Henry", age=40)
        assert model.get_param_value(model.name) == "Henry"
        assert model.get_param_value(model.age) == 40

    def test_get_param_value_default(self):
        model = TestFileConfigModel.insert("default_test")
        assert model.get_param_value(model.email) == "default@example.com"
        assert model.get_param_value(model.age) == 18

    def test_all(self):
        TestFileConfigModel.insert("all1", name="User1")
        TestFileConfigModel.insert("all2", name="User2")
        TestFileConfigModel.insert("all3", name="User3")
        all_models = TestFileConfigModel.all()
        assert len(all_models) >= 3
        names = [m.name.get_value() for m in all_models]
        assert "User1" in names
        assert "User2" in names
        assert "User3" in names

    def test_instance_persistence(self):
        model1 = TestFileConfigModel.insert("persist_test", name="Persist")
        TestFileConfigModel.save()
        TestFileConfigModel.instance_map.clear()
        TestFileConfigModel.init_resource()
        assert "persist_test" in TestFileConfigModel.instance_map
        model2 = TestFileConfigModel.instance_map["persist_test"]
        assert model2.name.get_value() == "Persist"

    def test_multiple_updates(self):
        model = TestFileConfigModel.insert("multi_update", name="Original")
        model.update_param_value(model.name, "Updated1")
        model.update_param_value(model.age, 25)
        model.update_param_value(model.email, "updated@example.com")
        TestFileConfigModel.save()
        
        content = File(self.test_file).read_file()
        assert content["multi_update"]["name"] == "Updated1"
        assert content["multi_update"]["age"] == 25
        assert content["multi_update"]["email"] == "updated@example.com"

    def test_dict_model(self):
        model = TestFileConfigModel.insert("dict_test", metadata={"key1": "value1", "key2": "value2"})
        assert model.metadata.get_value() == {"key1": "value1", "key2": "value2"}
        TestFileConfigModel.save()
        content = File(self.test_file).read_file()
        assert content["dict_test"]["metadata"] == {"key1": "value1", "key2": "value2"}

    def test_get_existing_instance(self):
        model1 = TestFileConfigModel.insert("get_existing", name="GetTest")
        model2 = TestFileConfigModel.get("get_existing")
        assert model1 is model2
        assert model2.name.get_value() == "GetTest"

    def test_get_new_instance(self):
        model = TestFileConfigModel.insert("new_get_test")
        assert model._id == "new_get_test"
        assert model.email.get_value() == "default@example.com"

    def test_query(self):
        TestFileConfigModel.insert("query1", name="QueryTest1")
        TestFileConfigModel.insert("query2", name="QueryTest2")
        TestFileConfigModel.insert("other", name="Other")
        results = TestFileConfigModel.query("query")
        assert len(results) == 2
        names = [m.name.get_value() for m in results]
        assert "QueryTest1" in names
        assert "QueryTest2" in names

    def test_to_json(self):
        model = TestFileConfigModel.insert("json_test", name="JsonTest", age=45)
        json_data = model.to_json()
        assert json_data["_id"] == "json_test"
        assert json_data["name"] == "JsonTest"
        assert json_data["age"] == 45
        assert json_data["email"] == "default@example.com"

    def test_raise_assertion_no_resource_path(self):
        class NoResourceModel(FileConfig):
            name = StrModel()
        
        with pytest.raises(AssertionError):
            NoResourceModel.init_resource()

    def test_config_dict_structure(self):
        TestFileConfigModel.insert("struct_test", name="StructTest", age=50, metadata={"test": "data"})
        TestFileConfigModel.save()
        content = File(self.test_file).read_file()
        assert isinstance(content, dict)
        assert "struct_test" in content
        assert isinstance(content["struct_test"], dict)
        assert "name" in content["struct_test"]
        assert "age" in content["struct_test"]
        assert "metadata" in content["struct_test"]

    def test_empty_instance_map_initially(self):
        TestFileConfigModel.set_resource(self.test_file)
        assert len(TestFileConfigModel.instance_map) == 0

    def test_file_handle_attribute(self):
        TestFileConfigModel.set_resource(self.test_file)
        assert hasattr(TestFileConfigModel, 'fp')
        assert isinstance(TestFileConfigModel.fp, File)