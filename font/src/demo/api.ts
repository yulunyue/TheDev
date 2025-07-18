
import {
    Div, Constant, Node, web_dom, oj_to_node, Form, to_node, Search, Container,
    Button
} from "../base/components/export";
const URIKEYID = "api_key"
export class Api extends Div {
    uri: Search
    input: Form
    result: Container
    exec_btn: Button
    init_node(): void {
        this.input = new Form()
        this.uri = new Search().set_option(to_node({
            url: "/app/api/query_api",
            id: URIKEYID,
            title: "APIKEY",
            type: Constant.DATA_SOURCE_DYN,
            local_storge_enable:true
        }))
        this.exec_btn = new Button().set_html("执行")
        this.result = new Container()
        this.add_childs([
            new Div().add_childs([
                new Div().add_childs([
                    this.uri,
                    this.exec_btn,
                ]).set_style_flex(Constant.VERTICAL),
                this.input
            ]),
            this.result
        ])
    }
    init_style(): void {
        this.set_style_flex(
            Constant.VERTICAL
        ).full()
        this.result.set_flex_grow(1)
    }
    init_event(): void {
        this.uri.on_change((src: Node, dst: Node) => {
            this.input.set_option(oj_to_node(dst.data.kwargs))
        })
        this.exec_btn.on_click(() => this.execute())
    }
    execute() {
        let info = this.uri.get_value()
        web_dom.post(info.key, this.input.get_value(), (v: Node) => {
            v.type = v.type || Constant.DOM_TYPE_PRE
            this.result.set_option(v)
        })
    }
    on_mount(): void {
        web_dom.get_local(URIKEYID, (v: any) => this.uri.set_value(v))

    }

}
export default function () {
    return new Api()
}