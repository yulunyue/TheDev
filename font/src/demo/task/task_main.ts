import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, FormRow, FormColumn, Search, dialog, Span, Pre,
    Data, Container, web_socket, Ct,
} from "../../base/components/export";

export class TaskMain extends Row {
    top_form: FormColumn
    search_input: Search
    add_btn: Button
    header: Column
    status_span: Span
    result_div: Pre
    exec_btn: Button
    current_task: string = ""
    init_style(): void {
        this.full()
        this.set_style({
            height: "100vh",
            overflow: "hidden"
        })
        this.search_input.set_style({
            width: 200,
            minWidth: 200
        })
        this.top_form.set_style({
            padding: "20px",
            minWidth: "300px"
        })
        this.status_span.set_size(1)
        this.header.set_style({
            justifyContent: "flex-start",
            alignItems: "center",
            width: 1,
            flex: "none"
        })
        this.result_div.set_style({
            flex: 1,
            overflow: "auto"
        })
        super.init_style()
    }
    init_node(): void {
        this.search_input = new Search()
        this.add_btn = new Button().set_html("新增任务")
        this.exec_btn = new Button().set_html("执行")
        this.top_form = new FormColumn()
        this.status_span = new Span()
        this.result_div = new Pre()
        this.header = new Column().add_childs([
            this.search_input,
            this.status_span,
            this.add_btn,
            this.exec_btn
        ])
        this.add_childs([
            this.header,
            this.result_div
        ])
    }
    init_event(): void {
        this.search_input.on_change(() => this.load_task())
        this.add_btn.on_click(() => {
            this.on_task_change(Constant.METHOD_INSERT, null, {})
        })
        this.exec_btn.on_click(() => {
            let name = this.search_input.get_value()
            if (name) {
                web_dom.post("/app/task/exec_task", { name }, (data: any) => {
                    this.result_div.set_html(JSON.stringify(data, null, 2))
                })
            }
        })
        this.top_form.on_submit(this.submit.bind(this))
    }
    on_task_update(data: any) {
        this.result_div.set_html(JSON.stringify(data, null, 2))
        let stateText = data.state === "doing" ? "(执行中)" : "(已完成)"
        this.status_span.set_html(`任务: ${data.name || this.search_input.get_value()} ${stateText}`)
    }
    subscribe_task(name: string) {
        web_socket.sub(`${Constant.TOPIC_TASK_UPDATE_MSG}.${name}`, (data: any) => {
            this.on_task_update(data)
        })
    }
    unsubscribe_task(name: string) {
        web_socket.un_sub(`${Constant.TOPIC_TASK_UPDATE_MSG}.${name}`)
    }
    submit(type: string) {
        let value = this.top_form.get_value()
        web_dom.post("/app/task/web_submit", { type, value }, () => {
            this.load_task()
            dialog.close()
        })
    }
    load_task(): void {
        let name = this.search_input.get_value()
        if (!name) {
            this.result_div.set_html("")
            this.status_span.set_html("")
            return
        }
        web_dom.post("/app/task/get", { key: name }, (data: Node) => {
            this.status_span.set_html(`任务: ${name}`)
            this.result_div.set_html(JSON.stringify(data, null, 2))
        })
    }
    on_task_change(method: string, f: any, t: any) {
        if (method == Constant.METHOD_INSERT) {
            this.top_form.set_btns({ [Constant.METHOD_INSERT]: "提交" })
        } else {
            this.top_form.set_btns({
                [Constant.METHOD_EDIT]: "保存",
                [Constant.METHOD_DELETE]: "删除"
            })
        }
        this.top_form.set_value(t)
        dialog.open(this.top_form)
    }
    render(): void {
        web_dom.post("/app/task/schema", {}, (v: Node) => {
            this.top_form.set_option(v.data.top_form)
            this.search_input.set_option({
                url: "/app/task/web_search",
                id: "task_search",
                title: "任务名称"
            })
            Data.get_user_name((user_name: any) => {
            })
        })
    }
}

export default function () {
    return new TaskMain()
}