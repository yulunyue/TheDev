import { input, Input } from "./dom/input"
import { search, search_dev } from "./dom/search"
import { select } from "./dom/select"
import { canca_dev } from "./canva/canva"
import { Svg, svg, svg_dev } from "./svg/svg"
import { button_dev, button } from "./dom/button"
import { div, Div, DivFactory } from "./dom/div"
import { gnode, GNode } from "./svg/gnode"
import { progress_dev, progress, Progress } from "./svg/comb/progress"
import { tree } from "./svg/comb/tree"
import { table } from "./dom/table"
import { label_dev } from "./dom/label"
import { listui, listdev } from "./dom/list"
import { dagre_d3_dev } from "../../third/third_util"
import Constant from "../../base/web/constant"
import { Node, node } from "../../base/web/cls"
import web_dom from "../../base/web/web_dom"
import { line, Line } from "./svg/line"
import { Form, form } from "./dom/form"
import dialog from "./dom/dialog"
const DEV_COMPONENT = {
    input, search_dev, select, canca_dev, svg_dev,
    button_dev, table, listdev, label_dev,
    dagre_d3_dev, progress_dev
}
DivFactory.register("div", div)
DivFactory.register("tree", tree)
export {

    DEV_COMPONENT, Div, div, Svg, svg, progress, Progress, Input, web_dom, dialog,
    Constant, Node, line, Line, gnode, GNode, button, input, tree, Form, form, node
}