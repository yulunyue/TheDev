
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, dialog, Row, to_node, Select, Pre,
    GNode, Button, Input, Progress, DivFactory, Search, Container,
    TextArea,
    Column
} from "../base/components/export";

let URIKEYID = "ALGO_SEARCH"
class Algo extends Row {
    container: Container
    pro: Progress
    dialog_div: Form
    code_select: Search
    head_msg: Div
    head_container: Column
    head_run_btn: Button
    head_edit_btn: Button
    init_style(): void {
        //this.set_style_ab_full()
        this.container.set_size(1).full()
        this.head_msg.set_size(1)
        this.full()
        super.init_style()

    }
    init_node() {
        this.code_select = new Search().set_option(to_node({
            url: "/app/algo/search",
            id: URIKEYID,
            local_storge_enable: true
        }))
        this.container = new Container()
        this.pro = new Progress()
        this.head_msg = new Div()
        this.head_edit_btn = new Button().set_html("EDIT")
        this.head_run_btn = new Button().set_html("RUN")
        this.head_container = new Column().add_childs([
            this.head_msg,
            this.code_select,
            this.head_edit_btn,
            this.head_run_btn
        ])
        this.add_childs([
            this.head_container,
            this.container,
            this.pro,
        ])
    }

    init_event(): void {
        this.head_run_btn.on_click(() => this.run())

    }
    open_setting() {
        dialog.open(this.dialog_div)
    }

    render_option() {

    }
    goto() {
        let idx = this.pro.get_value()
        if (!this.option.data.record || !this.option.data.record[idx]) {
            return
        }
        for (var key in this.option.data.record[idx]) {
            let d = DivFactory.get(key)
            d.set_option(this.option.data.record[idx][key])
        }
    }
    test() {
    }

    get_case() {
        // return this.case_pre.get_value()
    }
    load() {
    }
    run() {
        web_dom.post('/app/algo/run', {
            code: this.code_select.get_value()
        }, (node: Node) => {
            this.pro.set_option({ childs: node.data.records })
            this.container.set_option(node.data.layout)
        })
    }
    on_mount() {


    }
}
export default function () {
    return new Algo()
}