from common.util.export import TestBase
from common.tool.export import Draw


class ToolTest(TestBase):
    def test_draw(self):
        Draw().draw_line([[[2, 3, 4], None, "line1"], [[7, 8, 9], None, "line2"]]).save(
            "data/temp/draw.svg"
        )


if __name__ == "__main__":
    ToolTest().run()
