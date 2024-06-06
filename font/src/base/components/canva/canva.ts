import { Div } from "../dom/div";
import { CanvaNode } from "./node";
import { text } from "./text"
export class Canva extends Div {
    el: HTMLCanvasElement
    context: CanvasRenderingContext2D
    nodes: CanvaNode[]
    init_node(): void {
        this.el = Div.create_element("canvas") as HTMLCanvasElement
        this.context = this.el.getContext("2d")
        this.nodes = []
    }
    add(node: CanvaNode) {
        this.nodes.push(node)
        return this
    }
    adds(childs: CanvaNode[]) {
        for (var i = 0; i < childs.length; i++) {
            this.add(childs[i])
        }
        return this
    }
    draw() {
        this.context.beginPath()
        this.context.stroke()
        for (var i = 0; i < this.nodes.length; i++) {
            this.nodes[i].draw(this.context)
        }
        this.context.fill()
        this.context.closePath()
        return this
    }
}
export function canca_dev() {
    return new Canva().adds([
        text("xxx").set_pos(20, 20)
    ]).draw()
}
export function canca() {
    return new Canva()
}