import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, Label, web_socket, Ct, Span
} from "../../base/components/export";

export class TodoRow extends Column {
    todo_data: any
    on_update: any
    on_delete: any
    init_style(): void {
        this.set_style({
            padding: "12px",
            borderBottom: "1px solid #eee",
            width: "100%"
        })
    }
    set_todo(data: any): this {
        this.todo_data = data
        this.render_todo()
        return this
    }
    render_todo(): void {
        this.clear()
        let status_colors = {
            pending: "#ccc",
            doing: "#f90",
            done: "#0c0",
            closed: "#999"
        }
        let title_div = new Div().set_html(this.todo_data.title || "").set_style({
            fontSize: "16px",
            fontWeight: "bold",
            marginBottom: "4px"
        })
        let content_div = new Div().set_html(this.todo_data.content || "").set_style({
            fontSize: "14px",
            color: "#666",
            marginBottom: "8px"
        })
        let status_span = new Span().set_html(this.todo_data.status || "pending").set_style({
            padding: "4px 12px",
            borderRadius: "12px",
            backgroundColor: status_colors[this.todo_data.status] || "#ccc",
            fontSize: "12px"
        })
        let priority_span = new Span().set_html("P:" + (this.todo_data.priority || 0)).set_style({
            marginLeft: "8px",
            fontSize: "12px",
            color: "#888"
        })
        let done_btn = new Button().set_html("Done").on_click(() => this.update_status("done")).set_style({
            marginRight: "8px",
            padding: "8px 16px",
            borderRadius: "8px"
        })
        let del_btn = new Button().set_html("Del").on_click(() => this.on_delete?.(this.todo_data)).set_style({
            padding: "8px 16px",
            borderRadius: "8px",
            backgroundColor: "#f44"
        })
        let btn_row = new Row().add_childs([
            done_btn,
            del_btn
        ]).set_style({
            marginTop: "8px"
        })
        let info_row = new Row().add_childs([
            status_span,
            priority_span
        ]).set_style({
            alignItems: "center"
        })
        this.add_childs([
            title_div,
            content_div,
            info_row,
            btn_row
        ])
    }
    update_status(status: string): void {
        web_dom.post("/app/todo/web_submit", {
            type: "submit",
            value: { ...this.todo_data, status: status }
        }, (data: Node) => {
            this.on_update?.(data.value)
        })
    }
    set_on_update(call: any): this {
        this.on_update = call
        return this
    }
    set_on_delete(call: any): this {
        this.on_delete = call
        return this
    }
}