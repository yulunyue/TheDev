import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, web_socket, Ct
} from "../../base/components/export";
import { TodoRow } from "./todo_row";

export class TodoContainer extends Div {
    todo_rows: TodoRow[] = []
    on_refresh: any
    init_style(): void {
        this.set_style({
            flex: "1",
            overflow: "auto",
            margin: "8px",
            width: "100%"
        })
        super.init_style()
    }
    init_node(): void {
    }
    set_todos(data: Node, on_change: any): this {
        this.clear()
        this.todo_rows = []
        for (let todo of data.childs) {
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

}