
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, Row, node, Select, select, Pre, pre,
    line, gnode, GNode, button, progress, div, input, Input, Progress, DivFactory, row1, row2,
    text_area, TextAreaRich, MeraGraph, to_node, search, Search
} from "../base/components/export";
export class Api extends Div {
    search: Search
    input: TextAreaRich
    result: TextAreaRich
    init_node(): void {
        this.input = text_area().set_title("输入")
        this.search = search().set_title("APIKEY").set_search(
            "/app/tool/api/query_api"
        ).enable_local_storge().on_change((node: Node) => {
            this.input.set_value(node.data.kwargs)
        }).set_id("api_key").set_btns([
            button().set_html("执行").click(() => { this.execute() })
        ])
        this.result = text_area().set_title("输出")
        this.add_childs([this.search, this.input, this.result])
    }
    execute() {
        let info = this.search.get_value()
        web_dom.post(info.key, this.input.get_value(), (v: Node) => {
            this.result.set_value(v)
        })
    }
    on_mount(): void {
        //this.search.emit_search()
    }

}
export default function () {
    return new Api()
}