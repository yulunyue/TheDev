import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, FormRow, Search, web_socket, Ct, dialog, Span,
    Select
} from "../../base/components/export";
import { TodoContainer } from "./todo_container";

export class TodoMain extends Row {
    top_form: FormRow
    todo_list: TodoContainer
    search_input: Search
    add_btn: Button
    score_span: Span
    category_select: Select
    done_select: Select
    header: Column
    init_style(): void {
        this.full()
        this.score_span.set_style({
            fontSize: "20px",
            fontWeight: "bold",
            color: "#333"
        }).set_size(1)
        this.search_input.set_style({ flex: "1" })
        this.top_form.set_style({
            padding: "20px",
            minWidth: "300px"
        })
        this.category_select.set_style({ margin: "4px" })
        this.done_select.set_style({ margin: "4px" })
        this.header.set_style({ padding: "12px", justifyContent: "space-between", alignItems: "center" })
        super.init_style()
    }
    init_node(): void {
        this.score_span = new Span()
        this.search_input = new Search()
        this.add_btn = new Button().set_html("+ Add")
        this.top_form = new FormRow()
        this.category_select = new Select()
        this.done_select = new Select()
        this.todo_list = new TodoContainer().set_on_refresh(this.load_todos.bind(this))
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
        this.search_input.on_change(() => this.load_todos())
        this.add_btn.on_click(() => {
            this.top_form.set_value({})
            dialog.open(this.top_form)
        })
        this.top_form.on_submit((type: string, value: any) => {
            this.load_todos()
            this.top_form.set_value({})
            dialog.close()
        })
        this.category_select.on_change(() => this.load_todos())
        this.done_select.on_change(() => this.load_todos())
    }
    load_todos(): void {
        let category = this.category_select.get_value()
        let done = this.done_select.get_value() === "true"
        web_dom.post("/app/todo/get_stats", {}, (data: Node) => {
            this.score_span.set_html("总分: " + data.value)
            let idx = this.get_tab_index(category, done)
            this.todo_list.set_stats(data, idx)
        })
    }
    get_tab_index(category: string, done: boolean): number {
        if (category === "study" && done) return 0
        if (category === "study" && !done) return 1
        if (category === "entertainment" && done) return 2
        if (category === "entertainment" && !done) return 3
        return 0
    }
    render(): void {
        this.search_input.set_option({
            url: "/app/todo/web_search",
            title: "Search Todo"
        })
        this.top_form.set_option({
            url: "/app/todo",
            data: { btns: { submit: "Add" } }
        })
        this.category_select.set_option({
            childs: [
                { title: "学习", value: "study" },
                { title: "娱乐", value: "entertainment" }
            ],
            value: "study"
        })
        this.done_select.set_option({
            childs: [
                { title: "未完成", value: "false" },
                { title: "已完成", value: "true" }
            ],
            value: "false"
        })
        this.load_todos()
    }
}

export default function () {
    return new TodoMain()
}