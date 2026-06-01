from .base_class.storage.file_config import FileConfig
from .base_class.base_model import NumberModel, ListModel


class HttpConfig(FileConfig):
    port = NumberModel(default_value=49999).set_title("端口")
    py_modules = ListModel().set_title("模块配置")
    plugins = ListModel().set_title("插件列表")

    @classmethod
    def get_id_by_param(cls, **kw):
        return kw.get("name")
