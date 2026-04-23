import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, web_socket, Ct
} from "../../base/components/export";
import { TodoRow } from "./todo_row";

export class TodoContainer extends Column {
    todo_rows: TodoRow[] = []
    on_refresh: any
    init_style(): void {
        this.set_style({
            flex: "1",
            overflow: "auto"
        })
    }
    set_todos(todos: any[]): this {
        this.clear_rows()
        for (let todo of todos) {
            this.add_todo_row(todo)
        }
        return this
    }
    add_todo_row(todo: any): TodoRow {
        let row = new TodoRow()
            .set_todo(todo)
            .set_on_update(this.handle_update.bind(this))
            .set_on_delete(this.handle_delete.bind(this))
        this.add_child(row)
        this.todo_rows.push(row)
        return row
    }
    clear_rows(): void {
        this.clear()
        this.todo_rows = []
    }
    handle_update(todo: any): void {
        this.refresh()
    }
    handle_delete(todo: any): void {
        web_dom.post("/app/todo/web_submit", {
            type: "delete",
            value: { _id: todo._id }
        }, () => {
            this.refresh()
        })
    }
    refresh(): void {
        this.on_refresh?.()
    }
    set_on_refresh(call: any): this {
        this.on_refresh = call
        return this
    }
}