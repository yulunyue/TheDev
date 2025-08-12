import { input, Input, text_area, TextArea, TextAreaRich } from "./dom/input"
import { search, Search } from "./dom/search"
import { SvgNode, svg } from "./svg/svg"
import { button, Button } from "./dom/button"
import { div, Div, DivFactory, Container } from "./dom/div"
import { GNode } from "./svg/gnode"
import { progress, Progress } from "./svg/comb/progress"
import { tree } from "./svg/comb/tree"
import { grid, Grid } from './svg/comb/grid'
import { Table } from "./dom/table/main"
import { label, pre, Pre, Label } from "./dom/label"
import { ListUi } from "./dom/list"
import Constant from "../../base/web/constant"
import { Node, node, to_node, oj_to_node } from "../../base/web/cls"
import web_dom from "../../base/web/web_dom"
import { Line } from "./svg/line"
import { Form } from "./dom/form/main"
import { FormRow } from "./dom/form/row"
import { Select, select } from "./dom/select";
import Util from "../tool/util"
import Data from "../tool/data"
import dialog from "./dom/dialog"
import web_socket from "../web/web_socket"

import Ct from "../../base/web/constant"
import { Chart } from "./svg/comb/chart"
import { Axies } from "./svg/comb/axies"

DivFactory.register(Ct.DOM_TYPE_INPUT, () => new Input())
DivFactory.register(Ct.DOM_TYPE_STRING, () => new Input())

DivFactory.register(Ct.DOM_TYPE_PRE, () => new Pre())
DivFactory.register(Ct.DOM_TYPE_ENUM, () => new Select())
DivFactory.register(Ct.DOM_TYPE_SEARCH, () => new Search())
DivFactory.register(Ct.DOM_TYPE_TABLE, () => new Table())
export {
    Select, Pre, FormRow as Row, TextArea, Util, web_socket, Data, Button,
    Div, div, SvgNode as Svg, svg, Progress, Input, web_dom, dialog, DivFactory,
    Constant, Node, Line, GNode, button, input, tree, Form, node,
    to_node, Grid, ListUi, Table, Ct, search, Search, TextAreaRich, label,
    Container, Label, oj_to_node, Chart, Axies
}