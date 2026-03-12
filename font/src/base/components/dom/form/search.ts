import { Input } from "./input";
import web_dom from "../../../web/web_dom"
import Ct from "../../../web/constant"
import { Title, Button } from "./button";
import { Node, to_node } from "../../../web/cls";
import { Div } from "../div"
import { ListUi } from "../list";
import Constant from "../../../web/constant"
export class Search extends Div {
    dialog: Div
    listui: ListUi
    input: Input
    init_node(): void {
        this.input = this.add_child(new Input())
        this.dialog = this.add_child(new Div())
        this.listui = this.dialog.add_child(new ListUi())
    }
    init_style(): void {
        this.dialog.set_style({
            zIndex: Constant.Z_INDEX_1
        }).hide()
    }

    init_event(): void {
        this.input.on_click(() => this.emit_search())
        // this.input.on_input(() => this.emit_search())
        this.input.on_input(() => this.listui.filter(this.input.get_value()))
        this.listui.on_change((src: any, dst: any) => this.set_value(dst))
    }
    set_title(s: string) {
        this.input.set_placeholder(s)
        return this
    }
    set_value(value: Node): this {
        super.set_value(value)
        this.input.set_value(value.get_title())
        this.dialog.hide()
        return this
    }
    emit_search() {
        web_dom.post(this.option.url, {
            key: this.input.get_value()
        }, (node: Node) => {
            this.listui.set_option(node)
            this.show_search_dialog()
        })
        return this
    }

    show_search_dialog() {
        // console.log(this.get_rect(), this.el)

        this.dialog.set_style({
            left: this.get_a_x(),
            top: this.get_a_y() + this.get_height(),
            width: this.input.get_width(),
            maxHeight: 300,
            overflowY: "auto",
            border: "1px solid #000",
            backgroundColor: "white",
            position: "fixed"
        }).show()
        web_dom.body_click(() => {
            this.dialog.hide()
        })
    }

    set_btns(btns: any) {
        return this
    }

}
export function search() {
    return new Search()
}
export function search_dev() {
    return search()
}