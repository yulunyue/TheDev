import { Div } from "./div";
import web_dom from "../../web/web_dom"

import { Node } from "../../web/cls";
import { Row, Container, Span, Button, Column } from "../export";

export class Dialog extends Div {
    header: Column
    title_span: Span
    close_btn: Button
    body: Row
    main: Div
    init_node() {
        this.header = this.add_child(new Column())
        this.title_span = new Span().set_html("title")
        this.close_btn = new Button().set_html("✕")
        this.header.add_childs([
            this.title_span, this.close_btn
        ])
        this.main = new Div()
        this.body = new Row().add_childs([
            this.header,
            this.main,
        ])
        this.add_childs([
            this.body,
        ])
    }
    init_style(): void {
        this.set_style_ab_full().set_style({
            zIndex: "100",
            backgroundColor: "#8888",
            left: 0,
            top: 0,
        })
        this.header.set_style({
            display: "flex",
            flexDirection: "row",
            justifyContent: "space-between",
            alignItems: "center",
            flex: "none",
            backgroundColor: "#f5f5f5",
            borderBottom: "1px solid #ddd",
        })
        this.close_btn.set_style({
            cursor: "pointer",
            border: "none",
            background: "none",
            fontSize: "18px",
            fontWeight: "bold",
            lineHeight: 1,
            padding: "0 8px",
        })
        this.body.set_style_center_by_position().set_style({
            backgroundColor: "#fff",
        })

    }
    init_event(): void {
        this.header.on_click(() => { })
        this.main.on_click(() => { })
        this.close_btn.on_click(() => this.hide())
    }
    set_title(title: string) {
        this.title_span.set_html(title)
        return this
    }
    open(o: Div) {
        this.main.clear().add_child(o)
        this.show()
        return this
    }
    render(): void {
        console.log("xx")
        this.hide()
    }
}
class Dig {
    dig: Dialog
    get_dialog() {
        if (!this.dig) {
            this.dig = new Dialog().mount(web_dom.get_body())
        }
        return this.dig
    }
    open(c: Div) {
        return this.get_dialog().open(c)
    }
    open_loading() {
        return this.open(new Div().set_class("load_gif").set_style({
            width: 32,
            height: 32,
            backgroundSize: "cover",
            backgroundColor: "#8888"

        }))
    }
    close() {
        return this.get_dialog().hide()
    }
    alart(s: string) {
        alert(s)
    }
    open_progress_bar(s: any) {

    }
}
export default new Dig()
