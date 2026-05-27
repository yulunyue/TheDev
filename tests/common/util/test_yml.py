from common.util.export import TestBase
from common.util.yml import Yml, VALUE_KEY

A = """
b: 
  c: d
  e: f
  g: 'h'
c: "f"
f: 
"""


class TestYml(TestBase):
    def test_yml_to_dict(self):
        d = Yml().load(A)
        self.expect(
            d.data,
            {
                "b": {
                    "c": {VALUE_KEY: "d"},
                    "e": {VALUE_KEY: "f"},
                    "g": {VALUE_KEY: "h"},
                },
                "c": {VALUE_KEY: "f"},
                "f": {VALUE_KEY: ""},
            },
        )
        self.expect(d.get("b.g"), "h")
        dump_str = A.replace("'", "").replace('"', "")
        self.expect(d.dumps(), dump_str)
