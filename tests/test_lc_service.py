import pytest
from io import StringIO
from contextlib import redirect_stdout
from tool.service.lc import Lc, parse_case


class TestLcService:
    def test_instantiate(self):
        lc = Lc()
        assert hasattr(lc, "read")
        assert hasattr(lc, "check")
        assert hasattr(lc, "submit")
        assert lc.name == "lc"

    @pytest.mark.skip(reason="Requires LeetCode API and valid auth")
    def test_read_success(self):
        lc = Lc()
        buf = StringIO()
        with redirect_stdout(buf):
            lc.read("2770")
        out = buf.getvalue()
        assert "#2770." in out
        assert "难度:" in out
        assert "Python3 模板:" in out
        assert "本地文件:" in out

    @pytest.mark.skip(reason="Requires LeetCode API")
    def test_read_not_found(self):
        lc = Lc()
        buf = StringIO()
        with redirect_stdout(buf):
            lc.read("99999999")
        assert "未找到题目" in buf.getvalue()

    @pytest.mark.skip(reason="Requires LeetCode API and valid auth")
    def test_read_fresh(self):
        lc = Lc()
        buf = StringIO()
        with redirect_stdout(buf):
            lc.read("2770", "--fresh")
        out = buf.getvalue()
        assert "#2770." in out

    def test_parse_case_json_array(self):
        result = parse_case('"[1,2,3]"')
        assert result == [[1, 2, 3]]

    def test_parse_case_single(self):
        result = parse_case("2")
        assert result == [2]

    def test_parse_case_space_separated(self):
        result = parse_case('"1 2 3"')
        assert result == ["1 2 3"]
