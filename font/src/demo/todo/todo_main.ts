import {
    FlexRow, FlexColumn, Constant, web_dom,
    Button, dialog, Select,
    Span, Input,
    Data, Util,
} from "../../base/components/export";
import { TodoContainer } from "./todo_container";
import { TodoForm } from "./todo_form";
import { TodoData } from "./todo_types";

export class TodoMain extends FlexColumn {
    todo_form: TodoForm
    todo_list: TodoContainer
    search_input: Input
    add_btn: Button
    category_select: Select
    done_select: Select
    score_span: Span
    header: FlexRow
    init_style(): void {
        this.full()
        this.search_input.set_style({ width: 60 })
        this.todo_form.set_style({ minWidth: "300px" })
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
        this.todo_form = new TodoForm()
        this.score_span = new Span()
        this.todo_list = new TodoContainer()
        this.header = new FlexRow().add_children([
            this.score_span,
            this.category_select,
            this.done_select,
            this.search_input,
            this.add_btn
        ])
        this.add_children([
            this.header,
            this.todo_list
        ])
        this.todo_form.set_on_submit((type: string) => {
            let value = this.todo_form.get_value()
            Util.extend(value, {
                category: this.category_select.get_value()
            })
            web_dom.post(`/app/todo/web_${type.toLowerCase()}`, value, () => {
                this.load_todos()
                dialog.close()
            })
        })
    }
    init_event(): void {
        this.search_input.on_change(() => this.todo_list.filter(this.search_input.get_value()))
        this.add_btn.on_click(() => {
            this.todo_form.open(Constant.METHOD_INSERT, {
                category: this.category_select.get_value(),
                done: this.done_select.get_value()
            })
        })
        this.category_select.on_change(() => this.load_todos())
        this.done_select.on_change(() => this.load_todos())
    }
    load_todos(): void {
        let category = this.category_select.get_value()
        let done = this.done_select.get_value() === "true"
        web_dom.post('/app/todo/web_search', { category, done }, (data: any) => {
            this.score_span.set_html(data.title)
            this.todo_list.set_todos(data as any, (method: string, f: any, t: Partial<TodoData>) => {
                this.todo_form.open(method, t)
            })
        })
    }
    render(): void {
        this.done_select.set_option({
            children: [
                { title: "已完成", value: "true" },
                { title: "未完成", value: "false" }
            ],
            id: "todo_done",
        })
        web_dom.post('/app/todo/schema', {}, (v: any) => {
            this.todo_form.set_schema(v.data.top_form)
            v.data.category.id = "todo_category"
            this.category_select.set_option(v.data.category)
            Data.get_user_name(() => {
                this.load_todos()
            })
        })
    }
}

export default function () {
    return new TodoMain()
}
