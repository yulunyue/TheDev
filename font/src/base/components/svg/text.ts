import { GNode } from "./gnode"
import { Node } from "../../web/cls"
export class Text extends GNode {
    constructor() {
        super("text")
    }
    init_style(): void {
        this.set_style({
            fontFamily: "Arial",
            dominantBaseline: "middle",
            textAnchor: 'middle',
            fontSize: 16,
            cursor: "pointer",
        })
    }
    set_option(option: Node): this {
        this.set_html(option.title)
        return super.set_option(option)
    }
}
export function text() {
    return new Text()
}
export function text_mid_max(){
    return text().set_pos(100,100).set_font_size(30)
}