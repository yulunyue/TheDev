from .tool import json_get


def value_parse(s: str):
    s = s.strip()
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s


VALUE_KEY = "__VALUE"


class Yml:

    def str_to_dict(self, datas: str):
        q = [[-1, dict()]]
        for s in datas.split("\n"):
            if not s.strip():
                continue
            indent = 0
            while indent < len(s) and s[indent] == " ":
                indent += 2
            s1 = s[indent:].strip()
            if not s1 or s1.startswith("#"):
                continue
            split_index = s1.find(":")
            if split_index == -1:
                continue
            key = s1[:split_index].strip()
            value_str = s1[split_index + 1 :].strip()
            # Only create entry if there's a key and it's not already in the parent
            if key:  # Ensure key is not empty
                while q and q[-1][0] >= indent:
                    q.pop()
                if key not in q[-1][1]:
                    value = value_parse(value_str) if value_str else ""
                    if VALUE_KEY in q[-1][1]:
                        q[-1][1].pop(VALUE_KEY)
                    mp = q[-1][1][key] = {VALUE_KEY: value}
                    q.append([indent, mp])
        return q[0][1]

    def load(self, s):
        self.data = self.str_to_dict(s)
        return self

    def get(self, keys, defalut_value=None):
        ret = json_get(self.data, keys, {VALUE_KEY: defalut_value})
        if ret[VALUE_KEY] is None:
            raise Exception(self.data, keys)
        return ret[VALUE_KEY]

    def dfs(self, keys, value: dict, func):
        if VALUE_KEY in value:
            func(keys, value[VALUE_KEY], True)
            return
        if keys:
            func(keys, value, False)
        for k, v in value.items():
            ks = keys + [k]
            self.dfs(ks, v, func)

    def dumps(self, indent=2):
        ret = [""]

        def util(keys, value, is_leaf):
            head = " " * (len(keys) - 1) * indent + keys[-1]
            if is_leaf:
                ret.append(f"{head}: {value}")
            else:
                ret.append(f"{head}: ")

        self.dfs([], self.data, util)
        return "\n".join(ret + [""])

    def update(self, key, value):
        pass
