import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, FormRow, Search, web_socket, Ct, dialog, Select,
    Span, Input,
    Data
} from "../../base/components/export";
import { TodoContainer } from "./todo_container";

export class TodoMain extends Row {
    top_form: FormRow
    todo_list: TodoContainer
    search_input: Input
    user_search: Search
    add_btn: Button
    category_select: Select
    done_select: Select
    score_span: Span
    header: Column
    init_style(): void {
        this.full()
        this.search_input.set_style({
            width: 60
        })
        this.top_form.set_style({
            padding: "20px",
            minWidth: "300px"
        })
        this.score_span.set_size(1)
        this.category_select.set_style({ margin: "4px" })
        this.done_select.set_style({ margin: "4px" })
        this.header.set_style({
            justifyContent: "space-between", alignItems: "center", width: 1
        })
        super.init_style()
    }
    init_node(): void {
        this.search_input = new Input()
        this.add_btn = new Button().set_html("新增")
        this.category_select = new Select()
        this.done_select = new Select()
        this.top_form = new FormRow()
        this.score_span = new Span()
        this.todo_list = new TodoContainer()
        this.header = new Column().add_childs([
            this.score_span,
            this.category_select,
            this.done_select,
            this.search_input,
            this.add_btn
        ])
        this.add_childs([
            this.header,
            this.todo_list
        ])
    }
    init_event(): void {
        this.search_input.on_change(() => this.todo_list.filter(this.search_input.get_value()))
        this.add_btn.on_click(() => {
            this.on_to_do_change(Constant.METHOD_INSERT, null, {
                category: this.category_select.get_value(),
                done: this.done_select.get_value()
            })
        })
        this.top_form.on_submit((type: string, value: any) => {
            this.load_todos()
            dialog.close()
        })
        this.category_select.on_change(() => this.load_todos())
        this.done_select.on_change(() => this.load_todos())
    }
    load_todos(): void {
        let category = this.category_select.get_value()
        let done = this.done_select.get_value() === "true"
        web_dom.post("/app/todo/web_search", { category: category, done: done }, (data: Node) => {
            this.score_span.set_html("分数: " + data.value)
            this.todo_list.set_todos(data, this.on_to_do_change.bind(this))
        })
    }
    on_to_do_change(method: string, f: any, t: any) {
        if (method == Constant.METHOD_INSERT) {
            this.top_form.set_btns({ [Constant.METHOD_INSERT]: "提交" })
            this.top_form.child_map.title.show()
            this.top_form.child_map.user_id.show()
        } else {
            this.top_form.child_map.title.hide()
            this.top_form.child_map.user_id.hide()
            this.top_form.set_btns({ [Constant.METHOD_EDIT]: "保存", [Constant.METHOD_DELETE]: "删除" })
        }
        this.top_form.set_value(t)
        dialog.open(this.top_form)
    }
    render(): void {
        this.top_form.set_option({
            url: "/app/todo",
        })
        this.category_select.set_option({
            url: "/app/todo/category",
            value: "study"
        })
        this.done_select.set_option({
            childs: [
                { title: "已完成", value: "true" },
                { title: "未完成", value: "false" }
            ],
            value: "false"
        })

        Data.get_user_name((user_name: any) => {
            this.load_todos()
        })
    }
}

export default function () {
    return new TodoMain()
}