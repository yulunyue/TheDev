from common.util.export import TestBase, logger
from common.third_util.draw import Draw
from common.third_util.pt_table import PtTable
from common.third_util.pynut_util import PynutUtil


class ThirdTest(TestBase):

    def draw(self):
        line_tmp_path = "data/draw/line"
        Draw().draw_line([4, 5, 6]).save(f"{line_tmp_path}/line1.svg")
        Draw().draw_lines(
            [[[2, 3, 4], None, "line1"], [[7, 8, 9], None, "line2"]]
        ).save(f"{line_tmp_path}/line2.svg")
        Draw().draw_lines([dict(a=1, b=2), dict(a=4, b=5)]).save(
            f"{line_tmp_path}/line3.svg"
        )

    def pttable(self):
        p = PtTable().load_from_matrix([[1] * 12, [4] * 12], list(range(12)))
        logger.info(p)

    def pynut(self):
        PynutUtil().run()


if __name__ == "__main__":
    ThirdTest().run()
