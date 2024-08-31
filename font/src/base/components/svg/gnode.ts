import web_dom from "../../web/web_dom"
import { Div } from "../dom/div"
import { Node } from "../../web/cls"
export class GNode extends Div {
    constructor(name: string = "g", parent_type: string = "") {
        super(name, parent_type)
    }
    create_element(name: string) {
        return web_dom.createElementNS(name)
    }
    set_pos(x: number, y: number): this {
        return this.set_x(x).set_y(y)
    }
    set_x(x: number) {
        return this.set_attr("x", this.x(x))
    }
    set_y(y: number) {
        return this.set_attr("y", this.y(y))
    }
    get_x() {
        return parseFloat(this.get_attr("x"))
    }
    get_y() {
        return parseFloat(this.get_attr("y"))
    }
    set_option(option: Node): this {
        if (option.data.y != null) {
            return this.set_y(option.data.y)
        }
        if (option.data.x != null) {
            return this.set_x(option.data.x)
        }
        return this
    }

}
export function gnode() {
    return new GNode()
}