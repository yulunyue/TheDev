from common.util.export import logger, File, json, List, Dict
from .model import BaseModel
from ..front.table import FrontTable
from ..front.form import Form


class ConfigBase:
    _params_cls_map: Dict[str, BaseModel] = None
    resource_path = ""
    _id = None

    def load(self, _id):
        self._id = _id
        self.params: Dict[str, BaseModel] = dict()
        for k, v in self.get_params().items():
            c = v.clone().set_datasource(self).set_key(k)
            setattr(self, k, c)
            self.params[k] = c
        self.init()
        return self

    @classmethod
    def get_headers_keys(cls):
        return cls.get_params().keys()

    def init(self):
        pass

    @classmethod
    def get_params(self):
        if self._params_cls_map is None:
            self.init_param()
        return self._params_cls_map

    front_apis = ["to_form_view", "to_table_view"]

    @classmethod
    def to_form_view(cls):
        return Form().set_body(*cls.get_params().values())

    @classmethod
    def to_table_view(cls):
        return FrontTable().set_header(*cls.get_params().values()).set_body(cls.all())

    @classmethod
    def all(cls):
        raise NotImplementedError

    @classmethod
    def get_default_conifg(cls):
        ret = dict()
        for key, v in cls.get_params().items():
            ret[key] = v.default_value
        return ret

    @classmethod
    def update_param_value(self, param, value):
        raise NotImplementedError

    @classmethod
    def get_param_value(self, param):
        raise NotImplemented

    def update(self, **kw):
        for k, v in kw.items():
            if k in self.params:
                self.params[k].set_value(v)
        return self

    @classmethod
    def init_param(cls):
        from common.tool.base_class.model import BaseModel

        cls._params_cls_map = dict()
        for key in dir(cls):
            if key.startswith("_"):
                continue
            v = getattr(cls, key)
            if not isinstance(v, BaseModel):
                continue
            cls._params_cls_map[key] = v.set_key(key)
        return cls

    def to_json(self):
        ret = dict(_id=self._id)
        ret.update({v.key: v.get_value() for v in self.params.values()})
        return ret

    def save(self):
        if self.resource is None:
            return self
        cg = dict()
        if self.resource.exists():
            cg = self.resource.get_config()
        cg.update(self.to_json())
        logger.debug(self.resource)
        self.resource.write_file(cg)
        return self

    @classmethod
    def set_resource(cls, path):
        cls.resource_path = path
        cls.init_param()
        cls.init_resource()
        return cls

    @classmethod
    def init_resource(cls):
        raise NotImplementedError

    def __repr__(self):
        return f"[id:{self._id}]"
