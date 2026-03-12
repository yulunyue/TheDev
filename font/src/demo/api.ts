
import {
    Column, Row, Div, Constant, Node, web_dom, oj_to_node, Form, to_node, Search, Container,
    Button
} from "../base/components/export";
const URIKEYID = "api_key"
export class Api extends Column {
    uri: Search
    input: Form
    result: Container
    exec_btn: Button
    init_node(): void {
        this.input = new Form()
        this.uri = new Search().set_option(to_node({
            url: "/app/api/query_all_apis",
            id: URIKEYID,
            title: "APIKEY",
            local_storge_enable: true
        }))
        this.exec_btn = new Button().set_html("执行")
        this.result = new Container()
        this.add_childs([
            new Div().add_childs([
                new Column().add_childs([
                    this.uri,
                    this.exec_btn,
                ]),
                this.input
            ]).set_style({
                minWidth: 240,
            }),
            this.result
        ])
    }

    init_event(): void {
        this.uri.on_change((src: Node, dst: Node) => {
            web_dom.post("/app/api/get_api_call_info", { key: dst.key }, (d) => {
                this.input.set_option(d)
            })
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


    }

}
export default function () {
    return new Api()
}