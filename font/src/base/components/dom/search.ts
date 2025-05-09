import { Input } from "./input";
import web_dom from "../../web/web_dom"
import Ct from "../../web/constant"
import { Title, Button } from "./button";
import { Node, to_node } from "../../web/cls";
import { listui } from "./list";
import { Div } from "./div"
import { ListUi } from "./list";
export class Search extends Div {
    dialog: Div
    listui: ListUi
    input: Input

    search_url: any
    _value: Node
    set_flex_style() {
        return this
    }
    init_node(): void {
        this.input = this.add_child(new Input())
        this.dialog = this.add_child(new Div().hide())
        this.listui = this.dialog.add_child(new ListUi())
    }
    set_title(s: string) {
        this.input.set_placeholder(s)
        return this
    }
    set_value(value: Node): this {
        if (this._id && this.local_storge_enable) {
            web_dom.set_local(this._id, value.dump())
        }
        this._value = value
        this._on_change?.(value)
        this.input.set_value(value.title)
        return this
    }
    get_value() {
        return this._value
    }
    set_id(id: string): this {
        super.set_id(id)
        if (this.local_storge_enable) {
            this.set_value(web_dom.get_local(id))
        }
        return this
    }
    set_search(url: string) {
        this.search_url = url
        web_dom.bind_click(this.input.el, () => this.emit_search())
        web_dom.bind_input(this.input.el, () => this.filter_local())
        return this
    }
    emit_search(url?: string) {
        web_dom.post(this.search_url, { value: this.input.get_value() }, (node: Node) => {
            this.set_option(node)
            this.show_search_dialog()
        })
        return this
    }
    filter_local() {
        let value = this.input.get_value()
        this.listui.childs.map((v: Div) => {
            v.option.title.indexOf(value) != -1 ? v.show() : v.hide()
        })
    }
    filter() {
        this.listui.set_option(
            //to_node(this.option).filter(this.get_value())
            this.option
        ).select((v: any) => {
            this.set_value(v)

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
        this.filter()
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
    return search().set_search(Ct.MOCK_KEY)
}