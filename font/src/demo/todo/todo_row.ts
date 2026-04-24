import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, Label, web_socket, Ct, Span
} from "../../base/components/export";

export class TodoRow extends Column {
    todo_data: any
    title_div: Div
    content_div: Div
    edit_btn: Button
    create_time: Div
    update_time: Div
    init_style(): void {
        this.set_style({
            // padding: "0 12px",
            borderBottom: "1px solid #eee",
            width: "100%",
        })
        this.title_div.set_style({
            fontSize: "14px",
            fontWeight: "bold",
            flex: "1",
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
        super.init_style()
    }
    init_node(): void {
        this.title_div = new Div()
        this.content_div = new Div()
        this.create_time = new Div()
        this.update_time = new Div()
        this.edit_btn = new Button().set_html("修改")
        this.add_childs([
            this.title_div,
            this.content_div,
            // this.create_time,
            this.update_time,
            this.edit_btn,

        ])
    }
    init_event(): void {
        this.edit_btn.on_click(
            () => this.event_hander[Constant.EVENT_CHANGE](Constant.METHOD_EDIT, null, this.todo_data)
        )

    }
    set_todo(data: any): this {
        this.todo_data = data
        this.render_option()
        return this
    }
    render_option(): void {
        this.title_div.set_html(this.todo_data.title || "")
        this.content_div.set_html(this.todo_data.content || "")
        this.create_time.set_html(this.todo_data.create_time)
        this.update_time.set_html(this.todo_data.update_time)
        if (this.todo_data.done) {
            this.title_div.set_style({ color: "#0c0" })
        } else {
            this.title_div.set_style({ color: "#000" })
        }
    }
}