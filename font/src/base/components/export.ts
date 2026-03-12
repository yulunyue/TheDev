import { Input } from "./dom/form/input"
import { TextArea } from "./dom/form/text_area"
import { TextAreaRich } from "./dom/form/text_area_rich"
import { FileInput } from "./dom/form/file"
import { search, Search } from "./dom/form/search"
import { SvgNode, svg } from "./svg/svg"
import { Button } from "./dom/form/button"
import { Div, DivFactory, Container } from "./dom/div"
import { Row } from "./dom/base/row"
import { Column } from "./dom/base/column"
import { GNode } from "./svg/gnode"
import { Progress } from "./svg/comb/progress"
import { tree } from "./svg/comb/tree"
import { Grid } from './svg/comb/grid'
import { Table } from "./dom/table/main"
import { label, Pre, Label } from "./dom/label"
import { ListUi } from "./dom/list"
import Constant from "../../base/web/constant"
import { Node, node, to_node, oj_to_node } from "../../base/web/cls"
import web_dom from "../../base/web/web_dom"
import { Line } from "./svg/line"
import { Form } from "./dom/form/main"
import { FormRow } from "./dom/form/row"
import { Select } from "./dom/form/select";
import Mock from "../../model/mock"
import Util from "../tool/util"
import Data from "../tool/data"
import dialog from "./dom/dialog"
import web_socket from "../web/web_socket"

import Ct from "../../base/web/constant"
import { Chart } from "./svg/comb/chart"
import { Axies } from "./svg/comb/axies"

DivFactory.register(Ct.DOM_TYPE_INPUT, () => new Input())
DivFactory.register(Ct.DOM_TYPE_STRING, () => new Input())
DivFactory.register(Ct.DOM_TYPE_NUMBER, () => new Input())
DivFactory.register(Ct.DOM_TYPE_PRE, () => new Pre())
DivFactory.register(Ct.DOM_TYPE_ENUM, () => new Select())
DivFactory.register(Ct.DOM_TYPE_SEARCH, () => new Search())
DivFactory.register(Ct.DOM_TYPE_TABLE, () => new Table())
DivFactory.register(Ct.DOM_TYPE_GRID, () => new Grid())
DivFactory.register(Ct.DOM_TYPE_FILE, () => new FileInput())
export {
    Select, Pre, FormRow, TextArea, Util, web_socket, Data, Button,
    Div, SvgNode as Svg, svg, Progress, Input, web_dom, dialog, DivFactory,
    Constant, Node, Line, GNode, tree, Form, node,
    to_node, Grid, ListUi, Table, Ct, search, Search, TextAreaRich, label,
    Container, Label, oj_to_node, Chart, Axies, Mock, FileInput, Row, Column
}