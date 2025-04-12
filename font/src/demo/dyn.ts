
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, Row, node, Select, select, Pre, pre,
    line, gnode, GNode, button, progress, div, input, Input, Progress, DivFactory, row1, row2,
    text_area, TextArea, MeraGraph, to_node
} from "../base/components/export";
import fun from "../base/tool/fun";
import eval_func from "../demo/secmaster/manage"
export class Temaplate extends Div {

    init_node(): void {
        let path = web_dom.get_param("ts_file")
        if (path) {
            web_dom.get_ts(path, (fn: any) => {
                this.add_child(fn())
            })
        } else {
            this.add_child(eval_func())
        }
    }
    on_mount(): void {

    }

}
export default function () {
    return new Temaplate()
}