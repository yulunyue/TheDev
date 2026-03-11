
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, dialog, Row, node, Select, Pre,
    GNode, button, div, Input, Progress, DivFactory,
    TextArea
} from "../base/components/export";


class Algo extends Div {
    div: Div
    pro: Progress
    dialog_div: Form
    code_select: Row
    code_pre: Row
    case_select: Row
    case_pre: Row
    init_style(): void {
        this.set_style_ab_full()
    }
    init_edit_dialog() {
        // this.code_select = row1().set_input(
        //     select()
        // ).set_title(
        //     "py_module"
        // )
        // this.code_pre = row1().set_input(text_area().set_style({
        //     height: Constant.TEXT_AREA_HEIGHT_3,
        // }))
        // this.case_select = row1().set_input(
        //     select()
        // ).set_title(
        //     "case"
        // )
        // this.case_pre = row1().set_input(text_area())
        // this.dialog_div = form().set_rows([
        //     this.code_select,
        //     this.code_pre,
        //     this.case_select,
        //     this.case_pre,
        // ]).ok(() => {
        //     this.run()
        // })
    }
    init_node() {
        this.init_edit_dialog()
        this.div = div()
        this.pro = new Progress()

        this.add_childs([
            //div().set_size(1).add_childs([this.div]),
            this.div.set_size(1),
            div().add_childs([
                this.pro,
                button().set_html("setting").on_click(() => this.open_setting()),
            ]).set_height(Constant.DEFAULT_LINE_HEIGHT)
        ])
    }
    init_event2(): void {
        this.code_select.on_change(() => {
            let o = this.code_select.get_value()
            this.code_pre.set_value(o.value)
            this.case_select.set_option(new Node().set_childs(
                o.data.cases.map((v: any, i: number) => {
                    return new Node().set_value(v).set_title('case ' + i).set_key(i)
                })
            ))//select(web_dom.get_param('case', 0))
        })
        this.case_select.on_change(() => {
            let o = this.case_select.get_value()
            this.case_pre.set_value(JSON.stringify(o.value))

        })

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
        return this.case_pre.get_value()
    }
    load() {
        web_dom.post("/app/yly/algo/manage/query", {

        }, (node: Node) => {
            let py_module = web_dom.get_param("py_module")
            if (!py_module) {
                console.error('py_module is null')
            }
            this.code_select.set_option(node)//.select(py_module)
            this.run()

        })

    }
    run() {
        let module_select = this.code_pre.get_value()
        let case_select = this.case_pre.get_value()
        if (!module_select || !case_select) {
            return
        }
        web_dom.post('/app/yly/algo/manage/execute', {
            content: module_select,
            case: case_select
        }, (node: Node) => {
            this.set_option(node)
            this.pro.set_max_value(node.data.record.length)
            this.pro.set_value(
                parseInt(web_dom.get_param("goto"))
            )
        })
    }
    on_mount() {
        //this.test()
        //this.load()
        // this.open_setting()

    }
}
export default function () {
    return new Algo()
}