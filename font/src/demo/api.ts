
import {
    Div, Constant, Node, web_dom, oj_to_node, Form, to_node, Search, Container
} from "../base/components/export";
const URIKEYID = "api_key"
export class Api extends Div {
    uri: Search
    input: Form
    result: Container
    init_node(): void {
        this.input = new Form()
        this.uri = new Search().set_option(to_node({
            url: "/app/tool/api/query_api",
            id: URIKEYID,
            title: "APIKEY",
            type: Constant.DATA_SOURCE_DYN
        }))

        this.result = new Container()
        this.add_childs([
            new Div().add_childs(
                [this.uri, this.input]),
            this.result
        ]).set_style_flex(
            Constant.VERTICAL
        ).full()
    }
    init_event(): void {
        this.uri.on_change((src: Node, dst: Node) => {
            this.input.set_option(oj_to_node(dst.data.kwargs))
        })
    }
    execute() {
        let info = this.uri.get_value()
        web_dom.post(info.key, this.input.get_value(), (v: Node) => {
            this.result.set_value(v)
        })
    }
    on_mount(): void {
        web_dom.get_local(URIKEYID, (v: any) => this.uri.set_value(v))

    }

}
export default function () {
    return new Api()
}