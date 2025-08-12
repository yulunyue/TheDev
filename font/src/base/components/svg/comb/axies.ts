import { GNode } from "../gnode";
import { Rect } from "../rect";
export class Axies extends GNode {
    main_line: Rect
    init_node(): void {
        this.main_line = new Rect()
        this.add_childs([this.main_line])
    }
    render_option(): void {
        this.main_line.set_wh(this.option.x, 10)
    }
}