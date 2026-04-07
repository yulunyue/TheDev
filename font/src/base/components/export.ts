import { Input } from "./dom/form/input"
import { TextArea } from "./dom/form/text_area"
import { TextAreaRich } from "./dom/form/text_area_rich"
import { FileInput } from "./dom/form/file"
import { Search } from "./dom/form/search"
import { SvgNode } from "./svg/svg"
import { Button } from "./dom/form/button"
import { Div, DivFactory, Container } from "./dom/div"
import { Row } from "./dom/base/row"
import { Column } from "./dom/base/column"
import { GNode } from "./svg/gnode"
import { Progress } from "./svg/comb/progress"
import { tree } from "./svg/comb/tree"
import { Grid } from './svg/comb/grid'
import { Table } from "./dom/table/main"
import { Label } from "./dom/base/label"
import { Pre } from "./dom/base/pre"
import { Title } from "./dom/base/title"
import { Span } from "./dom/base/span"
import { ListUi } from "./dom/list"
import Constant from "../../base/web/constant"
import { Node, node, to_node, oj_to_node } from "../../base/web/cls"
import web_dom from "../../base/web/web_dom"
import { Line } from "./svg/line"
import { FormRow } from "./dom/form/form_row"
import { FormColumn } from "./dom/form/from_column"
import { Select } from "./dom/form/select";
import { Buttons } from "./dom/form/buttons"
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
DivFactory.register(Ct.DOM_TYPE_ROW, () => new Row())
DivFactory.register(Ct.DOM_TYPE_COLUMN, () => new Column())
DivFactory.register(Ct.DOM_TYPE_BUTTON, () => new Button())
DivFactory.register(Ct.DOM_TYPE_FORM_COLUMN, () => new FormColumn())
DivFactory.register(Ct.DOM_TYPE_FORM_ROW, () => new FormRow())
DivFactory.register(Ct.DOM_TYPE_SELECT, () => new Select())
DivFactory.register(Ct.DOM_TYPE_BTNS, () => new Buttons())
export {
    Select, Pre, TextArea, Util, web_socket, Data, Button,
    Div, SvgNode as Svg, Progress, Input, web_dom, dialog, DivFactory,
    Constant, Node, Line, GNode, tree, node, FormRow, FormColumn,
    to_node, Grid, ListUi, Table, Ct, Search, TextAreaRich, Title, Span,
    Container, Label, oj_to_node, Chart, Axies, Mock, FileInput, Row, Column
}