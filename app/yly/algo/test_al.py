import pytest
from common.util.export import Module


class TestAl:
    @pytest.mark.parametrize(
        "algo,case_name",
        [
            ("lc_3883", "case0"),
        ],
    )
    def test_case(self, algo, case_name):
        ins = Module().load_module_object(f"app.yly.algo.todo.{algo}::Solution")()
        cases = ins.get_cases()[case_name]
        expected = cases.pop("expected")
        result = ins.execute(**cases)
        assert result == expected

    @pytest.mark.parametrize(
        "algo",
        [
            ("lc_3883"),
        ],
    )
    def test_all(self, algo):
        ins = Module().load_module_object(f"app.yly.algo.todo.{algo}::Solution")()
        cases = ins.get_cases()
        for case in cases.values():
            expected = case.pop("expected")
            result = ins.execute(**case)
            assert result == expected
