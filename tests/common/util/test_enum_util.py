import unittest

from common.util.enum_util import EnumCls, auto, auto_reset
from common.exception import ValidationError


class TestEnumCls(unittest.TestCase):

    def setUp(self):
        auto_reset()

    def test_to_str_int(self):
        class Status(EnumCls):
            ACTIVE = 1
            INACTIVE = 0
            PENDING = 2

        st = Status()
        self.assertEqual(st.to_str(1), "ACTIVE")
        self.assertEqual(st.to_str(0), "INACTIVE")
        self.assertEqual(st.to_str(2), "PENDING")

    def test_to_str_string(self):
        class Colors(EnumCls):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"

        c = Colors()
        self.assertEqual(c.to_str("red"), "RED")
        self.assertEqual(c.to_str("green"), "GREEN")
        self.assertEqual(c.to_str("blue"), "BLUE")

    def test_to_str_invalid(self):
        class Status(EnumCls):
            ACTIVE = 1

        st = Status()
        with self.assertRaises(ValidationError):
            st.to_str(999)

    def test_skips_private(self):
        class TestEnum(EnumCls):
            PUBLIC_VALUE = 1
            _PRIVATE_VALUE = 2

        te = TestEnum()
        self.assertEqual(te.to_str(1), "PUBLIC_VALUE")
        with self.assertRaises(ValidationError):
            te.to_str(2)

    def test_skips_non_primitive(self):
        class MixedEnum(EnumCls):
            INT_VALUE = 1
            STR_VALUE = "string"
            LIST_VALUE = [1, 2, 3]

        me = MixedEnum()
        self.assertEqual(me.to_str(1), "INT_VALUE")
        self.assertEqual(me.to_str("string"), "STR_VALUE")
        self.assertNotIn([1, 2, 3], me)
        self.assertNotIn({"key": "value"}, me)

    def test_from_str(self):
        class Status(EnumCls):
            ACTIVE = 1
            INACTIVE = 0

        st = Status()
        self.assertEqual(st.from_str("ACTIVE"), 1)
        self.assertEqual(st.from_str("INACTIVE"), 0)

    def test_from_str_invalid(self):
        class Status(EnumCls):
            ACTIVE = 1

        st = Status()
        with self.assertRaises(ValidationError):
            st.from_str("NONEXISTENT")

    def test_contains(self):
        class Status(EnumCls):
            ACTIVE = 1

        st = Status()
        self.assertIn(1, st)
        self.assertNotIn(999, st)

    def test_values(self):
        class Status(EnumCls):
            ACTIVE = 1
            INACTIVE = 0

        st = Status()
        self.assertEqual(sorted(st.values()), [0, 1])

    def test_names(self):
        class Status(EnumCls):
            ACTIVE = 1
            INACTIVE = 0

        st = Status()
        self.assertEqual(sorted(st.names()), ["ACTIVE", "INACTIVE"])

    def test_items(self):
        class Status(EnumCls):
            ACTIVE = 1
            INACTIVE = 0

        st = Status()
        items = dict(st.items())
        self.assertEqual(items[1], "ACTIVE")
        self.assertEqual(items[0], "INACTIVE")

    def test_repr(self):
        class Status(EnumCls):
            ACTIVE = 1

        st = Status()
        r = repr(st)
        self.assertIn("Status", r)
        self.assertIn("ACTIVE", r)


class TestAutoFunction(unittest.TestCase):

    def setUp(self):
        auto_reset()

    def test_sequential(self):
        values = [auto() for _ in range(5)]
        self.assertEqual(values, [0, 1, 2, 3, 4])

    def test_start_value(self):
        result = auto(100)
        self.assertEqual(result, 100)
        self.assertEqual(auto(), 101)

    def test_none(self):
        result = auto(None)
        self.assertEqual(result, 0)
        self.assertEqual(auto(), 1)

    def test_negative(self):
        auto(-10)
        self.assertEqual(auto(), -9)
        self.assertEqual(auto(), -8)


class TestEnumIntegration(unittest.TestCase):

    def setUp(self):
        auto_reset()

    def test_with_auto_values(self):
        class AutoEnum(EnumCls):
            FIRST = auto()
            SECOND = auto()
            THIRD = auto()

        ae = AutoEnum()
        self.assertEqual(ae.to_str(0), "FIRST")
        self.assertEqual(ae.to_str(1), "SECOND")
        self.assertEqual(ae.to_str(2), "THIRD")

    def test_mixed_values(self):
        class MixedEnum(EnumCls):
            FIXED = 100
            AUTO1 = auto()
            AUTO2 = auto()
            STRING = "custom"

        me = MixedEnum()
        self.assertEqual(me.to_str(100), "FIXED")
        self.assertEqual(me.to_str(0), "AUTO1")
        self.assertEqual(me.to_str(1), "AUTO2")
        self.assertEqual(me.to_str("custom"), "STRING")

    def test_inheritance(self):
        class BaseEnum(EnumCls):
            BASE_VALUE = 1

        class DerivedEnum(BaseEnum):
            DERIVED_VALUE = 2

        de = DerivedEnum()
        self.assertEqual(de.to_str(1), "BASE_VALUE")
        self.assertEqual(de.to_str(2), "DERIVED_VALUE")


class TestEnumEdgeCases(unittest.TestCase):

    def setUp(self):
        auto_reset()

    def test_empty(self):
        class EmptyEnum(EnumCls):
            pass

        ee = EmptyEnum()
        self.assertEqual(ee.values(), [])
        with self.assertRaises(ValidationError):
            ee.to_str(0)

    def test_duplicate(self):
        class DuplicateEnum(EnumCls):
            VALUE1 = 1
            VALUE2 = 1

        de = DuplicateEnum()
        self.assertEqual(de.to_str(1), "VALUE2")

    def test_zero_negative(self):
        class NumberEnum(EnumCls):
            ZERO = 0
            NEGATIVE = -1
            POSITIVE = 1

        ne = NumberEnum()
        self.assertEqual(ne.to_str(0), "ZERO")
        self.assertEqual(ne.to_str(-1), "NEGATIVE")
        self.assertEqual(ne.to_str(1), "POSITIVE")


class TestAutoIsolation(unittest.TestCase):

    def setUp(self):
        auto_reset()

    def test_class_isolation(self):
        class Fruit(EnumCls):
            APPLE = auto()
            BANANA = auto()

        class Color(EnumCls):
            RED = auto()
            BLUE = auto()

        f = Fruit()
        c = Color()
        self.assertEqual(f.to_str(0), "APPLE")
        self.assertEqual(f.to_str(1), "BANANA")
        self.assertEqual(c.to_str(0), "RED")
        self.assertEqual(c.to_str(1), "BLUE")

    def test_class_cache(self):
        class Status(EnumCls):
            ACTIVE = 1

        s1 = Status()
        s2 = Status()
        self.assertIs(type(s1)._value_to_name, type(s2)._value_to_name)
