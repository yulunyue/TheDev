import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, web_socket, Ct, Label, Span
} from "../../base/components/export";
import { TodoRow } from "./todo_row";

export class TodoContainer extends Div {
    todo_rows: TodoRow[] = []
    on_refresh: any
    all_data: any
    init_style(): void {
        this.set_style({
            flex: "1",
            overflow: "auto",
            padding: "8px"
        })
        super.init_style()
    }
    init_node(): void {
    }
    set_current_tab(idx: number): void {
        this.render_tab(idx)
    }
    render_tab(idx: number): void {
        this.clear()
        this.todo_rows = []
        if (!this.all_data || !this.all_data.childs[idx]) return
        let childs = this.all_data.childs[idx].childs
        for (let child of childs) {
            this.add_todo_row(child.value)
        }
    }
    set_stats(data: Node, current_tab: number = 0): this {
        this.all_data = data
        this.render_tab(current_tab)
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