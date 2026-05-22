
import {
    FlexRow, FlexColumn, Div, Constant, Node, web_dom, oj_to_node, to_node, Search, Container,
    Button,
    FormRow,
    ListContainer
} from "../base/components/export";
import { U } from "../base/tool/export"
const URIKEYID = "api_key"
const INPUT_ID = "ID_API_INPUT"
export class Api extends FlexRow {
    uri: Search
    input: FormRow
    result: Container
    head_title_right: Div
    head_title_left: Div
    right_head: FlexRow
    right_main: FlexColumn
    left_main: FlexColumn
    running_url: string
    log_container: ListContainer
    init_node(): void {
        this.input = new FormRow().set_btns({ [Constant.METHOD_RUN]: "执行" })
        this.uri = new Search().set_option({
            url: "/app/api/query_all_apis",
            id: URIKEYID,
            title: "APIKEY"
        })
        this.result = new Container()
        this.left_main = new FlexColumn().add_children([
            this.uri,
            this.input
        ])
        this.head_title_left = new Div().set_html("left")
        this.head_title_right = new Div().set_html("right")
        this.right_head = new FlexRow().add_children([
            this.head_title_left,
            this.head_title_right
        ])
        this.log_container = new ListContainer()
        this.right_main = new FlexColumn().add_children([
            this.right_head,
            this.result,
            this.log_container
        ])
        this.add_children([
            this.left_main,
            this.right_main
        ])
    }
    init_style(): void {
        this.left_main.set_style({
            minWidth: 240,
        })
        this.right_main.set_size(1)
        this.result.set_size(1)
        this.log_container.set_style({
            height: 200
        })
        this.head_title_left.set_size(1)
        this.set_style({
            height: "100%"
        })
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
        this.log_container.sub(Constant.TOPIC_WEB_LOG)
        this.input.on_change(this.input_on_change.bind(this))
        this.input.on_submit(this.execute.bind(this))
    }
    input_on_change(key: string, src?: any, dst?: any) {
        // console.log(key, src, dst)
        this.local_data[this.uri.get_value()] = this.input.get_value()
        web_dom.set_local(INPUT_ID, this.local_data)
    }
    loop(idx: number) {
        if (!this.running_url) {
            return
        }
        this.head_title_left.set_html(this.running_url + ": run " + U.array(idx, () => "&#9679;").join(""))
        web_dom.set_time_out(() => {
            this.loop((idx + 1) % 15)
        }, 1000)
    }
    execute() {
        if (this.running_url) {
            web_dom.alert(this.running_url + ": runing")
            return
        }
        this.running_url = this.uri.input.get_value()
        this.loop(0)
        web_dom.post(this.running_url, this.input.get_value(), (v: Node) => {
            if (!v.type) {
                this.result.set_option({ type: Constant.DOM_TYPE_PRE, value: v })
            } else {
                this.result.set_option(v)
            }

        }, () => {
            this.head_title_left.set_html(this.running_url + ": finish")
            this.running_url = ""
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