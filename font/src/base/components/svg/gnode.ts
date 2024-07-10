import web_dom from "../../web/web_dom"
import { Div } from "../dom/div"
export class GNode extends Div {
    constructor(name: string = "g", parent_type: string = "") {
        super(name, parent_type)
    }
    create_element(name: string) {
        return web_dom.createElementNS(name)
    }
    set_pos(x: number, y: number): this {
        this.set_attr("x", this.x(x)).set_attr("y", this.y(y))
        return this
    }
}
export function gnode() {
    return new GNode()
}