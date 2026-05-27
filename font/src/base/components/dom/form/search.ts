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
    selected_index: number = 0
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
            this.selected_index = 0
            this.update_selection()
            this.dialog.show()
        }
    }
    update_selection() {
        let children = this.listui.children
        for (let i = 0; i < children.length; i++) {
            if (i === this.selected_index) {
                children[i].set_style({ backgroundColor: "#ddd" })
            } else {
                children[i].set_style({ backgroundColor: "white" })
            }
        }
    }
    select_current() {
        let children = this.listui.children
        if (children.length > 0 && this.selected_index < children.length) {
            children[this.selected_index].el.click()
        }
    }
    init_event(): void {
        this.input.on_click(() => this.emit_search(this.open_dialog.bind(this)))
        this.input.on_input(this.filter.bind(this))
        this.input.on_key_down((e: KeyboardEvent) => {
            let children = this.listui.children
            if (!this.dialog.is_visible() || children.length === 0) return
            if (e.key === "ArrowDown") {
                e.preventDefault()
                this.selected_index = Math.min(this.selected_index + 1, children.length - 1)
                this.update_selection()
            } else if (e.key === "ArrowUp") {
                e.preventDefault()
                this.selected_index = Math.max(this.selected_index - 1, 0)
                this.update_selection()
            } else if (e.key === "Enter") {
                e.preventDefault()
                this.select_current()
            }
        })
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
            this.selected_index = 0
            this.update_selection()
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
            web_dom.get_local_str(this.option.id, (v: any) => {
                this.set_value(v)
            })
        }
    }
    show_search_dialog() {
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
