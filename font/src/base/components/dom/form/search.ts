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
    filter() {
        this.listui.filter(this.input.get_value())
        if (this.listui.option.data.size == 0) {
            this.dialog.hide()
        } else {
            this.dialog.show()
        }
    }
    init_event(): void {
        this.input.on_click(() => this.emit_search(this.open_dialog.bind(this)))
        this.input.on_input(this.filter.bind(this))
        this.listui.on_change((key: string, src: any, dst: Node) => {
            this.input.set_value(dst.title)
            if (this.option.id) {
                web_dom.set_local(this.option.id, dst.title)
            }
            this.dialog.hide()
            this.do_change(this.option.key, null, dst.value)
        })
    }
    set_title(s: string) {
        this.input.set_placeholder(s)
        return this
    }
    set_value(v: string): this {
        this.input.set_value(v)
        this.emit_search(() => {
            this.do_change(this.option.key, null, this.listui.get_data(v))
        })
        return this
    }
    get_value() {
        return this.input.get_value()
    }
    open_dialog() {
        if (this.listui.option.data.size) {
            this.show_search_dialog()
        } else {
            this.dialog.hide()
        }
    }
    emit_search(call_back: any) {
        let url = this.option.url
        web_dom.post(url, {
            key: this.input.get_value(),
            name: this.option.key,
        }, (node: Node) => {
            this.listui.set_option(node)
            call_back()

        })
        return this
    }
    render_option(): void {
        if (this.option.id) {
            web_dom.get_loacl_str(this.option.id, (v: any) => {

                this.do_change(this.option.key, this.get_value(), v)
                this.set_value(v)
            })
        }
    }
    show_search_dialog() {
        // console.log(this.get_rect(), this.el)
        this.dialog.set_style({
            left: this.input.get_abs_x(),
            top: this.input.get_abs_y() + this.input.get_height(),
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
