import { GNode } from "../gnode";
import { Axies } from "./axies"
import { Node } from "../../../web/cls";
export class Chart extends GNode {
    x_axies: Axies
    y_axies: Axies
    init_node(): void {
        this.x_axies = new Axies()
        this.y_axies = new Axies()
        this.add_childs([
            this.x_axies,
            this.y_axies
        ])
    }
    get_width() {
        return 500
    }
    get_height() {
        return 500
    }
    render_option(): void {
        this.x_axies.set_option({
            x: this.get_width()
        })
    }
}