from .model import BaseModel
from common.util.export import File


class SelectModel(BaseModel):
    model: "SelectModel"

    def __init__(self, key=None, default_value=None, data_source=None) -> None:
        super().__init__(key, default_value, data_source)
        self._conf_file: File = None
        self._static_options: dict = None
        self.model: "SelectModel" = None

    def set_options(self, *args, **kw):
        self._static_options = {a: a for a in args}
        self._static_options.update(kw)
        return self

    def set_conf_file(self, path: str):
        self._conf_file = File.new(path)
        return self

    def get_conf_file(self):
        if self._conf_file:
            return self._conf_file
        if self.model and self.model._conf_file:
            return self.model._conf_file
        return None

    def get_static_options(self):
        if self._static_options:
            return self._static_options
        if self.model and self.model._static_options:
            return self.model._static_options
        return None

    def get_options(self):
        static = self.get_static_options()
        if static:
            return static
        conf_file = self.get_conf_file()
        if conf_file:
            data = conf_file.get_config()
            return {k: v.get("title", k) if isinstance(v, dict) else v for k, v in data.items()}
        return {}

    def get_options_data(self):
        conf_file = self.get_conf_file()
        if conf_file:
            data = conf_file.get_config()
            return {k: v for k, v in data.items() if isinstance(v, dict)}
        return {}

    def set_value(self, value):
        options = self.get_options()
        if value not in options:
            raise Exception(
                f"{self.key} value '{value}' not in options: {list(options.keys())}"
            )
        return super().set_value(value)

    def get_data(self):
        value = self.get_value()
        options_data = self.get_options_data()
        if value in options_data:
            return options_data[value]
        return {}

    def to_json(self):
        options = self.get_options()
        ret = super().to_json(type="select")
        ret["children"] = [dict(title=v, value=key) for key, v in options.items()]
        return ret