import json
from typing import List, Type
from ..constant import THE_DEV_CONSTANT, CT
from .tool import uid


class Node:
    type = ""

    def __init__(
        self,
        code=None,
        type="",
        key="",
        title="",
        size=None,
        value=None,
        data=None,
        children=None,
        ok=None,
    ) -> None:
        self.code = code
        if type:
            self.type = type
        self.key = key
        self.title = title
        self.value = value
        self.size = size
        self.ok = ok
        self.data = data or dict()
        self.parent = None
        self.childs: List[Node] = []
        if children:
            for cd in children:
                if isinstance(cd, dict):
                    self.add_child(cd)
                else:
                    self.childs.append(cd)
        self.init()

    def set_value(self, v):
        self.value = v
        return self

    def init(self):
        pass

    def set_type(self, tp):
        self.type = tp
        return self

    def set_key(self, key):
        self.key = key
        return self

    def set_title(self, title):
        self.title = title
        return self

    def set_data(self, **kw):
        for k, v in kw.items():
            self.data[k] = v
        return self

    def add_child(self, data):
        self.childs.append(data)
        return data

    def get_type(self):
        return self.type

    def add_childs(self, *args):
        for a in args:
            self.add_child(a)
        return self

    def get_value(self):
        return self.value

    def to_json(self, **kw):
        ret = dict(
            type=self.get_type(),
            key=self.key or self.get_title(),
            title=self.get_title(),
            value=self.get_value(),
            children=self.childs,
            data=self.get_data(),
        )
        if self.ok is not None:
            ret["ok"] = self.ok
        ret.update(kw)
        return ret

    def get_childs(self):
        return self.childs

    def get_title(self):
        return self.title

    def get_data(self):
        return self.data

    def to_dict(self):
        return self.to_json()

    def to_json_str(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json_str(cls, s: str):
        return cls(**json.loads(s))


def cls_util(tp, **kw):
    class T:
        type_info = dict(type=tp, **kw)

    return T


def enum_cls(*enums) -> Type[Node]:
    return cls_util("enum", children=list(enums))


def search_cls(url):
    return cls_util("search", url=url)
