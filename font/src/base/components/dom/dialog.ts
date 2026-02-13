import { Div, div } from "./div";
import web_dom from "../../web/web_dom"

import { Node } from "../../web/cls";
export class Dialog extends Div {
    container: Div
    header: Div
    main: Div
    init_node() {
        web_dom.get_body().appendChild(this.el)
        this.main = this.add_child(div())
        this.header = this.add_child(div())
        this.container = this.main.add_child(div())
    }

    init_style(): void {
        this.set_style_ab_full().set_style({
            zIndex: "100",
            backgroundColor: "#8888"

        })
        this.main.set_style_center_by_position().set_style({
            backgroundColor: "#fff",
        })
        this.hide()
    }
    init_event(): void {

    }
    open_form(oj: any, call: any) {
        // let rows = []
        // for (var key in oj) {
        //     rows.push(
        //         row1().set_option(new Node().set_type(
        //             oj[key]
        //         ).set_title(
        //             key
        //         ).set_key(key))
        //     )
        // }
        // return this.open(form().set_rows(rows).ok(call))
    }
    open(c: any) {
        this.container.clear().add_child(c)
        c._dialog = this
        this.show()
        web_dom.bind_click(this.el, () => {
            this.hide()
        })
        web_dom.bind_click(this.container.el, () => {
        })
        return this
    }
}
class Dig {
    dig: Dialog
    get_dialog() {
        if (!this.dig) {
            this.dig = new Dialog()
        }
        return this.dig
    }
    open_form(oj: any, call: any) {
        return this.get_dialog().open_form(oj, call)
    }
    open(c: any) {
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
    open_progress_bar(s: any) {

    }
}
export default new Dig()