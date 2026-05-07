import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, Span
} from "../../base/components/export";

export class TaskRow extends Column {
    task_data: any
    name_div: Div
    fun_path_div: Div
    args_div: Div
    run_num_span: Span
    result_div: Div
    edit_btn: Button
    exec_btn: Button
    init_style(): void {
        this.set_style({
            borderBottom: "1px solid #eee",
            width: "100%",
        })
        super.init_style()
    }
    init_node(): void {
        this.name_div = new Div()
        this.fun_path_div = new Div()
        this.args_div = new Div()
        this.run_num_span = new Span()
        this.result_div = new Div()
        this.edit_btn = new Button().set_html("编辑")
        this.exec_btn = new Button().set_html("执行")
        this.add_childs([
            new Row().add_childs([
                this.name_div,
                this.fun_path_div,
                this.args_div,
            ]).set_size(1).set_align_start(),
            new Row().add_childs([
                new Span().set_html("运行次数: "),
                this.run_num_span,
            ]),
            new Row().add_childs([
                this.result_div,
                this.edit_btn,
                this.exec_btn
            ])
        ])
    }
    init_event(): void {
        this.edit_btn.on_click(
            () => this.event_hander[Constant.EVENT_CHANGE](Constant.METHOD_EDIT, null, this.task_data)
        )
        this.exec_btn.on_click(() => {
            web_dom.post("/app/task/exec_task", { name: this.task_data.name }, (data: Node) => {
                this.task_data = data
                this.render_option()
            })
        })
    }
    set_task(data: any): this {
        this.task_data = data
        this.render_option()
        return this
    }
    render_option(): void {
        this.name_div.set_html(this.task_data.name || "")
        this.fun_path_div.set_html(this.task_data.fun_path || "")
        this.args_div.set_html(this.task_data.args || "")
        this.run_num_span.set_html(String(this.task_data.run_num || 0))
        if (this.task_data.result && this.task_data.result.code === Constant.CODE_200) {
            this.name_div.set_style({ color: "#0c0" })
        } else {
            this.name_div.set_style({ color: "#000" })
        }
    }
}