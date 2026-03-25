import { Div } from "./div";
import web_dom from "../../web/web_dom"

import { Node } from "../../web/cls";
import { Row, Container } from "../export";

export class Dialog extends Row {
    header: Div
    main: Div
    init_node() {
        this.header = this.add_child(new Div())
        this.main = this.add_child(new Div())
    }
    init_style(): void {
        this.set_style_ab_full().set_style({
            zIndex: "100",
            backgroundColor: "#8888",
            left: 0,
            top: 0,
        })
        this.main.set_style_center_by_position().set_style({
            backgroundColor: "#fff",
        })

    }
    init_event(): void {
        this.on_click(this.hide.bind(this))
        this.main.on_click(() => { })
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