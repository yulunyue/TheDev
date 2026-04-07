from common.algo.base.str_util import z_kmp


class TestStrUtil:
    def test_zkmp(self):
        """
        z 函数第
        """
        assert z_kmp("abaabaababa") == [0, 0, 1, 6, 0, 1, 3, 0, 3, 0, 1]
