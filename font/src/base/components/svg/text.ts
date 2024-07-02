import { GNode } from "./gnode"
export class Text extends GNode {
    constructor() {
        super("text")
    }
    init_style(): void {
        this.set_style({
            fontFamily: "Arial",
            dominantBaseline: "middle",
            textAnchor: 'middle',
            fontSize: 20,
            cursor: "pointer",
        })
    }
}
export function text() {
    return new Text()
}