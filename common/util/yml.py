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
            value_str = s1[split_index + 1:].strip()
            # Only create entry if there's a key and it's not already in the parent
            if key:  # Ensure key is not empty
                while q and q[-1][0] >= indent:
                    q.pop()
                if key not in q[-1][1]:
                    value = value_parse(value_str) if value_str else ""
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
