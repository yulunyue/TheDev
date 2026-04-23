import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, FormRow, FormColumn, Search, web_socket, Ct
} from "../../base/components/export";
import { TodoContainer } from "./todo_container";

export class TodoMain extends Column {
    top_form: FormColumn
    todo_list: TodoContainer
    search_input: Search
    add_btn: Button
    form_visible: boolean = false
    form_wrapper: Div
    init_style(): void {
        this.full()
        super.init_style()
    }
    init_node(): void {
        this.search_input = new Search().set_option({
            url: "/app/todo/web_search",
            title: "Search Todo"
        })
        this.add_btn = new Button().set_html("+ Add")
        this.top_form = new FormColumn().set_option({
            url: "/app/todo",
            data: { btns: { submit: "Add" } }
        })
        this.form_wrapper = new Div().add_child(this.top_form).set_style({
            padding: "12px",
            borderBottom: "1px solid #ddd",
            display: "none"
        })
        this.todo_list = new TodoContainer().set_on_refresh(this.load_todos.bind(this))
        let header = new Column().add_childs([
            new Row().add_childs([
                this.search_input.set_style({ flex: "1" }),
                this.add_btn.set_style({ marginLeft: "8px" })
            ]).set_style({ padding: "12px" }),
            this.form_wrapper
        ]).set_style({ backgroundColor: "#f5f5f5" })
        this.add_childs([
            header,
            this.todo_list
        ])
    }
    init_event(): void {
        this.search_input.on_change((key: string, src: Node, dst: Node) => {
            this.load_todos()
        })
        this.add_btn.on_click(() => {
            this.form_visible = !this.form_visible
            this.form_wrapper.set_style({ display: this.form_visible ? "" : "none" })
            if (this.form_visible) {
                this.top_form.set_value({})
            }
        })
        this.top_form.on_submit((type: string, value: any) => {
            this.load_todos()
            this.top_form.set_value({})
            this.form_visible = false
            this.form_wrapper.set_style({ display: "none" })
        })
    }
    load_todos(): void {
        web_dom.post("/app/todo/web_search", { key: "", name: "" }, (data: Node) => {
            this.todo_list.set_todos(data.childs.map(c => c.value))
        })
    }
    render(): void {
        this.top_form.set_option({ url: "/app/todo" })
        this.load_todos()
    }
}

export default function () {
    return new TodoMain()
}