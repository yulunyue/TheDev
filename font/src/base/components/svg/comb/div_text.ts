import { GNode, gnode } from "../gnode"
import { Node, Style, } from "../../../web/cls"
import Constant from "../../../web/constant"
import { Div } from "../../dom/div"
import { Pre, pre } from "../../dom/label"
import web_dom from "../../../web/web_dom"

export class Text extends GNode {
    contain: Pre
    foreign_object: GNode
    width = 0
    height = 0
    init_node(): void {
        this.contain = pre().set_style({
            border: "1px solid #000",
            // margin: Constant.DEFAULT_MARGIN,
            padding: Constant.DEFAULT_PADDING,
            textAlign: "center"
        })
        this.foreign_object = this.add_child(gnode("foreignObject").add_childs([this.contain]))

    }

    // set_style(s: Style) {
    //     this.contain.set_style(s)
    //     return this
    // }
    set_text(s: any) {
        let w = 80

        // for (var i = 0; i < s.length; i++) {
        //     let w2 = web_dom.calc_text_width(s[i], Constant.DEFAULT_FONT_FAMILY, Constant.DEFAULT_FONT_SIZE)
        //     w = Math.max(w, w2)
        // }
        // this.contain.set_text(s)
        this.foreign_object.set_width(w + Constant.DEFAULT_PADDING * 3).set_attr("x", -w / 2)
        web_dom.next_frame(() => {
            this._on_change?.()
            this.foreign_object.set_attr("y", -this.contain.get_height() / 2).set_height(
                this.contain.get_height() + 4
            )

        })
        return this
    }
    init_style(): void {

    }
    set_width(w: number) {
        this.contain.set_width(w)
        this.foreign_object.set_width(w)
        return this
    }
    set_height(w: number) {
        this.contain.set_height(w)
        this.foreign_object.set_height(w)
        return this
    }
    get_height() {
        return this.contain.get_height()
    }
    render_option(): void {
        // this.set_text(this.option.title)
    }

}
export function text() {
    return new Text()
}