from common.util.export import TestBase
from common.util.yml import Yml, VALUE_KEY


class TestYml(TestBase):
    def test_yml_to_dict(self):
        a = """
b:
  c: d
  e: f
  g: 'h'

c: "f"
f:
"""
        d = Yml().load(a)
        self.expect(
            d.data,
            {
                "b": {
                    VALUE_KEY: "",
                    "c": {VALUE_KEY: "d"},
                    "e": {VALUE_KEY: "f"},
                    "g": {VALUE_KEY: "h"},
                },
                "c": {VALUE_KEY: "f"},
                "f": {VALUE_KEY: ""},
            },
        )
        self.expect(d.get("b.g"), "h")
