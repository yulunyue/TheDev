import os
import tempfile

from common.util.export import TestBase
from common.tool.export import SqliteDbStore, StrModel, NumberModel, DictModel


class TestSqliteModel(SqliteDbStore):
    __table_name__ = "test_sqlite_model"

    name = StrModel()
    age = NumberModel(18)
    email = StrModel("default@example.com")
    metadata = DictModel({})


class TestSqliteDbStore:

    def setup_class(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_file = os.path.join(cls.temp_dir, "test_sqlite.db")
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)
        TestSqliteModel.set_resource(cls.test_file)

    def setup_method(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        TestSqliteModel.set_resource(self.test_file)

    def teardown_class(cls):
        if hasattr(TestSqliteModel, "_conn") and TestSqliteModel._conn:
            TestSqliteModel._conn.close()
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)
        if os.path.exists(cls.temp_dir):
            os.rmdir(cls.temp_dir)

    def test_init_resource_new_db(self):
        assert os.path.exists(self.test_file)
        assert hasattr(TestSqliteModel, "_conn")
        assert hasattr(TestSqliteModel, "_config")
        assert TestSqliteModel._config == {}

    def test_init_resource_existing_db(self):
        TestSqliteModel.insert("test1", name="Alice", age=25, email="alice@example.com")
        TestSqliteModel._conn.close()
        TestSqliteModel.set_resource(self.test_file)
        assert "test1" in TestSqliteModel.instance_map
        assert TestSqliteModel.instance_map["test1"].name.get_value() == "Alice"
        assert TestSqliteModel.instance_map["test1"].age.get_value() == 25

    def test_save(self):
        model = TestSqliteModel.insert("save_test", name="Bob", age=30)
        model.save()
        cursor = TestSqliteModel._conn.execute(
            f"SELECT name, age FROM {TestSqliteModel._table_name} WHERE id=?",
            ("save_test",),
        )
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == "Bob"
        assert row[1] == 30

    def test_insert_and_immediate_persist(self):
        model = TestSqliteModel.insert("insert_test", name="Charlie", age=35)
        cursor = TestSqliteModel._conn.execute(
            f"SELECT name, age FROM {TestSqliteModel._table_name} WHERE id=?",
            ("insert_test",),
        )
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == "Charlie"
        assert row[1] == 35

    def test_update_param_value(self):
        model = TestSqliteModel.insert("update_test", name="David")
        model.update_param_value(model.name, "Eve")
        assert model.name.get_value() == "Eve"
        cursor = TestSqliteModel._conn.execute(
            f"SELECT name FROM {TestSqliteModel._table_name} WHERE id=?",
            ("update_test",),
        )
        assert cursor.fetchone()[0] == "Eve"

    def test_update_param_value_if_none(self):
        model = TestSqliteModel.insert("if_none_test", name="Frank")
        model.update_param_value(model.name, "George", if_none=True)
        assert model.name.get_value() == "Frank"

    def test_get_param_value(self):
        model = TestSqliteModel.insert("get_test", name="Henry", age=40)
        assert model.get_param_value(model.name) == "Henry"
        assert model.get_param_value(model.age) == 40

    def test_get_param_value_default(self):
        model = TestSqliteModel.insert("default_test")
        assert model.get_param_value(model.email) == "default@example.com"
        assert model.get_param_value(model.age) == 18

    def test_all(self):
        TestSqliteModel.insert("all1", name="User1")
        TestSqliteModel.insert("all2", name="User2")
        TestSqliteModel.insert("all3", name="User3")
        all_models = TestSqliteModel.all()
        assert len(all_models) >= 3
        names = [m.name.get_value() for m in all_models]
        assert "User1" in names
        assert "User2" in names
        assert "User3" in names

    def test_instance_persistence(self):
        model1 = TestSqliteModel.insert("persist_test", name="Persist")
        model1.save()
        TestSqliteModel._conn.close()
        TestSqliteModel.set_resource(self.test_file)
        assert "persist_test" in TestSqliteModel.instance_map
        model2 = TestSqliteModel.instance_map["persist_test"]
        assert model2.name.get_value() == "Persist"

    def test_multiple_updates(self):
        model = TestSqliteModel.insert("multi_update", name="Original")
        model.update_param_value(model.name, "Updated1")
        model.update_param_value(model.age, 25)
        model.update_param_value(model.email, "updated@example.com")
        model.save()
        cursor = TestSqliteModel._conn.execute(
            f"SELECT name, age, email FROM {TestSqliteModel._table_name} WHERE id=?",
            ("multi_update",),
        )
        row = cursor.fetchone()
        assert row[0] == "Updated1"
        assert row[1] == 25
        assert row[2] == "updated@example.com"

    def test_dict_model(self):
        model = TestSqliteModel.insert(
            "dict_test", metadata={"key1": "value1", "key2": "value2"}
        )
        assert model.metadata.get_value() == {"key1": "value1", "key2": "value2"}
        model.save()
        cursor = TestSqliteModel._conn.execute(
            f"SELECT metadata FROM {TestSqliteModel._table_name} WHERE id=?",
            ("dict_test",),
        )
        import json

        assert json.loads(cursor.fetchone()[0]) == {
            "key1": "value1",
            "key2": "value2",
        }

    def test_get_existing_instance(self):
        model1 = TestSqliteModel.insert("get_existing", name="GetTest")
        model2 = TestSqliteModel.get("get_existing")
        assert model1 is model2
        assert model2.name.get_value() == "GetTest"

    def test_get_new_instance(self):
        TestSqliteModel.insert("new_get_test")
        model = TestSqliteModel.get("new_get_test")
        assert model._id == "new_get_test"
        assert model.email.get_value() == "default@example.com"

    def test_filter(self):
        TestSqliteModel.insert("query1", name="Q1")
        TestSqliteModel.insert("query2", name="Q2")
        TestSqliteModel.insert("other", name="Other")
        results = TestSqliteModel.filter("query")
        assert len(results) == 2
        names = [m.name.get_value() for m in results]
        assert "Q1" in names
        assert "Q2" in names

    def test_to_json(self):
        model = TestSqliteModel.insert("json_test", name="JsonTest", age=45)
        json_data = model.to_json()
        assert json_data["_id"] == "json_test"
        assert json_data["name"] == "JsonTest"
        assert json_data["age"] == 45
        assert json_data["email"] == "default@example.com"

    def test_delete(self):
        model = TestSqliteModel.insert("delete_test", name="ToDelete", age=99)
        assert "delete_test" in TestSqliteModel.instance_map
        model.delete()
        assert "delete_test" not in TestSqliteModel.instance_map
        cursor = TestSqliteModel._conn.execute(
            f"SELECT COUNT(*) FROM {TestSqliteModel._table_name} WHERE id=?",
            ("delete_test",),
        )
        assert cursor.fetchone()[0] == 0
