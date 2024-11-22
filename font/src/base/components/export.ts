import { input, Input, text_area, TextArea } from "./dom/input"
import { search, search_dev } from "./dom/search"
import { canca_dev } from "./canva/canva"
import { Svg, svg, svg_dev } from "./svg/svg"
import { button_dev, button } from "./dom/button"
import { div, Div, DivFactory } from "./dom/div"
import { gnode, GNode } from "./svg/gnode"
import { progress_dev, progress, Progress } from "./svg/comb/progress"
import { tree } from "./svg/comb/tree"
import { table } from "./dom/table"
import { label, pre, Pre } from "./dom/label"
import { listui, listdev } from "./dom/list"
import { dagre_d3_dev } from "../../third/third_util"
import Constant from "../../base/web/constant"
import { Node, node } from "../../base/web/cls"
import web_dom from "../../base/web/web_dom"
import { line, Line } from "./svg/line"
import { Form, form, row1, row2, Row } from "./dom/form"
import { Select, select } from "./dom/select";

import dialog from "./dom/dialog"
const DEV_COMPONENT = {
    input, search_dev, Select, select, canca_dev, svg_dev,
    button_dev, table, listdev,
    dagre_d3_dev, progress_dev
}
DivFactory.register("div", pre)
DivFactory.register("tree", tree)
export {
    Select, select, Pre, pre, Row, text_area, TextArea,
    DEV_COMPONENT, Div, div, Svg, svg, progress, Progress, Input, web_dom, dialog, DivFactory,
    Constant, Node, line, Line, gnode, GNode, button, input, tree, Form, form, node, row1, row2
}