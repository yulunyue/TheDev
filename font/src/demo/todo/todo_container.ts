import {
    Div, Constant, Node, web_dom,
    Button, web_socket, Ct, Util
} from "../../base/components/export";
import { TodoRow } from "./todo_row";

export class TodoContainer extends Div {
    todo_rows: TodoRow[] = []
    on_refresh: any
    init_style(): void {
        this.set_style({
            flex: "1",
            overflow: "auto",
            width: "100%"
        })
        super.init_style()
    }
    init_node(): void {
    }
    set_todos(data: Node, on_change: any): this {
        this.clear()
        this.todo_rows = []
        for (let todo of data.children) {
            this.add_todo_row(todo).on_change(on_change)
        }
        return this
    }
    add_todo_row(todo: any): TodoRow {
        let row = new TodoRow().set_todo(todo)
        this.add_child(row)
        this.todo_rows.push(row)
        return row
    }
    filter(key: string) {
        for (var i = 0; i < this.todo_rows.length; i++) {
            var todo = this.todo_rows[i]
            var s = todo.todo_data.title + todo.todo_data.content
            if (Util.str_match(s, key)) {
                todo.show()
            } else {
                todo.hide()
            }

        }
    }
}