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
            if not s:
                continue
            indent = 0
            while indent < len(s) and s[indent] == " ":
                indent += 2
            s1 = s[indent:]
            split_index = s1.find(":")
            if split_index == -1:
                continue
            key, value = s1[:split_index], value_parse(s1[split_index + 2 :])
            while q and q[-1][0] >= indent:
                q.pop()
            mp = q[-1][1][key] = {VALUE_KEY: value}
            q.append([indent, mp])
        return q[0][1]

    def load(self, s):
        self.data = self.str_to_dict(s)
        return self

    def get(self, keys, defalut_value=None):
        keys = keys
        if isinstance(keys, str):
            keys = keys.split(".")
        ret = self.data
        for key in keys:
            if key not in ret:
                if defalut_value is None:
                    raise Exception(keys, list(ret.keys()))
                return defalut_value
            ret = ret[key]
        return ret[VALUE_KEY]
