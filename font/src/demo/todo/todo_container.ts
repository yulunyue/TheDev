import {
    Div, Constant, Node, web_dom,
    Button, web_socket, Ct, Util
} from "../../base/components/export";
import { TodoRow } from "./todo_row";
import { TodoData, TodoChangeCallback } from "./todo_types";

export class TodoContainer extends Div {
    todo_rows: TodoRow[] = []
    label_empty: Div
    on_refresh: any
    init_style(): void {
        this.set_style({
            flex: "1",
            overflow: "auto",
            width: "100%"
        })
        this.label_empty.set_style({
            textAlign: "center", color: "#999", padding: "40px 0"
        })
        super.init_style()
    }
    init_node(): void {
        this.label_empty = new Div().set_html("暂无待办事项")
    }
    set_todos(data: Node, on_change: TodoChangeCallback): this {
        this.clear()
        this.todo_rows = []
        this.add_child(this.label_empty)
        for (let todo of data.children) {
            this.add_todo_row(todo as any).on_change(on_change)
        }
        this.update_empty()
        return this
    }
    add_todo_row(todo: TodoData): TodoRow {
        let row = new TodoRow().set_todo(todo)
        this.add_child(row)
        this.todo_rows.push(row)
        return row
    }
    update_empty() {
        if (this.todo_rows.length === 0) {
            this.label_empty.show()
        } else {
            this.label_empty.hide()
        }
    }
    filter(key: string) {
        let has_visible = false
        for (var i = 0; i < this.todo_rows.length; i++) {
            var todo = this.todo_rows[i]
            var s = todo.todo_data.title + todo.todo_data.content
            if (Util.str_match(s, key)) {
                todo.show()
                has_visible = true
            } else {
                todo.hide()
            }
        }
        if (has_visible) {
            this.label_empty.hide()
        } else {
            this.label_empty.show()
        }
    }
}
