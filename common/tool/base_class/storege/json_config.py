from ..baseconfig import ConfigBase, BaseModel
from common.util.export import File


class JsonConfig(ConfigBase):
    @classmethod
    def init_resource(cls):
        cls.fp = File(cls.resource_path)
        for p in cls.get_params().values():
            p.set_datasource(cls)

    @classmethod
    def get_param_value(cls, param: BaseModel):
        return cls.fp.get(param.key, default_value=param.default_value)
