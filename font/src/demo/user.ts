
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, Row, node, Select, select, Pre, pre,
    line, gnode, GNode, button, progress, div, input, Input, Progress, DivFactory, row1, row2,
    text_area, TextArea, MeraGraph, to_node, Table
} from "../base/components/export";
export class User extends Div {
    table: Table
    init_node(): void {
        this.table = this.add_child(new Table())
    }
    on_mount(): void {

    }

}
export default function () {
    return new User()
}