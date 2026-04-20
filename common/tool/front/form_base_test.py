from common.util.export import TestBase, Node, ApiBase
from common.tool.export import FormBase, ConfigBase, StrModel, NumberModel, FileConfig
import pytest


class TestModel(FileConfig):
    name = StrModel()
    age = NumberModel(18)
    email = StrModel()


TestModel.set_resource("data/test_form_base.json")


class TestForm(FormBase):
    model = TestModel


class TestFormEmpty(FormBase):
    pass


class TestFormBase:

    def setup_class(cls):
        TestModel.instance_map = {}

    def setup_method(self):
        TestModel.instance_map = {}

    def test_get(self):
        test_form = TestForm()
        model = test_form.get("test_key")
        assert hasattr(model, '_id')

    def test_to_form_row_view(self):
        test_form = TestForm()
        result = test_form.to_form_row_view()
        assert hasattr(result, 'to_json')
        json_result = result.to_json()
        assert json_result["type"] == "form_row"
        assert len(json_result["childs"]) == 3

    def test_to_form_column_view(self):
        test_form = TestForm()
        result = test_form.to_form_column_view()
        assert hasattr(result, 'to_json')
        json_result = result.to_json()
        assert json_result["type"] == "form_column"
        assert len(json_result["childs"]) == 3

    def test_web_search_empty(self):
        test_form = TestForm()
        result = test_form.web_search("", "")
        assert isinstance(result, Node)
        assert isinstance(result.childs, list)

    def test_to_table_view_empty(self):
        test_form = TestForm()
        result = test_form.to_table_view()
        assert hasattr(result, 'to_json')
        json_result = result.to_json()
        assert json_result["type"] == "table"
        assert "childs" in json_result
        assert "value" in json_result

    def test_form_with_empty_model(self):
        test_form = TestFormEmpty()
        result = test_form.to_form_row_view()
        assert hasattr(result, 'to_json')
        json_result = result.to_json()
        assert json_result["type"] == "form_row"

    def test_form_inheritance(self):
        class CustomForm(TestForm):
            model = TestModel

        custom_form = CustomForm()
        result = custom_form.to_form_row_view()
        assert hasattr(result, 'to_json')
        json_result = result.to_json()
        assert json_result["type"] == "form_row"

    def test_get_font_columns(self):
        test_form = TestForm()
        columns = TestForm.model.get_font_columns()
        assert len(columns) == 3

    def test_form_base_is_api_base(self):
        test_form = TestForm()
        assert isinstance(test_form, ApiBase)

    def test_model_structure(self):
        params = TestModel.get_params()
        assert 'name' in params
        assert 'age' in params
        assert 'email' in params

    def test_form_row_structure(self):
        test_form = TestForm()
        result = test_form.to_form_row_view().to_json()
        assert 'childs' in result
        assert 'data' in result
        assert 'btns' in result['data']

    def test_form_column_structure(self):
        test_form = TestForm()
        result = test_form.to_form_column_view().to_json()
        assert 'childs' in result
        assert 'data' in result

    def test_table_structure(self):
        test_form = TestForm()
        result = test_form.to_table_view().to_json()
        assert 'type' in result
        assert 'childs' in result
        assert 'value' in result

    def test_search_returns_list(self):
        test_form = TestForm()
        result = test_form.web_search("test", "name")
        assert isinstance(result.childs, list)

    def test_node_creation(self):
        test_form = TestForm()
        result = test_form.web_search("", "")
        assert result.type == ""

    def test_model_instance_map(self):
        TestModel.insert("test_instance_1")
        assert "test_instance_1" in TestModel.instance_map
        assert TestModel.instance_map["test_instance_1"]._id == "test_instance_1"