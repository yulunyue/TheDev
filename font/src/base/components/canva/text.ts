import { CanvaNode } from "./node";
export class CanvaTextNode extends CanvaNode {
    text: string = ""
    set_pos(y: number, x: number) {
        this.y = y
        this.x = x
        return this
    }
    draw(c: CanvasRenderingContext2D): void {
        c.strokeText(this.text, this.x, this.y)
    }
    set_text(s: string) {
        this.text = s
        return this
    }
}
export function text(s: string) {
    return new CanvaTextNode().set_text(s)
}