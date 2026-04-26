import {
    Column, Row, Div, Constant, Node, web_dom,
    Button, Label, web_socket, Ct, Span
} from "../../base/components/export";

export class TodoRow extends Column {
    todo_data: any
    title_div: Div
    content_div: Div
    edit_btn: Button
    user_name: Div
    create_time: Div
    update_time: Div
    init_style(): void {
        this.set_style({
            // padding: "0 12px",
            borderBottom: "1px solid #eee",
            width: "100%",
        })
        super.init_style()
    }
    init_node(): void {
        this.title_div = new Div()
        this.content_div = new Div()
        this.create_time = new Div()
        this.update_time = new Div()
        this.user_name = new Div()
        this.edit_btn = new Button().set_html("修改")
        this.add_childs([
            new Row().add_childs([
                this.title_div,
                this.content_div,
            ]).set_size(1).set_align_left(),
            new Row().add_childs([
                this.create_time,
                this.update_time,
            ]),
            new Row().add_childs([
                this.user_name,
                this.edit_btn
            ])


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
        this.user_name.set_html(this.todo_data.user_id || "")
        this.content_div.set_html(this.todo_data.content || "")
        this.create_time.set_html("开始: " + this.todo_data.create_time.slice(5, 16))
        this.update_time.set_html("完成: " + this.todo_data.update_time.slice(5, 16))
        if (this.todo_data.done) {
            this.title_div.set_style({ color: "#0c0" })
        } else {
            this.title_div.set_style({ color: "#000" })
        }
    }
}