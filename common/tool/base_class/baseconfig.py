from common.util.export import (
    logger,
    File,
    json,
    C,
    List,
    Dict,
    hash_any_str,
    time,
    Self,
)
from .base_model.model import BaseModel


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
    def get_id_any(cls, **kw):
        if not kw:
            return time.time()
        return cls.get_id_by_param(**kw)

    @classmethod
    def get_id_by_param(cls, **kw):
        raise NotImplemented

    @classmethod
    def insert(cls, idx, **kw) -> "Self":
        cls.instance_map[idx] = cls.new(idx).update(**kw)
        return cls.instance_map[idx]

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

    @classmethod
    def all(cls) -> List[Self]:
        raise NotImplementedError

    @classmethod
    def get_default_conifg(cls):
        ret = dict()
        for key, v in cls.get_params().items():
            ret[key] = v.default_value
        return ret

    @classmethod
    def query(cls, key) -> Self:
        return cls.instance_map[key]

    @classmethod
    def get(cls, key) -> Self:
        if key in cls.instance_map:
            return cls.instance_map[key]
        return cls.insert(key)

    @classmethod
    def exist(cls, key):
        return key in cls.instance_map

    @classmethod
    def new(cls, key) -> Self:
        return cls().load(key)

    @classmethod
    def update_param_value(self, param, value):
        raise NotImplementedError

    @classmethod
    def get_param_value(self, param):
        raise NotImplemented

    def update(self, **kw) -> "Self":
        for k, v in kw.items():
            if k in self.params:
                self.params[k].set_value(v)
        return self

    @classmethod
    def init_param(cls):
        from common.tool.base_class.base_model.model import BaseModel

        cls.instance_map = dict()
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

    @classmethod
    def save_to_local(cls):
        raise NotImplementedError

    def save(self):
        self.__class__.save_to_local()

    def delete(self):
        self.instance_map.pop(self._id)
        return self

    @classmethod
    def get_form_columns(cls):
        return [v for v in cls.get_params().values()]

    @classmethod
    def set_resource(cls, path):
        cls.resource_path = path
        cls.init_param()
        cls.init_resource()
        return cls

    @classmethod
    def init_resource(cls):
        raise NotImplementedError

    @classmethod
    def filter(cls, key):
        ret: List[ConfigBase] = []
        for k, v in cls.instance_map.items():
            if key in str(k):
                ret.append(v)
        return ret

    def __repr__(self):
        return f"[id:{self._id}]"
