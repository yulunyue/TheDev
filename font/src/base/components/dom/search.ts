import { Input } from "./input";
import web from "../../web/web_dom"
import Ct from "../../web/constant"
import { Node, to_node } from "../../web/cls";
import { listui } from "./list";
import { Div } from "./div"
import { ListUi } from "./list";
export class Search extends Input {
    dialog: Div
    listui: ListUi
    init_node(): void {
        this.dialog = new Div().mount(this.div_el)
        this.listui = this.dialog.add_child(new ListUi())
    }
    set_search(url: string) {
        web.bind_click(this.el, () => this.emit_search(url))
        web.bind_input(this.el, () => this.filter())
        return this
    }
    emit_search(url: string) {
        web.post(url, { value: this.get_value() }, (node: Node) => {
            this.set_option(node)
            this.show_search_dialog()
        })
    }
    filter() {
        listui().set_option(
            to_node(this.option).filter(this.get_value())
        ).select((v: any) => {
            this.set_value(v.title)
            this.dialog.hide()
        })
    }
    render_option(): void {
        if (this.option.data.uri) {
            this.set_search(this.option.data.uri)
        }
    }
    show_search_dialog() {
        // console.log(this.get_rect(), this.el)
        this.dialog.set_style({
            left: this.get_a_x(),
            top: this.get_a_y() + this.get_height(),
            width: this.get_width(),
            maxHeight: 300,
            overflowY: "auto",
            border: "1px solid #000",
            backgroundColor: "white",
        }).show()
        web.body_click(() => {
            this.dialog.hide()
        })
    }

}
export function search() {
    return new Search()
}
export function search_dev() {
    return search().set_search(Ct.MOCK_KEY)
}