import {
    FlexRow, FlexColumn, Div, Constant, Node, web_dom,
    Button, FormRow, FormColumn, Search, dialog, Span, Pre,
    Data, Container, web_socket, Ct,
} from "../../base/components/export";

export class TaskMain extends FlexColumn {
    top_form: FormRow
    search_input: Search
    add_btn: Button
    header: FlexRow
    status_span: Span
    result_div: Pre
    exec_btn: Button
    edit_btn: Button
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
        this.add_btn = new Button().set_html("新增")
        this.exec_btn = new Button().set_html("执行")
        this.edit_btn = new Button().set_html("编辑")
        this.top_form = new FormRow()
        this.status_span = new Span()
        this.result_div = new Pre()
        this.header = new FlexRow().add_children([
            this.search_input,
            this.edit_btn,
            this.exec_btn,
            this.status_span,
            this.add_btn,

        ])
        this.add_children([
            this.header,
            this.result_div
        ])
    }
    init_event(): void {
        this.search_input.on_change(() => this.load_task())
        this.add_btn.on_click(() => {
            this.on_task_change(Constant.METHOD_INSERT, null, {})
        })
        this.edit_btn.on_click(() => this.post("get_font"))
        this.exec_btn.on_click(() => this.post("exec_task"))
        this.top_form.on_submit(this.submit.bind(this))
    }
    post(method: string) {
        let name = this.search_input.get_value()
        if (!name) {
            return
        }
        web_dom.post("/app/task/" + method, { key: name }, (data: Node) => {
            if (method.includes("get")) {
                this.on_task_change(Constant.METHOD_EDIT, null, data.value)
            }
            this.view_task(name)
        })
    }
    view_task(name: string) {
        web_dom.post("/app/task/view", { key: name }, (data: Node) => {
            this.on_task_update(data)
        })
    }
    on_task_update(data: any) {
        this.result_div.set_html(JSON.stringify(data, null, 2))
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
        web_dom.post(`/app/task/web_${type.toLowerCase()}`, value, () => {
            this.load_task()
            dialog.close()
        })
    }
    load_task(): void {
        let name = this.search_input.get_value()
        if (this.current_task && this.current_task !== name) {
            this.unsubscribe_task(this.current_task)
        }

        if (!name) {
            this.result_div.set_html("")
            this.status_span.set_html("")
            this.current_task = ""
            return
        }
        this.view_task(name)
        this.current_task = name
        this.subscribe_task(name)

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
        this.search_input.set_option({
            url: "/app/task/web_search",
            id: "task_search",
            title: "任务名称"
        })
        web_dom.post("/app/task/schema", {}, (v: Node) => {
            this.top_form.set_option(v.data.top_form)
        })
        Data.get_user_name((user_name: any) => {
        })
    }
}

export default function () {
    return new TaskMain()
}