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
        .set_options(x="X轴(垂直)", y="Y轴(水平)", z="Z轴(前后)")
    )
    layer = SelectModel().set_title("层号").set_options(zero=0, one=1, two=2)
    rotate = (
        SelectModel()
        .set_title("旋转方向")
        .set_options(l1="-1(逆时针)", r1="1(顺时针)", r2="2(180度)")
    )
    steps = NumberModel(default_value=1).set_title("步数")


CubeModel.init_param()
