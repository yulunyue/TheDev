from typing import Dict
import xml.etree.ElementTree as ET
from common import function
import json
import re


def int_util(v):
    try:
        return int(v)
    except:
        return v


class XmlUtil:
    def __init__(self, data: str, namespace=None) -> None:
        self.namespace = namespace
        self.attr_key = "attr"
        self.child_key = "children"
        self.node_key = "node"
        if isinstance(data, dict):
            self.dictToXml(data)
        else:
            if data.endswith(".json"):
                with open(data, "r") as f:
                    self.dictToXml(json.loads(f.read()))
            elif data.endswith(".xml"):
                self._tree = ET.parse(data)
                self._root = self._tree.getroot()

        # function.log(self._root, self._tree)

    def toJson(self):
        rt = {}

        def util(p: ET.Element, dt: dict):
            rt[self.node_key] = p.tag
            if self.child_key not in dt:
                dt[self.child_key] = []
            dt[self.attr_key] = p.attrib
            for child in p:
                child_dict = dict()
                util(child, child_dict)
                dt[self.child_key].append(child_dict)

        util(self._root, rt)
        return rt

    def save(self, path: str):
        if path.endswith(".json"):
            with open(path, "w") as f:
                f.write(json.dumps(self.toJson(), indent=4))
        else:

            # function.log(s1)
            # ps: minidom.Document = minidom.parseString(
            #     s1)
            with open(path, "w") as f:
                f.write(self.toString())

    def toString(self):
        return ET.tostring(self._root).decode()

    def dictToXml(self, oj):
        def util(p):
            if self.node_key not in p or not p[self.node_key]:
                return
            rt = ET.Element(p[self.node_key])
            for key, value in p.get(self.attr_key, {}).items():
                rt.set(key, str(value))
            for child in p.get(self.child_key, []):
                if isinstance(child, str):
                    if rt.text is None:
                        rt.text = ""
                    rt.text = rt.text + str(child)
                else:
                    tmp = util(child)
                    if tmp is not None:
                        rt.append(tmp)
            return rt

        self._root = util(oj)
        self._tree = ET.ElementTree(self._root)

    def get(self, keys):
        rt = self._root
        for key in keys:
            rt = rt[key]
        return rt

    def __setitem__(self, key, value):
        keys = [int_util(d) for d in key.split("/")]
        p = self.get(keys[:-1])
        p.set(keys[-1], value)

    def __getitem__(self, key):
        keys = [int_util(d) for d in key.split("/")]
        p = self.get(keys[:-1])
        return p.get(keys[-1])


def M(_node_tmp_name, *args, **kwargs):
    ag = []

    def util(p):
        if isinstance(p, list):
            for d in p:
                util(d)
        else:
            ag.append(p)

    util(list(args))
    return dict(node=_node_tmp_name, children=ag, attr=kwargs)


def test1():
    c = XmlUtil(M("a1", M("ff:b", "abc"), c=1))
    c.save("data/test.xml")
    # c.save("data/test.xml")
    c1 = XmlUtil("data/test.xml")
    # function.log(c1["0"])


if __name__ == "__main__":
    test1()
