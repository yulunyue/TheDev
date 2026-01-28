from common.util.export import TestBase, uid, base64_encode, ii, hash_any, md5, random


class TestTool(TestBase):
    def test_uid(self):
        self.expect(uid("a"), "a_0")
        self.expect(uid("a"), "a_1")

    def test_base64(self):
        a = base64_encode("s")
        self.expect(a, "cw==")

    def test_ii(self):
        self.expect(ii("2 4  a9 9a 7"), [2, 4, 7])

    def test_hash_any(self):
        self.expect(hash_any("aa"), "aa")
        self.expect(hash_any([0, 1, 2]), "012")
        self.expect(hash_any(dict(a=1)), "a1")

    def test_md5(self):
        self.expect(md5("aa"), "4124bc0a9335c27f086f24ba207a4912")

    def test_random(self):
        random.seed(0)
        ins = [random.randint(1, 100) for _ in range(20)]
        random.seed(0)
        e = [random.randint(1, 100) for _ in range(20)]
        self.expect(ins, e)
