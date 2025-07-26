from common.util.export import TestBase
from common.tool.export import Draw, ThreadRecord


class ToolTest(TestBase):
    def test_draw(self):
        line_tmp_path = "data/draw/line"
        Draw().draw_line([4, 5, 6]).save(f"{line_tmp_path}/line1.svg")
        Draw().draw_lines(
            [[[2, 3, 4], None, "line1"], [[7, 8, 9], None, "line2"]]
        ).save(f"{line_tmp_path}/line2.svg")
        Draw().draw_lines([dict(a=1, b=2), dict(a=4, b=5)]).save(
            f"{line_tmp_path}/line3.svg"
        )

    def test_thread_record(self):
        class Test(ThreadRecord):
            def init(self):
                self.a = 0
                self.b = 0

            def exec_main(self):
                for i in range(3):
                    self.b += i
                    self.a += i
                return self.a

            def __str__(self):
                return f"{self.a}"

            def to_josn(self):
                return dict(a=self.a, b=self.b)

        s = Test().execute()
        self.expect(s.result, 3)
        self.expect(s.records, [{"a": 0, "b": 0}, {"a": 1, "b": 1}, {"a": 3, "b": 3}])


if __name__ == "__main__":
    ToolTest().run()
