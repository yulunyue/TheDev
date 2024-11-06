import { GNode, gnode } from "../gnode"
import { Node, Style, } from "../../../web/cls"
import Constant from "../../../web/constant"
import { Div } from "../../dom/div"
import web_dom from "../../../web/web_dom"

export class Text extends GNode {
    contain: Div
    foreign_object: GNode
    max_width: number
    init_node(): void {
        this.max_width = 150
        this.contain = new Div().set_style({
            border: "1px solid #000",
            width: this.max_width,
            // wordWrap: "break-word",
            padding: Constant.DEFAULT_PADDING,
            textAlign: "center"
        })
        this.foreign_object = this.add_child(gnode("foreignObject").add_childs([this.contain]))

    }

    set_style(s: Style) {
        this.contain.set_style(s)
        return this
    }
    set_html(s: string) {
        this.contain.set_html(s)
        web_dom.next_frame(() => {
            this._on_change?.()
            this.foreign_object.set_attr("y", -this.contain.get_height() / 2)
            this.foreign_object.set_attr("x", -this.contain.get_width() / 2)
            this.foreign_object.set_width(this.contain.get_width() + 4).set_height(this.contain.get_height() + 4)

        })
        return this
    }
    init_style(): void {

    }
    get_height() {
        return this.contain.get_height()
    }
    set_option(option: Node): this {
        this.set_html(option.title)
        return this
    }
}
export function text() {
    return new Text()
}