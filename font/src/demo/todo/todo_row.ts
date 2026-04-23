import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, Label, web_socket, Ct, Span, Checkbox
} from "../../base/components/export";

export class TodoRow extends Column {
    todo_data: any
    on_update: any
    on_delete: any
    title_div: Div
    content_div: Div
    category_span: Span
    priority_span: Span
    done_checkbox: Checkbox
    del_btn: Button
    init_style(): void {
        this.set_style({
            padding: "0 12px",
            borderBottom: "1px solid #eee",
            width: "100%",
            height: "24px",
            flexDirection: "row",
            alignItems: "center"
        })
        this.done_checkbox.set_style({
            width: "16px",
            height: "16px"
        })
        this.title_div.set_style({
            fontSize: "14px",
            fontWeight: "bold",
            flex: "1",
            marginLeft: "8px",
            lineHeight: "24px",
            overflow: "hidden"
        })
        this.content_div.set_style({
            fontSize: "12px",
            color: "#666",
            flex: "2",
            lineHeight: "24px",
            overflow: "hidden"
        })
        this.category_span.set_style({
            padding: "2px 8px",
            borderRadius: "4px",
            fontSize: "10px",
            lineHeight: "20px"
        })
        this.priority_span.set_style({
            marginLeft: "4px",
            fontSize: "10px",
            color: "#888",
            lineHeight: "24px"
        })
        this.del_btn.set_style({
            marginLeft: "4px",
            padding: "2px 8px",
            borderRadius: "4px",
            backgroundColor: "#f44",
            fontSize: "12px",
            height: "20px",
            lineHeight: "20px"
        })
        super.init_style()
    }
    init_node(): void {
        this.done_checkbox = new Checkbox()
        this.title_div = new Div()
        this.content_div = new Div()
        this.category_span = new Span()
        this.priority_span = new Span()
        this.del_btn = new Button().set_html("Del")
        this.add_childs([
            this.done_checkbox,
            this.title_div,
            this.content_div,
            this.category_span,
            this.priority_span,
            this.del_btn
        ])
    }
    init_event(): void {
        this.done_checkbox.on_change(() => this.toggle_done())
        this.del_btn.on_click(() => this.on_delete?.(this.todo_data))
    }
    set_todo(data: any): this {
        this.todo_data = data
        this.render_option()
        return this
    }
    render_option(): void {
        let category_colors = {
            study: "#4a90d9",
            entertainment: "#e67e22"
        }
        this.title_div.set_html(this.todo_data.title || "")
        this.content_div.set_html(this.todo_data.content || "")
        this.category_span.set_html(this.todo_data.category || "study").set_style({
            backgroundColor: category_colors[this.todo_data.category] || "#ccc"
        })
        this.priority_span.set_html("P:" + (this.todo_data.priority || 0))
        this.done_checkbox.set_value(this.todo_data.done)
        if (this.todo_data.done) {
            this.title_div.set_style({ color: "#0c0" })
        } else {
            this.title_div.set_style({ color: "#000" })
        }
    }
    toggle_done(): void {
        web_dom.post("/app/todo/web_submit", {
            type: "submit",
            value: { ...this.todo_data, done: !this.todo_data.done }
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