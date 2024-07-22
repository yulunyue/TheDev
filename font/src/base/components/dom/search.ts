import { Input } from "./input";
import web from "../../web/web_dom"
import Ct from "../../web/constant"
import { Node } from "../../web/cls";
import { listui } from "./list";
export class Search extends Input {
    set_search(url: string) {
        web.bind_click(this.el, () => this.emit_search(url))
        web.bind_input(this.el, () => this.emit_search(url))
        return this
    }
    emit_search(url: string) {
        web.post(url, { value: this.get_value() }, (node: Node) => {
            this.set_option(node)
            this.show_search_dialog()
        })
    }
    set_option(node: Node) {
        return super.set_option(node)
    }
    show_search_dialog() {
        console.log(this.get_rect(), this.el)
        this.get_dialog().set_style({
            left: this.get_a_x(),
            top: this.get_a_y() + this.get_height(),
            width: this.get_width(),
            maxHeight: 300,
            overflowY: "auto",
            border: "1px solid #000",
            backgroundColor: "white",
        }).clear().add_child(
            listui().set_option(
                this.option.filter(this.get_value())
            ).select((v) => {
                this.set_value(v.title)
                this.get_dialog().hide()
            })
        ).show()
        web.body_click(() => {
            this.get_dialog().hide()
        })
    }

}
export function search() {
    return new Search()
}
export function search_dev() {
    return search().set_search(Ct.MOCK_KEY)
}