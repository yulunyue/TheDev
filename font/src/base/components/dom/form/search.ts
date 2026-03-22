import { Input } from "./input";
import web_dom from "../../../web/web_dom"
import Ct from "../../../web/constant"
import { Button } from "./button";
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
        this.listui.on_select((src: any) => {
            this.set_data(src)
            this.do_select(src)
        })
    }
    set_title(s: string) {
        this.input.set_placeholder(s)
        return this
    }
    set_data(value: Node): this {
        this.option.data = value
        this.input.set_value(value.get_title())
        this.dialog.hide()
        return super.set_data(value)
    }
    get_value() {
        return this.input.get_value()
    }
    emit_search() {
        let url = this.option.url
        if (!url) {
            url = this.option.parent.url + "/web_search"
        }
        web_dom.post(url, {
            key: this.input.get_value(),
            name: this.option.key,
        }, (node: Node) => {
            this.listui.set_option(node)
            if (this.listui.option.data.size) {
                this.show_search_dialog()
            } else {
                this.dialog.hide()
            }
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
