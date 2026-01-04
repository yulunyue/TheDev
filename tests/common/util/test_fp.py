from common.util.export import File, TestBase, time


class TestFp(TestBase):
    def test_vs_code_log_file_refresh(self):
        """
        用肉眼观察文件的刷新
        """
        f = File.new("data/log/test_log.log")
        for i in range(10):
            f.write_file(str(i))
            time.sleep(0.2)


if __name__ == "__main__":
    TestFp().run()
