from common.util.export import TestBase, logger
from common.tool.export import (
    Draw,
    ThreadRecord,
    OsUtil,
    TableBase,
    StrModel,
    NumberModel,
    TableConfig,
    TestTableConfig,
    TestRc,
    get_task,
)


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

    def test_os(self):
        b = OsUtil().check_output("ls")
        self.expect(b, "")

    def test_thread_record(self):
        s = TestRc().execute()
        self.expect(s.result, 3)
        self.expect(s.records, [{"a": 0, "b": 0}, {"a": 1, "b": 1}, {"a": 3, "b": 3}])

    def test_table(self):
        t = TableBase().set_model(
            TestTableConfig().set_resource("data/setting/test_table.json")
        )
        t.add_row_data(a="a", b=1)
        t.add_row_data(a="b", b=2)
        t.save()
        logger.info(t.to_web_view())

    def test_task(self):
        t = get_task("taskconfig")
        t.loop()
        t.save()


if __name__ == "__main__":
    ToolTest().run()
