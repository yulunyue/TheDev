import { GNode } from "./gnode"
import { Rect, rect } from "./rect"
import { Node } from "../../web/cls"
import { Constant } from "../export"
class Tt extends GNode {
    constructor() {
        super('text')
    }
    get_rect() {
        let ret = this.el.getBoundingClientRect()
        return {
            width: ret.width,
            height: ret.height
        }
    }

}
export class GText extends GNode {
    text: Tt
    bg: Rect
    init_node(): void {
        this.bg = this.add_child(new Rect().set_color(Constant.COLOR_WHITE))
        this.text = this.add_child(new Tt())

    }
    init_style(): void {
        this.text.set_style({
            fontFamily: "Arial",
            dominantBaseline: "text-before-edge",
            textAnchor: 'start',
            fontSize: 16,
            cursor: "pointer",
        })
    }
    render_option() {

    }
    set_html(title: string) {
        if (title == undefined) {
            return this
        }
        this.text.set_html(title)
        requestAnimationFrame(() => {
            let r = this.text.get_rect()
            let w = r.width
            let h = r.height
            this.text.set_pos(-h / 2, -w / 2)
            this.bg.set_pos(-h / 2 - 2, -w / 2 - 2,)
            this.bg.set_wh(w + 4, h + 4)


        })
        return this
    }
}
export function gtext() {
    return new GText()
}
