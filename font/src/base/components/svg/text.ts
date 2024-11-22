import { GNode } from "./gnode"
import { Node } from "../../web/cls"
export class GText extends GNode {
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
export function gtext() {
    return new GText()
}
