from common.algo.base.math_util import prime_gcds, gcd_primes


class TestMathUtil:
    def test_prime(self):
        assert prime_gcds(10) == [
            None,
            None,
            None,
            None,
            {2},
            None,
            {2, 3},
            None,
            {2},
            {3},
        ]
        assert gcd_primes(10) == [[], [], [2], [3], [2], [5], [2, 3], [7], [2], [3]]
