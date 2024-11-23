import { GNode } from "./gnode"
import Constant from "../../web/constant";
export class Rect extends GNode {
    constructor() {
        super("rect")
    }
    init_style(): void {
        this.set_color(Constant.COLOR_WHITE)
    }
    set_wh(w: number, h: number) {
        return this.set_width(w).set_height(h)
    }
    set_width(x: number) {
        return this.set_attr("width", x)
    }
    set_height(y: number) {
        return this.set_attr("height", y)
    }
}
// export class Polygon extends GNode {
//     constructor() {
//         super("polygon")
//     }
// }


export function rect() {
    return new Rect()
}