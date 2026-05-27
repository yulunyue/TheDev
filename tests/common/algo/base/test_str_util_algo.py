from common.algo.base.str_util_algo import z_kmp


class TestAlgoStrUtil:
    def test_zkmp(self):
        """
        z 函数第
        """
        assert z_kmp("abaabaababa") == [11, 0, 1, 6, 0, 1, 3, 0, 3, 0, 1]
