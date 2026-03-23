import json
from typing import List, Type
from ..constant import THE_DEV_CONSTANT, CT
from .tool import uid


class Node:
    type = ""

    def __init__(
        self,
        code=0,
        type="",
        key="",
        title="",
        size=0,
        value=None,
        data=None,
        childs=None,
    ) -> None:
        self.code = code
        if type:
            self.type = type
        self.key = key or uid("node")
        self.title = title
        self.value = value
        self.size = size
        self.data = data or dict()
        self.parent = None
        self.childs: List[Node] = []
        if childs:
            for cd in childs:
                if isinstance(cd, dict):
                    self.add_child(**cd)
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

    def add_child(
        self,
        code=0,
        type="",
        key="",
        title="",
        value=None,
        data=None,
        childs=None,
    ):
        ret = Node(
            code=code,
            type=type,
            key=key,
            title=title,
            value=value,
            data=data,
            childs=childs,
        )
        self.childs.append(ret)
        ret.parent = self
        return ret

    @classmethod
    def get_dom_type(cls, v):
        return v

    def add_node(self, *args):
        for n in args:
            self.childs.append(self.__class__.get_dom_type(n))
        return self

    def to_json(self, **kw):
        ret = dict(
            type=self.type,
            key=self.key,
            title=self.get_title(),
            value=self.value,
            childs=self.childs,
            data=self.get_data(),
        )
        ret.update(kw)
        return ret

    def get_childs(self):
        return self.childs

    def get_title(self):
        return self.title

    def get_data(self):
        return self.data

    def __str__(self):
        return json.dumps(self.to_json(), indent=4, ensure_ascii=False)


def cls_util(tp, **kw):
    class T:
        type_info = dict(type=tp, **kw)

    return T


def enum_cls(*enums) -> Type[Node]:
    return cls_util("enum", childs=list(enums))


def search_cls(url):
    return cls_util("search", url=url)
