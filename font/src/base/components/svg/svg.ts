import { Div } from "../dom/div"
import { Defs } from "./defs"
import { GNode } from "./gnode"
import { Tree, tree } from "./comb/tree"
import { Node } from "../../web/cls"
import web_dom from "../../web/web_dom"
export class SvgNode extends Div {
    def: Defs
    constructor() {
        super("svg")
        this.add_child(new Defs())
    }
    create_element(name: string) {
        return web_dom.createElementNS(name)
    }
    get_x() {
        return this.el.clientLeft
    }
    get_y() {
        return this.el.clientTop
    }
    init_node(): void {
    }
    init_style(): void {
        this.set_attr("shape-rendering", "geometricPrecision")
    }
    on_render(): void {

    }

}
