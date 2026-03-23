
import {
    Column, Row, Div, Constant, Node, web_dom, oj_to_node, to_node, Search, Container,
    Button,
    FormRow
} from "../base/components/export";
const URIKEYID = "api_key"
export class Api extends Column {
    uri: Search
    input: FormRow
    result: Container
    left_main: Div
    init_node(): void {
        this.input = new FormRow()
        this.uri = new Search().set_option({
            url: "/app/api/query_all_apis",
            title: "APIKEY",
            local_storge_enable: true
        })
        this.result = new Container()
        this.left_main = new Div().add_childs([
            this.uri,
            this.input
        ])
        this.add_childs([
            this.left_main,
            this.result
        ])
    }
    init_style(): void {
        this.left_main.set_style({
            minWidth: 240,
        })
        this.result.set_size(1)
        super.init_style()
    }
    init_event(): void {
        this.uri.on_change((key: string, src: Node, dst: Node) => {
            web_dom.post("/app/api/get_api_call_info", { key: dst.key }, (d) => {
                this.input.set_option(d)
            })
        })
        this.input.on_submit(this.execute.bind(this))
    }
    execute() {
        let info = this.uri.option.data
        web_dom.post(info.key, this.input.get_value(), (v: Node) => {
            v.type = v.type || Constant.DOM_TYPE_PRE
            this.result.set_option(v)
        })
    }
    render(): void {
        this.uri.set_id(URIKEYID)
    }

}
export default function () {
    return new Api()
}