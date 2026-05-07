import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, FormRow, FormColumn, Search, dialog, Span,
    Data, Util, Container, ListContainer,
} from "../../base/components/export";
import { TaskContainer } from "./task_container";

export class TaskMain extends Row {
    top_form: FormColumn
    task_list: TaskContainer
    search_input: Search
    add_btn: Button
    header: Column
    status_span: Span
    init_style(): void {
        this.full()
        this.search_input.set_style({
            width: 200
        })
        this.top_form.set_style({
            padding: "20px",
            minWidth: "300px"
        })
        this.status_span.set_size(1)
        this.header.set_style({
            justifyContent: "space-between", alignItems: "center", width: 1
        })
        super.init_style()
    }
    init_node(): void {
        this.search_input = new Search()
        this.add_btn = new Button().set_html("新增任务")
        this.top_form = new FormColumn()
        this.status_span = new Span()
        this.task_list = new TaskContainer()
        this.header = new Column().add_childs([
            this.status_span,
            this.search_input,
            this.add_btn
        ])
        this.add_childs([
            this.header,
            this.task_list
        ])
    }
    init_event(): void {
        this.search_input.on_change(() => this.task_list.filter(this.search_input.get_value()))
        this.add_btn.on_click(() => {
            this.on_task_change(Constant.METHOD_INSERT, null, {})
        })
        this.top_form.on_submit(this.submit.bind(this))
    }
    submit(type: string) {
        let value = this.top_form.get_value()
        web_dom.post("/app/task/web_submit", { type, value }, () => {
            this.load_tasks()
            dialog.close()
        })
    }
    load_tasks(): void {
        web_dom.post("/app/task/web_search", {}, (data: Node) => {
            this.status_span.set_html(data.title)
            this.task_list.set_tasks(data, this.on_task_change.bind(this))
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
            Data.get_user_name((user_name: any) => {
                this.load_tasks()
            })
        })
    }
}

export default function () {
    return new TaskMain()
}