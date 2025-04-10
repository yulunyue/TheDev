
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, Row, node, Select, select, Pre, pre,
    line, gnode, GNode, button, progress, div, input, Input, Progress, DivFactory, row1, row2,
    text_area, TextArea, MeraGraph, to_node
} from "../base/components/export";
import fun from "../base/tool/fun";
export class Temaplate extends Div {

    init_node(): void {

    }
    on_mount(): void {
        web_dom.get_ts(web_dom.get_param("ts_file", "/font/src/demo/eval.ts"), (data: any) => {
            console.log(data)
        })
    }

}
export default function () {
    return new Temaplate()
}