import { input, Input, text_area, TextArea, TextAreaRich } from "./dom/input"
import { search, Search } from "./dom/search"
import { canca_dev } from "./canva/canva"
import { SvgNode, svg } from "./svg/svg"
import { button, Button } from "./dom/button"
import { div, Div, DivFactory, Container, container } from "./dom/div"
import { gnode, GNode } from "./svg/gnode"
import { progress_dev, progress, Progress } from "./svg/comb/progress"
import { tree } from "./svg/comb/tree"
import { grid, Grid } from './svg/comb/grid'
import { Table } from "./dom/table"
import { label, pre, Pre } from "./dom/label"
import { listui, ListUi } from "./dom/list"
import { dagre_d3_dev } from "../../third/third_util"
import Constant from "../../base/web/constant"
import { Node, node, to_node } from "../../base/web/cls"
import web_dom from "../../base/web/web_dom"
import { line, Line } from "./svg/line"
import { Form, form, row1, row2, Row } from "./dom/form"
import { Select, select } from "./dom/select";
import Util from "../tool/util"
import Data from "../tool/data"
import dialog from "./dom/dialog"
import web_socket from "../web/web_socket"
import { mera_util, MeraGraph } from "./svg/comb/mermaid_util"
import Ct from "../../base/web/constant"

DivFactory.register("div", div)
DivFactory.register("Div", Div)
DivFactory.register("pre", pre)
DivFactory.register("tree", tree)
DivFactory.register('grid', grid)
DivFactory.register('search', search)
DivFactory.register('text_area', text_area)
// DivFactory.register("web_dom", web_dom)
DivFactory.register('button', button)
DivFactory.register("listui", listui)
DivFactory.register('graph', () => new MeraGraph())
export {
    Select, select, Pre, pre, Row, text_area, TextArea, Util, web_socket, Data, Button, MeraGraph, mera_util,
    Div, div, SvgNode as Svg, svg, progress, Progress, Input, web_dom, dialog, DivFactory,
    Constant, Node, line, Line, gnode, GNode, button, input, tree, Form, form, node, row1, row2,
    to_node, Grid, ListUi, Table, Ct, search, Search, TextAreaRich, label,
    Container, container
}