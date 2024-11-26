
import {
    Div, Svg, svg, Constant, Node, web_dom, tree, Form, form, dialog, Row, node, Select, select, Pre, pre,
    line, gnode, GNode, button, progress, div, input, Input, Progress, DivFactory, row1, row2,
    text_area, TextArea
} from "../base/components/export";


class Algo extends Div {
    div: Div
    pro: Progress
    algo_nodes: Div[]
    dialog_div: Form
    code_select: Row
    code_pre: Row
    case_select: Row
    case_pre: Row
    init_style(): void {
        this.set_style_ab_full()
    }
    init_node() {
        this.div = div()
        this.code_select = row1().set_input(
            select()
        ).set_title(
            "模块名"
        )
        this.code_pre = row1().set_input(text_area().set_style({
            height: Constant.TEXT_AREA_HEIGHT_3,
        }))
        this.case_select = row1().set_input(
            select()
        ).set_title(
            "样例"
        )
        this.case_pre = row1().set_input(text_area())
        this.dialog_div = form().set_rows([
            this.code_select,
            this.code_pre,
            this.case_select,
            this.case_pre,
        ]).ok(() => {
            this.run()
        })
        this.pro = progress().set_size(1).change(() => this.goto())
        this.add_childs([
            this.div.set_size(1),
            div().add_childs([
                this.pro,
                button().set_html("setting").click(() => this.open_setting()),
            ]).set_height(Constant.DEFAULT_LINE_HEIGHT)
        ]).flex_horizontal_layout()
    }
    init_event(): void {
        this.code_select.change(() => {
            let o = this.code_select.get_value()
            this.code_pre.set_value(o.value)
            this.case_select.set_option(new Node().set_childs(
                o.data.cases.map((v: any, i: number) => {
                    return new Node().set_value(v).set_title('case ' + i).set_key(i)
                })
            )).select(web_dom.get_param('case', 0))
        })
        this.case_select.change(() => {
            let o = this.case_select.get_value()
            this.case_pre.set_value(JSON.stringify(o.value))

        })

    }
    open_setting() {
        dialog.open(this.dialog_div)
    }
    set_option(option: Node): this {
        this.option = option
        this.draw_nodes()
        return this
    }
    draw_nodes() {
        this.algo_nodes = this.div.clear().add_grid_childs(
            this.option.childs,
            web_dom.get_wh_scale()<1?Constant.HORIZONTAL:Constant.VERTICAL
        ).emit_mount().get_content_divs()
    }
    goto() {
        let idx = this.pro.get_value()
        if (!this.option.data.records || !this.option.data.records[idx]) {
            return
        }
        for (var key in this.option.data.records[idx]) {
            DivFactory.get(key).set_option(this.option.data.records[idx][key])
        }
    }
    test() {
        this.set_option(new Node().set_childs([Constant.MOCK_NODE_3_3.set_type("tree")]))
    }

    get_case() {
        return this.case_pre.get_value()
    }
    load() {
        web_dom.post("/app/yly/algo/manage/query", {}, (node: Node) => {
            this.code_select.set_option(node).select(web_dom.get_param("py_module"))
            this.run()
        })

    }
    run() {
        let module_select = this.code_pre.get_value()
        let case_select = this.case_pre.get_value()

        web_dom.post('/app/yly/algo/manage/execute', {
            content: module_select,
            case: case_select
        }, (node: Node) => {
            this.set_option(node)
            this.pro.set_max_value(node.data.records.length)
        })
    }
    on_mount() {
        //this.test()
        this.load()
        //this.open_setting()

    }
}
export default function () {
    return new Algo()
}