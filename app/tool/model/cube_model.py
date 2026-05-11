from common.tool.export import (
    FileConfig,
    StrModel,
    SearchModel,
    NumberModel,
    SelectModel,
    BoolModel,
    DateModel,
    ConfigBase,
)


class CubeModel(ConfigBase):
    axis = (
        SelectModel()
        .set_title("旋转轴")
        .set_options(**{"0": "X轴(垂直)", "1": "Y轴(水平)", "2": "Z轴(前后)"})
    )
    layer = SelectModel().set_title("层号").set_options(**{"0": "层0", "1": "层1"})
    rotate = (
        SelectModel()
        .set_title("旋转方向")
        .set_options(**{"-1": "逆时针", "1": "顺时针", "2": "180度"})
    )
    steps = NumberModel(default_value=1).set_title("步数")


CubeModel.init_param()
