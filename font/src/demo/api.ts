
import {
    Column, Row, Div, Constant, Node, web_dom, oj_to_node, to_node, Search, Container,
    Button,
    FormRow
} from "../base/components/export";
const URIKEYID = "api_key"
const INPUT_ID = "ID_API_INPUT"
export class Api extends Column {
    uri: Search
    input: FormRow
    result: Container
    left_main: Div
    init_node(): void {
        this.input = new FormRow()
        this.uri = new Search().set_option({
            url: "/app/api/query_all_apis",
            id: URIKEYID,
            title: "APIKEY"
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
            web_dom.post("/app/api/get_api_call_info", { key: dst }, (d) => {
                this.input.set_option(d)
                let data = this.local_data[this.uri.get_value()]
                if (data) {
                    this.input.set_value(data)
                }
            })
        })
        this.input.on_change(this.input_on_change.bind(this))
        this.input.on_submit(this.execute.bind(this))
    }
    input_on_change(key: string, src?: any, dst?: any) {
        // console.log(key, src, dst)
        this.local_data[this.uri.get_value()] = this.input.get_value()
        web_dom.set_local(INPUT_ID, this.local_data)
    }
    execute() {
        web_dom.post(this.uri.input.get_value(), this.input.get_value(), (v: Node) => {
            if (!v.type) {
                this.result.set_option({ type: Constant.DOM_TYPE_PRE, value: v })
            } else {
                this.result.set_option(v)
            }

        })
    }
    local_data: any
    render(): void {
        this.local_data = web_dom.get_local_data(INPUT_ID, {})
        console.log(this.local_data)
    }

}
export default function () {
    return new Api()
}